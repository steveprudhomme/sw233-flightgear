"""Copy editable aircraft sources to an untracked FlightGear package."""

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def package(output: Path) -> Path:
    """Never overwrite a package or delete an existing user's directory."""
    destination = output / "Aircraft" / "SW233"
    if destination.exists():
        raise FileExistsError(f"Destination already exists: {destination}")
    shutil.copytree(ROOT / "src" / "SW233", destination)
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build")
    print(package(parser.parse_args().output).resolve())
