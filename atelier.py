"""Atelier Windows : construire et filmer le SW233 dans un dossier neuf."""

import json
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

from tools.annotate import annotate
from tools.flightgear import execute
from tools.package import ROOT, package


def choose_path(label, default):
    value = input(f"{label}\nEntrée pour {default}, ou colle un autre chemin : ").strip('" ')
    return Path(value) if value else default


def main():
    print("Ferme FlightGear avant de commencer. Chaque essai aura son propre dossier.")
    default_exe = Path("C:/Program Files/FlightGear 2024.1/bin/fgfs.exe")
    exe = choose_path("Programme FlightGear", default_exe)
    downloads = Path.home() / "FlightGear/Downloads"
    data = choose_path("Données de FlightGear", downloads/"fgdata_2024_1")
    local = ROOT/"build/scene-CYJN"
    scene = choose_path("Décor TerraSync", local if local.exists() else downloads/"TerraSync")
    if not (exe.is_file() and (data/"defaults.xml").is_file()):
        raise ValueError("Programme ou données introuvables. Revois l’étape 1 du tutoriel.")
    if not (scene/"Terrain/w080n40/w074n45/CYJN.btg.gz").is_file():
        raise ValueError("Il manque la piste de CYJN. Suis l’étape 2 du tutoriel.")
    if not shutil.which('ffmpeg'):
        raise ValueError("FFmpeg est introuvable. Revois l’étape 1.")
    folder = ROOT/"build"/datetime.now().strftime("atelier-%Y%m%d-%H%M%S")
    folder.mkdir(parents=True)
    package(folder)
    home = folder/"session"
    home.mkdir()
    log = folder/"vol.log"
    options = [str(exe),f"--fg-root={data}",f"--fg-aircraft={folder/'Aircraft'}",
               f"--fg-scenery={scene}", "--aircraft=sw233","--airport=CYJN","--altitude=5000",
               "--vc=60","--heading=010","--in-air","--start-date-gmt=2026:06:21:16:45:00",
               "--disable-real-weather-fetch","--disable-terrasync","--geometry=1280x720",
               "--httpd=8094","--prop:/sim/presets/trim=true","--prop:/controls/flight/elevator=-0.6244"]
    print("Chargement du décor… Ne change pas la taille de la fenêtre pendant le film.")
    with log.open('w') as journal:
        proc = subprocess.Popen(options, cwd=folder, env={**os.environ,'FG_HOME':str(home)},
                                stdout=journal, stderr=subprocess.STDOUT)
        try:
            for _ in range(180):
                if proc.poll() is not None:
                    raise RuntimeError(f"FlightGear s’est arrêté. Journal : {log}")
                try:
                    base = 'http://127.0.0.1:8094/json/'
                    with urlopen(base+'sim/fg-home', timeout=1) as res:
                        ours = Path(json.load(res)['value']).resolve() == home.resolve()
                    with urlopen(base+'sim/initialized', timeout=1) as res:
                        if ours and json.load(res).get('value'):
                            break
                except (OSError, KeyError):
                    pass
                time.sleep(1)
            else:
                raise RuntimeError("Session indisponible : vérifie le port 8094 et le journal.")
            time.sleep(5)
            execute((ROOT/'tools/native-demo.nas').read_text(encoding='utf-8'),8094)
            for _ in range(240):
                time.sleep(1)
                with urlopen(base+'sim/sw233/demo/active',timeout=5) as res:
                    if json.load(res).get('value') == 0:
                        break
            else:
                raise RuntimeError("Le vol ne s’est pas terminé.")
            time.sleep(2)
        finally:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=15)
    film = folder/"Mon-vol-CYJN.mp4"
    annotate(folder/"SW233-CYJN-angles.mp4", log, film)
    print(f"Ton film est prêt : {film}")


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        raise SystemExit(str(error)) from error
