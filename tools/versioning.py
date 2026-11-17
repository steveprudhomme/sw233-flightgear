"""Read and validate the shared SemVer release identity."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)


def validate(value):
    match = PATTERN.fullmatch(value)
    if not match or any(len(p) > 1 and p.startswith("0") and p.isdigit()
                        for p in (match.group(4) or "").split(".")):
        raise ValueError(f"Invalid SemVer: {value}")
    return value


def project_version():
    version = validate((ROOT / "VERSION").read_text(encoding="utf-8").strip())
    aircraft = ET.parse(ROOT / "src/SW233/sw233-set.xml")
    if aircraft.findtext("sim/aircraft-version") != version:
        raise ValueError("VERSION and FlightGear aircraft-version differ")
    return version
