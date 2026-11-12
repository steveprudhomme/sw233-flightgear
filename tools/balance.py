"""AUD-01: mass, balance and pitch-moment diagnostics; no source FDM changes."""

import argparse
import csv
import hashlib
import json
import math
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import jsbsim
import numpy as np

from tools.glide import ROOT, aircraft, trim_glide


def source_balance(front, rear, arms=None):
    """Independent weight/first-moment calculation from the source XML (lb, in)."""
    if not all(math.isfinite(w) and w >= 0 for w in (front, rear)):
        raise ValueError("Occupant weights must be finite and nonnegative")
    root = ET.parse(ROOT / "src/SW233/sw233.xml").getroot()
    mass = root.find("mass_balance")
    empty = float(mass.findtext("emptywt"))
    cg = mass.find("location[@name='CG']")
    points = mass.findall("pointmass")
    weights = [empty, front, rear]
    positions = [[float(cg.findtext(axis)) for axis in "xyz"]]
    positions += [[float(p.findtext("location/" + axis)) for axis in "xyz"] for p in points]
    if arms is not None:
        positions[1][0], positions[2][0] = arms
    total = sum(weights)
    center = [sum(w * p[i] for w, p in zip(weights, positions)) / total for i in range(3)]
    return total, center


def prepare(front, rear, mode="source"):
    """Each sensitivity is isolated; manual arms assume a common datum, unverified."""
    fdm = aircraft()
    fdm["inertia/pointmass-weight-lbs"] = front
    fdm["inertia/pointmass-weight-lbs[1]"] = rear
    for axis in ("north", "east", "down"):
        fdm[f"atmosphere/wind-{axis}-fps"] = 0
    fdm["atmosphere/turb-type"] = 0
    fdm["fcs/pitch-trim-cmd-norm"] = 0
    fdm["fcs/speedbrake-cmd-norm"] = 0
    arms = None
    if mode == "manual-arms-assumption":
        arms = (43.8, 74.7)
        for i, arm in enumerate(arms):
            suffix = "" if i == 0 else "[1]"
            fdm["inertia/pointmass-location-X-inches" + suffix] = arm
    elif mode == "arp-forward-one-inch":
        fdm["metrics/aero-rp-x-in"] -= 1
    elif mode != "source":
        raise ValueError("Unknown sensitivity mode")
    fdm["ic/h-sl-ft"] = 5000
    fdm["ic/vc-kts"] = 50
    if not fdm.run_ic():
        raise RuntimeError("Initial conditions rejected")
    weight, center = source_balance(front, rear, arms)
    for prop, expected in zip(
        ["inertia/weight-lbs"] + [f"inertia/cg-{axis}-in" for axis in "xyz"],
        [weight] + center,
    ):
        if abs(fdm[prop] - expected) > 1e-8:
            raise AssertionError(f"Independent mass balance differs: {prop}")
    return fdm


def pitch_terms(fdm):
    """Structural inches to body feet; y moment of r cross F = rz Fx - rx Fz."""
    rx = (fdm["inertia/cg-x-in"] - fdm["metrics/aero-rp-x-in"]) / 12
    rz = (fdm["inertia/cg-z-in"] - fdm["metrics/aero-rp-z-in"]) / 12
    transport = rz * fdm["forces/fbx-aero-lbs"] - rx * fdm["forces/fbz-aero-lbs"]
    intrinsic = fdm["aero/sw233/load-pitch"]
    measured = fdm["moments/m-aero-lbsft"]
    if abs(intrinsic + transport - measured) > 1e-6:
        raise AssertionError("Pitch-moment transport does not close")
    return {"intrinsic_pitch_lbsft": intrinsic, "transport_pitch_lbsft": transport,
            "total_aero_pitch_lbsft": measured}


def measure(front, rear, mode="source", speed=50):
    fdm = prepare(front, rear, mode)
    result = {"mode": mode, "front_lbs": front, "rear_lbs": rear,
              "weight_lbs": fdm["inertia/weight-lbs"],
              "cg_x_in": fdm["inertia/cg-x-in"], "cg_z_in": fdm["inertia/cg-z-in"],
              "arp_x_in": fdm["metrics/aero-rp-x-in"], "requested_speed_kts": speed}
    try:
        result.update(trim_glide(fdm, speed))
    except (RuntimeError, np.linalg.LinAlgError) as error:
        result.update(status="no_equilibrium_found", reason=str(error))
        return result
    result.update(pitch_terms(fdm))
    result["elevator_deg"] = math.degrees(fdm["fcs/elevator-pos-rad"])
    result["remaining_command_percent"] = 100 * (1 - abs(result["elevator_norm"]))
    result["udot_ft_s2"] = fdm["accelerations/udot-ft_sec2"]
    result["wdot_ft_s2"] = fdm["accelerations/wdot-ft_sec2"]
    result["qdot_rad_s2"] = fdm["accelerations/qdot-rad_sec2"]
    result["status"] = "equilibrium_found"
    for _ in range(60 * 120):
        if not fdm.run() or not all(math.isfinite(fdm[p]) for p in
                                   ("position/h-sl-ft", "velocities/vc-kts")):
            raise RuntimeError("Non-finite or interrupted trajectory")
    result["speed_after_60s_kts"] = fdm["velocities/vc-kts"]
    result["altitude_after_60s_ft"] = fdm["position/h-sl-ft"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    args.folder.mkdir(parents=True, exist_ok=False)
    rows = [measure(front, rear) for front, rear in
            ((180, 0), (180, 180), (220, 140), (140, 220), (220, 210))]
    rows += [measure(180, 180, mode) for mode in
             ("manual-arms-assumption", "arp-forward-one-inch")]
    keys = list(dict.fromkeys(key for row in rows for key in row))
    with (args.folder / "balance.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
    metadata = {"source_commit": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "jsbsim_version": jsbsim.__version__,
        "tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fdm_sha256": hashlib.sha256((ROOT / "src/SW233/sw233.xml").read_bytes()).hexdigest(),
        "conditions": "JSBSim standalone; 5000 ft MSL, 50 kt CAS, zero wind, trim=0, spoilers=0",
        "warning": ("Alignment to the manual datum is unverified. "
                    "Sensitivities are not corrections."),
        "results": rows}
    (args.folder / "balance.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    for row in rows:
        print(row["mode"], row["front_lbs"], row["rear_lbs"], row["status"],
              round(row["cg_x_in"], 4), row.get("elevator_norm", "--"))


if __name__ == "__main__":
    main()
