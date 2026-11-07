"""Summarize the matched-speed SW233 descent and encode native cockpit excerpts."""

import argparse
import bisect
import csv
import json
import shutil
import statistics
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import findfont
from PIL import Image, ImageDraw, ImageFont


def report(folder, output):
    output.mkdir(exist_ok=False, parents=True)
    with (folder / "vol.csv").open() as f:
        rows = [
            {k: v if k == "frame" else float(v) for k, v in r.items()} for r in csv.DictReader(f)
        ]
    if rows[-1]["phase"] != 5:
        raise ValueError("Vol incomplet")
    windows = [(55, 60), (105, 110)]
    summary = []
    for start, end in windows:
        part = [r for r in rows if start <= r["time"] <= end]
        if len(part) < 10:
            raise ValueError("Échantillons insuffisants")
        summary.append(
            {k: statistics.mean(r[k] for r in part) for k in ["kt", "fpm", "ind", "brake", "wind"]}
        )
    if abs(summary[0]["kt"] - summary[1]["kt"]) > 2:
        raise ValueError(f"Vitesses non comparables : {summary}")
    print(json.dumps(summary, indent=2))
    (output / "resultats.json").write_text(json.dumps(summary, indent=2))
    shutil.copyfile(folder / "vol.csv", output / "vol.csv")
    shown = [r for r in rows if r["time"] >= 45]
    fig, axes = plt.subplots(3, 1, figsize=(10, 6.4), sharex=True, layout="constrained")
    ts = [r["time"] for r in shown]
    axes[0].plot(ts, [r["fpm"] for r in shown], label="Trajectoire", color="#176f82")
    axes[0].plot(ts, [r["ind"] for r in shown], label="Instrument", color="#b94e31")
    axes[0].set_ylabel("Montée signée (ft/min)")
    axes[0].legend()
    axes[1].plot(ts, [r["kt"] for r in shown], color="#176f82")
    axes[1].set_ylabel("Vitesse indiquée (kt)")
    axes[2].plot(ts, [100 * r["brake"] for r in shown], color="#535b7b")
    axes[2].set_ylabel("Aérofreins (%)")
    axes[2].set_xlabel("Temps de simulation (s) · bandes : fenêtres comparées")
    for ax in axes:
        for a, b in windows:
            ax.axvspan(a, b, color="#dcebdc")
        ax.grid(axis="y", alpha=0.25)
    fig.suptitle("CYJN · descente à vitesse indiquée comparable")
    fig.savefig(output / "courbes-vario.png", dpi=140)
    plt.close(fig)
    font = ImageFont.truetype(findfont("DejaVu Sans"), 21)
    all_t = [r["time"] for r in rows]

    def at(t):
        return rows[min(len(rows) - 1, bisect.bisect_left(all_t, t))]

    def frame(r, title):
        with Image.open(folder / r["frame"]) as src:
            im = Image.new("RGB", (960, 620), "#122736")
            im.paste(src.resize((960, 540), Image.Resampling.LANCZOS))
        d = ImageDraw.Draw(im)
        d.text((16, 546), f"CYJN · {title} · t={r['time']:.1f} s · {r['kt']:.1f} kt", font=font)
        d.text(
            (16, 580),
            f"Trajectoire {r['fpm']:.0f} ft/min  |  Cadran {r['ind']:.0f} ft/min"
            f"  |  Aérofreins {100 * r['brake']:.0f} %",
            font=font,
        )
        return im

    for t, title, name in [
        (57, "Aérofreins rentrés", "rentres"),
        (62, "Sortie des panneaux", "sortie"),
        (107, "Aérofreins sortis", "sortis"),
    ]:
        frame(at(t), title).save(output / (name + ".jpg"), quality=94)
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-n",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        "960x620",
        "-r",
        "6",
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-crf",
        "19",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output / "variometre-cyjn.mp4"),
    ]
    with subprocess.Popen(cmd, stdin=subprocess.PIPE) as ff:
        for start, duration, title in [(55, 5, "Rentrés"), (60, 7, "Sortie"), (105, 5, "Sortis")]:
            for i in range(duration * 6):
                ff.stdin.write(frame(at(start + i / 6), title).tobytes())
        ff.stdin.close()
        if ff.wait():
            raise RuntimeError("Encodage impossible")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report(args.folder, args.output)
