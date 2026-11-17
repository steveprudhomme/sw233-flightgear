"""Record a native static FlightGear presentation; this is not a flight test."""
import argparse
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

from tools.flightgear import execute

VIEW = "/sim/current-view/"
CAMERA = [VIEW + name for name in (
    "heading-offset-deg", "pitch-offset-deg", "field-of-view", "z-offset-m")]
BRAKE = "/fdm/jsbsim/fcs/speedbrake-pos-norm"
SCENES = (
    ("Extérieur — présentation statique", 1, 140, 18, 40, 0, False),
    ("Spoilers : sortie puis rentrée", 1, 140, 10, 35, 0, True),
    ("Grille UV — contrôle des surfaces", 1, 140, 38, 38, 1, False),
    ("Vue pilote — instruments et verre", 0, 0, -18, 65, 0, False),
    ("Vue latérale — spoilers", 0, 90, 12, 85, 0, True),
    ("Poste arrière — tenue et harnais", 0, 180, -15, 80, 0, False),
    ("Retour au poste avant", 0, 0, -18, 65, 0, False),
)


def record(folder, port, fps=8, seconds=4):
    base = f"http://127.0.0.1:{port}"

    def get(path):
        with urlopen(base + "/json" + path, timeout=15) as response:
            return json.load(response).get("value")

    def put(values):
        normalized = {p: int(v) if isinstance(v, bool) else v for p, v in values.items()}
        execute("".join(f"setprop({json.dumps(p)},{json.dumps(v)});"
                        for p, v in normalized.items()), port)

    if get("/sim/aircraft") != "sw233" or get("/sim/flight-model") != "null":
        raise ValueError("A dedicated SW233 null-FDM session is required")
    if fps <= 0 or seconds < 1:
        raise ValueError("Positive frame rate and at least one second per scene required")
    properties = ["/sim/menubar/visibility", "/sim/freeze/master", BRAKE,
                  "/sim/sw233/visuals/uv-grid"]
    saved = {p: get(p) for p in properties}
    if any(v is None for v in saved.values()):
        raise ValueError("Initialize visual test properties before recording")
    initial_view = get(VIEW + "view-number")

    def camera_snapshot():
        settings = {p: get(p) for p in CAMERA}
        if any(v is None for v in settings.values()):
            raise ValueError("Initialize camera properties before recording")
        return settings

    if initial_view is None:
        raise ValueError("Initialize current view before recording")
    cameras = {initial_view: camera_snapshot()}
    folder.mkdir(parents=True, exist_ok=False)
    report = {"scope": "Native static presentation, not a flight or slip validation",
              "encoding_fps": fps, "frames": [], "restored": False}
    start = time.monotonic()
    try:
        put({"/sim/menubar/visibility": 0, "/sim/freeze/master": 1})
        frame_id = 0
        for title, view, heading, pitch, fov, grid, animate in SCENES:
            put({VIEW + "view-number": view})
            if view not in cameras:
                cameras[view] = camera_snapshot()
            put({CAMERA[0]: heading, CAMERA[1]: pitch, CAMERA[2]: fov,
                 CAMERA[3]: -25 if view == 1 else 1.65,
                 "/sim/sw233/visuals/uv-grid": grid, BRAKE: 0})
            time.sleep(.3)
            for index in range(fps * seconds):
                begin = time.monotonic()
                fraction = index / max(1, fps * seconds - 1)
                brake = max(0, 1 - abs(2 * fraction - 1)) if animate else 0
                put({BRAKE: brake})
                with urlopen(base + "/screenshot?type=jpg", timeout=25) as response:
                    data = response.read()
                with Image.open(io.BytesIO(data)) as image:
                    if image.width < 1024 or image.height < 600:
                        raise ValueError("Restore the FlightGear window before capture")
                    image.verify()
                name = f"{frame_id:04d}.jpg"
                (folder / name).write_bytes(data)
                report["frames"].append({"file": name, "scene": title,
                    "seconds_since_start": time.monotonic() - start, "spoilers": brake})
                frame_id += 1
                time.sleep(max(0, 1 / fps - (time.monotonic() - begin)))
    except Exception as exc:
        report["error"] = str(exc)
        raise
    finally:
        errors = []

        def restore(path, value):
            try:
                put({path: value})
                if get(path) != value:
                    raise RuntimeError("value differs after restore")
                return True
            except Exception as exc:
                errors.append(f"{path}: {exc}")
                return False

        for view, settings in cameras.items():
            if restore(VIEW + "view-number", view):
                for path, value in settings.items():
                    restore(path, value)
        for path, value in saved.items():
            restore(path, value)
        # Selecting a view can reset its transient offsets. Apply the initial
        # camera again after the final switch, then verify each restored value.
        if restore(VIEW + "view-number", initial_view):
            for path, value in cameras[initial_view].items():
                restore(path, value)
        report["saved_cameras"] = cameras
        report["restored"] = not errors
        report["restoration_errors"] = errors
        (folder / "record.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        if errors:
            raise RuntimeError(f"Incomplete restoration: {errors}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    record(args.folder, args.port)
