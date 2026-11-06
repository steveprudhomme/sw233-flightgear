"""Continuous scripted flight: airbrakes, crossed controls, then recovery.

The test driver commands controls only. It never overwrites JSBSim attitude,
position or sideslip after initialization. Not an aircraft autopilot.
"""

import math

import numpy as np

from tools.glide import aircraft, trim_glide

FIELDS = (
    "time_s", "north_m", "east_m", "height_m", "roll_rad", "pitch_rad", "yaw_rad",
    "cas_kt", "altitude_ft", "beta_deg", "spoilers_norm", "aileron_norm",
    "rudder_norm", "elevator_norm", "vertical_fps",
)
DURATION = 66
SAMPLE_TICKS = 5  # 24 samples/s, playback at real time.


def phase(t):
    if t < 8:
        return "Vol stabilisé · vue extérieure"
    if t < 14:
        return "Place avant · commandes au neutre"
    if t < 18:
        return "Ouverture des aérofreins"
    if t < 24:
        return "Aérofreins sortis"
    if t < 28:
        return "Fermeture des aérofreins"
    if t < 34:
        return "Aérofreins rentrés"
    if t < 40:
        return "Entrée en virage · commandes croisées"
    if t < 54:
        return "Virage en glissade · observer le fil"
    return "Retour au vol symétrique"


def targets(t):
    spoilers = min(1.0, max(0.0, (t-14)/4), max(0.0, (28-t)/4))
    slip = min(1.0, max(0.0, (t-34)/6), max(0.0, (58-t)/4))
    return spoilers, math.radians(20)*slip, 0.8*slip


def trace():
    fdm = aircraft()
    trim = trim_glide(fdm, speed=60)
    origin = [fdm["position/lat-gc-rad"], fdm["position/long-gc-rad"]]
    pitch = fdm["attitude/theta-rad"]
    rows = []
    for tick in range(DURATION*120 + 1):
        t = tick/120
        if tick % SAMPLE_TICKS == 0:
            rows.append((
                t,
                (fdm["position/lat-gc-rad"]-origin[0])*6371000,
                (fdm["position/long-gc-rad"]-origin[1])*math.cos(origin[0])*6371000,
                fdm["position/h-sl-ft"]*.3048,
                fdm["attitude/phi-rad"], fdm["attitude/theta-rad"],
                fdm["attitude/psi-rad"], fdm["velocities/vc-kts"],
                fdm["position/h-sl-ft"], fdm["aero/beta-deg"],
                fdm["fcs/speedbrake-pos-norm"], fdm["fcs/aileron-cmd-norm"],
                fdm["fcs/rudder-cmd-norm"], fdm["fcs/elevator-cmd-norm"],
                -fdm["velocities/v-down-fps"],
            ))
        if tick == DURATION*120:
            break
        spoilers, bank, rudder = targets(t)
        roll_error = bank-fdm["attitude/phi-rad"]
        fdm["fcs/aileron-cmd-norm"] = float(np.clip(
            2.5*roll_error - .8*fdm["velocities/p-rad_sec"], -1, 1))
        fdm["fcs/rudder-cmd-norm"] = rudder
        fdm["fcs/speedbrake-cmd-norm"] = spoilers
        fdm["fcs/elevator-cmd-norm"] = float(np.clip(
            trim["elevator_norm"] + 2*(fdm["attitude/theta-rad"]-pitch)
            + 1.1*fdm["velocities/q-rad_sec"], -1, 1))
        if not fdm.run():
            raise RuntimeError("JSBSim stopped")
    values = np.array(rows)
    if not np.isfinite(values).all():
        raise RuntimeError("Non-finite test state")
    return values


if __name__ == "__main__":
    data = trace()
    for t in (0, 18, 24, 28, 40, 50, 58, 66):
        row = data[np.argmin(abs(data[:, 0]-t))]
        print(t, dict(zip(FIELDS[4:], np.round(row[4:], 4))))
