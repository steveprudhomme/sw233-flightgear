"""Create isolated planar test ramps for native terrain-ray verification."""

import argparse
import json
import math
from pathlib import Path

CASES = [(0, 0), (25, 0), (-25, 0), (0, 25), (0, -25), (20, 20), (-20, -20)]


def build(destination):
    tile = destination / "Objects/w080n40/w074n45"
    tile.mkdir(parents=True, exist_ok=False)
    rows, manifest = [], []
    for index, (pitch, roll) in enumerate(CASES):
        lat = 45.297435 + (index // 3 + 1) * 90 / 111132
        lon = -73.275838 + (index % 3) * 90 / (111132 * math.cos(math.radians(lat)))
        sx, sy = math.tan(math.radians(pitch)), math.tan(math.radians(roll))
        # AC3D x/aft, y/up, z/left. Each 5 m square is coplanar.
        vertices, faces = [], []
        for ix in range(10):
            for iy in range(10):
                x, y = -25 + 5 * ix, -25 + 5 * iy
                start = len(vertices)
                for a, b in [(x, y), (x + 5, y), (x + 5, y + 5), (x, y + 5)]:
                    vertices.append((a, sx * a + sy * b, -b))
                faces.append((start, (ix + iy) % 2))
        data = [
            "AC3Db",
            'MATERIAL "light" rgb 0.75 0.75 0.72 amb .5 .5 .5 emis 0 0 0 spec 0 0 0 shi 0 trans 0',
            'MATERIAL "dark" rgb 0.28 0.35 0.4 amb .5 .5 .5 emis 0 0 0 spec 0 0 0 shi 0 trans 0',
            "OBJECT world",
            "kids 1",
            "OBJECT poly",
            f'name "ramp-{index}"',
            f"numvert {len(vertices)}",
        ]
        data += [" ".join(f"{v:.8f}" for v in p) for p in vertices]
        data += [f"numsurf {len(faces)}"]
        for start, material in faces:
            data += ["SURF 0x20", f"mat {material}", "refs 4"]
            data += [f"{start + i} 0 0" for i in range(4)]
        data += ["kids 0"]
        name = f"ramp-{index}.ac"
        (tile / name).write_text("\n".join(data) + "\n", encoding="utf-8")
        (tile / f"ramp-{index}.xml").write_text(
            f"<PropertyList><path>{name}</path><animation><object-name>ramp-{index}</object-name>"
            '<enable-hot type="bool">true</enable-hot></animation></PropertyList>',
            encoding="utf-8",
        )
        rows.append(f"OBJECT_STATIC ramp-{index}.xml {lon:.10f} {lat:.10f} 60 0 0 0")
        manifest.append(
            dict(
                index=index,
                latitude=lat,
                longitude=lon,
                elevation_m=60,
                slope_x=sx,
                slope_y=sy,
                angle_x=pitch,
                angle_y=roll,
            )
        )
    (tile / "1745362.stg").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (destination / "ramps.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    print(json.dumps(build(parser.parse_args().destination), indent=2))
