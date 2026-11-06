"""Send an explicit local development script to FlightGear's HTTP interface."""

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen


def execute(script, port=8089):
    body = json.dumps({"name": "", "children": [
        {"name": "script", "value": script},
    ]}).encode()
    request = Request(f"http://127.0.0.1:{port}/run.cgi?value=nasal", body,
                      {"Content-Type": "application/json"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("--port", type=int, default=8089)
    args = parser.parse_args()
    print(execute(args.script.read_text(encoding="utf-8"), args.port))
