"""Solve a descending equilibrium; never assume an unpowered level-flight trim."""

import argparse
import json
import math
from pathlib import Path

import jsbsim
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def aircraft():
    """Load our source directly, independently of installed JSBSim aircraft."""
    fdm = jsbsim.FGFDMExec(None)
    fdm.set_debug_level(0)
    fdm.set_aircraft_path(str(ROOT / "src" / "SW233"))
    if not fdm.load_model("sw233", False):
        raise RuntimeError("Unable to load SW233")
    fdm.set_dt(1 / 120)
    return fdm


def trim_glide(fdm, speed=50.0, altitude=5000.0):
    """Solve udot, wdot and qdot using alpha, descent angle and elevator.

    Degrees for angles, normalized elevator demand. This bounded Newton solver
    is a development instrument, not a FlightGear autopilot. Reject a saturated
    elevator or an unsupported operating point instead of reporting a false trim.
    """
    def residual(state):
        alpha, gamma, elevator = state
        fdm["ic/h-sl-ft"] = altitude
        fdm["ic/vc-kts"] = speed
        fdm["ic/alpha-deg"] = alpha
        fdm["ic/gamma-deg"] = gamma
        fdm["fcs/elevator-cmd-norm"] = elevator
        if not fdm.run_ic():
            raise RuntimeError("Initial conditions rejected")
        return np.array([fdm[p] for p in (
            "accelerations/udot-ft_sec2",
            "accelerations/wdot-ft_sec2",
            "accelerations/qdot-rad_sec2",
        )])

    state = np.array([4.0, -4.0, -0.8])
    for _ in range(15):
        error = residual(state)
        if np.max(np.abs(error)) < 1e-6:
            if not (-1 <= state[2] <= 1 and -20 < state[0] < 20 and -20 < state[1] < 0):
                raise RuntimeError("Equilibrium outside the supported development envelope")
            return {
                "alpha_deg": float(state[0]),
                "gamma_deg": float(state[1]),
                "elevator_norm": float(state[2]),
                "glide_ratio": 1 / math.tan(math.radians(-state[1])),
                "speed_kts": speed,
                "altitude_ft": altitude,
            }
        jacobian = np.column_stack([
            (residual(state + np.eye(3)[i] * 0.001) - error) / 0.001
            for i in range(3)
        ])
        state -= np.linalg.solve(jacobian, error)
        if not np.isfinite(state).all():
            raise RuntimeError("Non-finite trim iteration")
    raise RuntimeError("No descending equilibrium found within 15 iterations")


def simulate(seconds=60, speed=50):
    fdm = aircraft()
    result = trim_glide(fdm, speed)
    for _ in range(round(seconds * 120)):
        if not fdm.run():
            raise RuntimeError("Simulation stopped")
        if not all(math.isfinite(fdm[p]) for p in (
            "position/h-sl-ft", "velocities/vc-kts", "attitude/theta-rad",
        )):
            raise RuntimeError("Non-finite flight state")
    result.update({
        "duration_seconds": seconds,
        "final_speed_kts": fdm["velocities/vc-kts"],
        "final_altitude_ft": fdm["position/h-sl-ft"],
        "weight_lbs": fdm["inertia/weight-lbs"],
    })
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--speed", type=float, default=50)
    parser.add_argument("--seconds", type=float, default=60)
    args = parser.parse_args()
    print(json.dumps(simulate(args.seconds, args.speed), indent=2))
