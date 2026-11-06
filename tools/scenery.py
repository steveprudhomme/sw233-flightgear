"""Installer la tuile FlightGear de CYJN, sans remplacer de fichier différent."""

import argparse
import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen

BASE = "https://flightgear.sourceforge.net/scenery/"


def fetch(path):
    with urlopen(BASE+path, timeout=30) as response:
        return response.read()


def install(root):
    pending = []
    for folder in ("Terrain/w080n40/w074n45","Objects/w080n40/w074n45","Airports/C/Y/J"):
        lines = fetch(folder+"/.dirindex").decode().splitlines()
        if "path:"+folder not in lines:
            raise ValueError("Index de scène inattendu.")
        for line in lines:
            if not line.startswith("f:"):
                continue
            _, name, digest, size = line.split(":")
            if Path(name).name != name or name in (".",".."):
                raise ValueError("Nom de fichier inattendu.")
            if not folder.startswith("Airports") or name.startswith("CYJN"):
                pending.append((folder+"/"+name,digest,int(size)))

    def save(item):
        relative,digest,size = item
        target = root/relative
        data = target.read_bytes() if target.exists() else fetch(relative)
        if len(data) != size or hashlib.sha1(data).hexdigest() != digest:
            raise ValueError("Fichier différent ou incomplet : "+relative)
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)

    with ThreadPoolExecutor(6) as pool:
        list(pool.map(save,pending))
    if not (root/"Terrain/w080n40/w074n45/CYJN.btg.gz").is_file():
        raise ValueError("La piste de CYJN manque.")
    print(f"Décor prêt : {len(pending)} fichiers vérifiés dans {root.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, nargs="?", default=Path("build/scene-CYJN"))
    install(parser.parse_args().destination)
