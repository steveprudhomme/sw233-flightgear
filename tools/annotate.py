"""Label a native 1280x720 FlightGear recording using its own flight log."""

import argparse
import re
import subprocess
from pathlib import Path
from uuid import uuid4


def stamp(seconds):
    return f"0:{int(seconds)//60:02d}:{seconds%60:05.2f}"


def annotate(movie, log, output):
    samples = [list(map(float, m.split())) for m in re.findall(
        r"SW233_SAMPLE ([0-9.+ −-]+)", log.read_text(errors="replace"))]
    if not samples or samples[0][0] > 1 or samples[-1][0] < 65:
        raise ValueError("Incomplete native flight log")
    labels = [(8, "Vue extérieure"), (14, "Place avant · commande orange à gauche"),
              (18, "Sortie des aérofreins"), (24, "Aérofreins sortis"),
              (28, "Rentrée des aérofreins"), (34, "Aérofreins rentrés"),
              (40, "Entrée en glissade · commandes croisées"),
              (54, "Virage en glissade · détail du fil de laine"),
              (58, "Sortie de glissade"), (99, "Retour au vol symétrique")]
    events = []
    for i, (t, brake, beta, roll, speed, *_) in enumerate(samples):
        end = samples[i+1][0] if i+1 < len(samples) else 66.1
        label = next(v for k, v in labels if t < k)
        title = f"CYJN  /  {label}"
        data = (f"FlightGear 2024.1.4   ·   {speed:.0f} kt   ·   Aérofreins {brake:.0%}"
                f"   ·   Dérapage β {beta:+.1f}°   ·   Inclinaison {roll:+.1f}°")
        events.append(f"Dialogue: 0,{stamp(t)},{stamp(end)},Default,,0,0,0,,"
                      + r"{\pos(28,730)\b1}" + title + r"\N{\b0\fs21}" + data)
    header = Path(__file__).with_name('native-labels.ass').read_text(encoding='utf-8')
    captions = output.resolve().parent / f'labels-{uuid4().hex}.ass'
    graph = ("[0:v]fps=30,split[base][detail];[detail]crop=100:76:590:320,"
             "scale=240:182,drawbox=t=2:c=white[inset];[base]pad=1280:804:0:0:0x13242c[bg];"
             "[bg][inset]overlay=1012:20:enable='between(t,30,57.95)',ass=")+captions.name+"[v]"
    try:
        captions.write_text(header+'\n'.join(events)+'\n', encoding='utf-8')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-i',
                        str(movie.resolve()), '-filter_complex', graph, '-map', '[v]',
                        '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags',
                        '+faststart', str(output.resolve())], cwd=captions.parent, check=True)
    finally:
        captions.unlink(missing_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('movie', 'log', 'output'):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    annotate(args.movie, args.log, args.output)
