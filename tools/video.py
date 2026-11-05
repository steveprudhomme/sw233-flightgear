"""Render a real JSBSim trace with a schematic aircraft and illustrative terrain.

Requires Pillow, NumPy, JSBSim and ffmpeg. No FlightGear imagery is used.
Run from the repository root: python -m tools.video build/vol-plane.mp4
"""

import argparse
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from tools.cockpit import exterior, front_view
from tools.glide import aircraft, trim_glide

W, H, VW, VH = 1280, 720, 890, 458
FPS = 24
DURATION = 60
STEPS = 15  # 120 physics ticks/s, 3 simulation seconds per screen second.
INK = "#102c35"
PAPER = "#f4f1e7"
TEAL = "#006f72"
MINT = "#81d2be"


def font(size, bold=False):
    for family in (("DejaVuSans-Bold.ttf", "arialbd.ttf") if bold
                   else ("DejaVuSans.ttf", "arial.ttf")):
        try:
            return ImageFont.truetype(family, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


FONTS = {size: font(size, bold) for size, bold in
         [(14, True), (16, False), (18, True), (22, True), (32, True), (43, True)]}


def label(draw, xy, value, size=16, color=INK):
    draw.text(xy, value, fill=color, font=FONTS[size])


def trace():
    fdm = aircraft()
    trim_glide(fdm)
    origin = [fdm["position/lat-gc-rad"], fdm["position/long-gc-rad"]]
    samples = []
    for i in range(DURATION * 120 // STEPS + 1):
        lat = fdm["position/lat-gc-rad"]
        lon = fdm["position/long-gc-rad"]
        h = fdm["position/h-sl-ft"]
        samples.append((
            i * STEPS / 120,
            (lat - origin[0]) * 6371000,
            (lon - origin[1]) * math.cos(origin[0]) * 6371000,
            h * 0.3048,
            fdm["attitude/phi-rad"], fdm["attitude/theta-rad"], fdm["attitude/psi-rad"],
            fdm["velocities/vc-kts"], h,
        ))
        if i < DURATION * 120 // STEPS:
            for _ in range(STEPS):
                if not fdm.run():
                    raise RuntimeError("JSBSim stopped before the end of the test")
    return np.asarray(samples)


def terrain(x, y):
    return (95 * np.sin(x/2800 + y/3700) + 65 * np.cos(y/1900)
            + 80 * np.sin(x/4300 - y/2200))


def world():
    faces = []
    palette = ["#8faf96", "#9db69c", "#a6bdae", "#b6c6aa", "#9ab8a7", "#acc4af"]
    for i in range(-20, 22):
        for j in range(-20, 22):
            xy = np.array([(i, j), (i+1, j), (i+1, j+1), (i, j+1)]) * 740
            vertices = np.column_stack((xy, terrain(xy[:, 0], xy[:, 1])))
            color = palette[(i*19 + j*37 + (i*j) % 7) % len(palette)]
            faces.append((vertices, color))
    return np.stack([v for v, _ in faces]), [c for _, c in faces]


def rotation(roll, pitch, yaw):
    # Body vectors expressed in local north, east, up.
    cp, sp, ct, st, cy, sy = (math.cos(roll), math.sin(roll), math.cos(pitch),
                              math.sin(pitch), math.cos(yaw), math.sin(yaw))
    forward = [ct*cy, ct*sy, st]
    right = [sp*st*cy-cp*sy, sp*st*sy+cp*cy, -sp*ct]
    up = [-cp*st*cy-sp*sy, -cp*st*sy+sp*cy, cp*ct]
    return np.array([forward, right, up])


def scene(row, land, colors, aircraft_faces):
    t, north, east, up, roll, pitch, yaw, _, _ = row
    pos = np.array([north, east, up])
    angle = math.radians(28 + 75 * t / DURATION)
    eye = pos + np.array([18*math.cos(angle), -18*math.sin(angle), 5.0])
    view = pos-eye
    view /= np.linalg.norm(view)
    right = np.cross(view, [0, 0, 1])
    right /= np.linalg.norm(right)
    camera_up = np.cross(right, view)
    matrix = np.array([right, camera_up, view]).T

    def project(points):
        uv = points[..., :2] / np.maximum(points[..., 2:3], 0.1)
        return uv * [630, -630] + [VW*0.5, VH*0.46]

    view_image = Image.new("RGB", (VW, VH), "#c7dcd7")
    d = ImageDraw.Draw(view_image)
    for y in range(VH):
        f = min(1., y/145)
        rgb = tuple(round(a*(1-f) + b*f) for a, b in zip((123, 174, 189), (221, 230, 210)))
        d.line((0, y, VW, y), fill=rgb)
    camera = (land-eye) @ matrix
    projected = project(camera)
    visible = ((camera[:, :, 2].min(1) > 20)
               & (projected[:, :, 0].min(1) < VW) & (projected[:, :, 0].max(1) > 0)
               & (projected[:, :, 1].min(1) < VH) & (projected[:, :, 1].max(1) > 0))
    order = np.argsort(-camera[:, :, 2].mean(1))
    for idx in order[visible[order]]:
        d.polygon([tuple(p) for p in projected[idx]], fill=colors[idx])
    orient = rotation(roll, pitch, yaw)
    parts = [(((v @ orient + pos) - eye) @ matrix, col) for v, col in aircraft_faces]
    for v, col in sorted(parts, key=lambda item: -item[0][:, 2].mean()):
        normal = np.cross(v[1]-v[0], v[2]-v[0])
        norm = np.linalg.norm(normal)
        shade = .84 + (.16 * abs(normal[1])/norm if norm > 1e-9 else 0)
        d.polygon([tuple(p) for p in project(v)], fill=tuple(int(c*shade) for c in col))
    return view_image


def render(path):
    values, faces = trace(), exterior()
    land, palette = world()
    path.parent.mkdir(parents=True, exist_ok=True)
    ff = ["ffmpeg", "-loglevel", "error", "-n", "-f", "rawvideo", "-pix_fmt", "rgb24",
          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
          "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)]
    with subprocess.Popen(ff, stdin=subprocess.PIPE) as encoder:
        vs_fps = np.gradient(values[:, 8], values[:, 0])
        for i, row in enumerate(values):
            t, north, _, _, _, _, _, speed, altitude = row
            frame = Image.new("RGB", (W, H), PAPER)
            d = ImageDraw.Draw(frame)
            label(d, (34, 19), "SW233   /   CARNET D’ESSAIS", 14, TEAL)
            label(d, (34, 43), "Vol plané stabilisé", 43)
            label(d, (927, 53), "ESSAI  01    /    JSBSIM", 18, TEAL)
            front = t >= 39
            view = (front_view(row, vs_fps[i], land, palette, rotation) if front
                    else scene(row, land, palette, faces))
            frame.paste(view, (32, 112))
            title = "02  /  PLACE AVANT" if front else "01  /  VUE EXTÉRIEURE"
            d.rounded_rectangle((48, 124, 276, 154), radius=4, fill=INK)
            label(d, (58, 129), title, 14, PAPER)
            d.rectangle((940, 112, 1248, 570), fill=INK)
            label(d, (963, 137), "TÉLÉMÉTRIE DE VOL", 14, MINT)
            for y, title, value in [
                (181, "ALTITUDE  ·  MSL", f"{altitude:,.0f} ft".replace(",", " ")),
                (280, "VITESSE CALIBRÉE", f"{speed:.1f} kt".replace(".", ",")),
                (379, "DISTANCE NORD", f"{north/1000:.2f} km".replace(".", ",")),
            ]:
                label(d, (963, y), title, 14, "#bcd5ce")
                label(d, (961, y+23), value, 32, PAPER)
            label(d, (963, 507), f"t = {t:04.1f} s    /    60 s", 18, MINT)
            d.rectangle((964, 544, 1222, 546), fill="#56776f")
            d.rectangle((964, 544, 964+258*t/60, 546), fill=MINT)
            label(d, (34, 600), "SCHWEIZER SGS 2-33", 22)
            label(d, (34, 640), "970 lb   /   Air calme   /   Lecture ×3", 16, TEAL)
            label(d, (614, 602), "60 secondes de trajectoire calculée", 22)
            label(d, (614, 641), "Rejeu JSBSim · terrain et cockpit illustrés", 16)
            label(d, (34, 687), "SW233   /   PROTOTYPE EXPÉRIMENTAL", 14, TEAL)
            encoder.stdin.write(frame.tobytes())
        encoder.stdin.close()
        if encoder.wait():
            raise RuntimeError("ffmpeg could not encode the film")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    render(parser.parse_args().output)
