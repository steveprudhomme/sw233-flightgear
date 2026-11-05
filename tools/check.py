"""Check repository hygiene, XML structure, asset paths and DCO trailers."""

import argparse
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".xml", ".ac", ".md", ".py", ".yml", ".toml", ".txt"}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)


def check_sources():
    errors = []
    for relative in git("ls-files").splitlines():
        path = ROOT / relative
        if relative.startswith(("build/", "dist/", "work/", ".venv/")):
            errors.append(f"Generated/private content tracked: {relative}")
        if path.suffix in TEXT_SUFFIXES or path.name.startswith("."):
            text = path.read_text(encoding="utf-8")
            if not text.endswith("\n"):
                errors.append(f"Missing final newline: {relative}")
            if any(line.rstrip() != line for line in text.splitlines()):
                errors.append(f"Trailing whitespace: {relative}")
        if path.suffix == ".xml":
            ET.parse(path)
            if "TODO_" in path.read_text(encoding="utf-8"):
                errors.append(f"Unresolved numeric placeholder: {relative}")
    source = ROOT / "src" / "SW233"
    config = ET.parse(source / "sw233-set.xml").getroot()
    model = config.findtext("sim/model/path")
    if not model or not model.startswith("Aircraft/"):
        errors.append("Model path must be relative to Aircraft/")
    elif not (ROOT / "src" / model.removeprefix("Aircraft/")).is_file():
        errors.append(f"Missing model: {model}")
    fdm = ET.parse(source / "sw233.xml").getroot()
    axes = {axis.attrib["name"] for axis in fdm.findall("aerodynamics/axis")}
    if axes != {"LIFT", "DRAG", "SIDE", "ROLL", "PITCH", "YAW"}:
        errors.append("Missing aerodynamic axis")
    if errors:
        raise ValueError("\n".join(errors))


def check_dco(revision):
    commits = git("rev-list", revision).splitlines()
    if not commits:
        raise ValueError("No commits selected for DCO validation")
    for commit in commits:
        message = git("show", "-s", "--format=%B", commit)
        trailers = subprocess.check_output(
            ["git", "interpret-trailers", "--parse"], input=message, text=True, cwd=ROOT,
        )
        if not re.search(r"^Signed-off-by: .+ <[^<>\s]+@[^<>\s]+>$", trailers, re.M):
            raise ValueError(f"Missing DCO trailer: {commit}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dco", help="Git revision or range; for example origin/main..HEAD")
    args = parser.parse_args()
    check_sources()
    if args.dco:
        check_dco(args.dco)
    print("Source checks passed" + ("; DCO trailers present" if args.dco else ""))
