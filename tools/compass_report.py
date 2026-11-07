"""Analyse a SW233 compass flight; render its graph, stills and cockpit excerpts."""

import argparse
import bisect
import csv
import json
import shutil
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import findfont
from PIL import Image, ImageDraw, ImageFont


def wrap(angle):
    return (angle + 180) % 360 - 180


def analyse(rows, phase):
    turn = [r for r in rows if r["phase"] == phase]
    hold = [r for r in rows if r["phase"] == phase + 1]
    peak = max(turn, key=lambda r: abs(r["roll"]))
    level = next(r for r in turn + hold if r["time"] > peak["time"] and abs(r["roll"]) <= 3)
    start = settled = None
    for r in turn + hold:
        if r["time"] < level["time"]:
            continue
        if abs(r["err"]) <= 2 and abs(r["roll"]) <= 3:
            if start is None:
                start = r["time"]
            if r["time"] - start >= 3:
                settled = start
                break
        else:
            start = None
    north = next(b for a, b in zip(turn, turn[1:]) if abs(a["mag"] - b["mag"]) > 180)
    extreme = max(turn, key=lambda r: abs(r["err"]))
    return dict(
        entry=turn[0]["time"],
        north=north["time"],
        level=level["time"],
        settled=settled,
        end=hold[-1]["time"],
        err=extreme["err"],
        bank=peak["roll"],
    )


def render(folder, output):
    output.mkdir(exist_ok=False, parents=True)
    with (folder / "vol.csv").open() as f:
        rows = [
            {k: (v if k == "frame" else float(v)) for k, v in r.items()} for r in csv.DictReader(f)
        ]
    if rows[-1]["phase"] != 5 or any(b["time"] <= a["time"] for a, b in zip(rows, rows[1:])):
        raise ValueError("Trace incomplète ou horloge non monotone")
    for r in rows:
        r["err"] = wrap(r["ind"] - r["mag"])
    right, left = (analyse(rows, p) for p in (1, 3))
    print(json.dumps([right, left], indent=2))
    shutil.copyfile(folder / "vol.csv", output / "vol.csv")
    lo = right["entry"] - 5
    shown = [r for r in rows if r["time"] >= lo]
    ts = [r["time"] for r in rows]

    def at(t):
        i = min(len(ts) - 1, bisect.bisect_left(ts, t))
        return rows[i - 1] if i and t - ts[i - 1] < ts[i] - t else rows[i]

    fig, axes = plt.subplots(3, 1, figsize=(10, 6.4), sharex=True, layout="constrained")
    t = [r["time"] for r in shown]
    for ax in axes:
        for trace in (right, left):
            ax.axvspan(trace["entry"], trace["level"], color="#e9f0f4")
            ax.axvline(trace["north"], color="#687986", ls=":", lw=1)
        ax.grid(axis="y", alpha=0.25)
        ax.margins(x=0)
    for field, label, color in [
        ("mag", "Cap magnétique", "#086779"),
        ("ind", "Compas indiqué", "#bc522d"),
    ]:
        axes[0].plot(t, [wrap(r[field]) for r in shown], label=label, color=color)
    axes[0].set_ylabel("Cap relatif au nord (°)")
    axes[0].legend(loc="upper right", ncol=2)
    axes[1].plot(t, [r["err"] for r in shown], color="#ae462b")
    axes[1].axhspan(-2, 2, color="#c2e4cf")
    axes[1].set_ylabel("Indiqué − magnétique (°)")
    axes[2].plot(t, [r["roll"] for r in shown], color="#395271")
    axes[2].set_ylabel("Roulis (°)")
    axes[2].set_xlabel("Temps de simulation (s) · pointillés : passages du nord")
    fig.suptitle("Schweizer SGS 2-33 · Compas en virage à CYJN")
    fig.savefig(output / "courbes.png", dpi=140)
    plt.close(fig)
    windows = [
        ("Avant le virage", lo, 4),
        ("Droite · passage du nord", right["north"] - 4, 8),
        ("Après remise à plat", right["level"], 5),
        ("Gauche · passage du nord", left["north"] - 4, 8),
        ("Retour vers 330°", left["end"] - 5, 5),
    ]
    font = ImageFont.truetype(findfont("DejaVu Sans"), size=22)

    def card(r, title):
        with Image.open(folder / r["frame"]) as src:
            im = Image.new("RGB", (960, 620), "#142838")
            im.paste(src.resize((960, 540), Image.Resampling.LANCZOS))
            inset = src.crop((565, 324, 715, 469)).resize((165, 160), Image.Resampling.LANCZOS)
            im.paste(inset, (785, 8))
        d = ImageDraw.Draw(im)
        d.rectangle((784, 7, 950, 168), outline="#f5edd6")
        d.text((18, 545), f"CYJN   /   {title}    ·    t = {r['time']:.1f} s", font=font)
        d.text(
            (18, 581),
            f"Magnétique {r['mag']:05.1f}°   |   Compas {r['ind']:05.1f}°   |   "
            f"Écart {r['err']:+.1f}°   |   Roulis {r['roll']:+.1f}°",
            font=font,
        )
        return im

    for name, t, title in [
        ("avant", lo + 2, "Avant le virage"),
        ("nord", right["north"], "Franchissement du nord"),
        ("retour", left["end"] - 1, "Ailes revenues à plat"),
    ]:
        card(at(t), title).save(output / (name + ".jpg"), quality=92)
    command = [
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
        str(output / "compas-en-virage.mp4"),
    ]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as ff:
        for title, start, duration in windows:
            for i in range(6 * duration):
                ff.stdin.write(card(at(start + i / 6), title).tobytes())
        ff.stdin.close()
        if ff.wait():
            raise RuntimeError("Encodage impossible")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render(args.folder, args.output)
