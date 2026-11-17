"""Verify native SW233 checklist data and language transitions in a static session."""

import argparse
import io
import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

from PIL import Image

from tools.flightgear import execute
from tools.package import ROOT


def capture(output, port):
    base = f"http://127.0.0.1:{port}"

    def tree(path, depth=8):
        with urlopen(base + "/json" + path + f"?d={depth}", timeout=15) as response:
            return json.load(response)

    def get(path):
        try:
            return tree(path, 0).get("value")
        except HTTPError as error:
            if error.code == 404:
                return None
            raise

    def run(script):
        execute(script, port)

    def setprop(path, value):
        run(f"setprop({json.dumps(path)},{json.dumps(value, ensure_ascii=False)});")

    def close():
        run('setprop("/sim/sw233/test/dialog-was-open",'
            'fgcommand("dialog-close",props.Node.new({"dialog-name":"checklist"})));')
        return bool(get("/sim/sw233/test/dialog-was-open"))

    def opened():
        result = close()
        if result:
            run('gui.showDialog("checklist");')
        return result

    def children(node, name):
        return sorted([c for c in node.get("children", []) if c["name"] == name],
                      key=lambda c: c.get("index", 0))

    def field(node, name):
        return children(node, name)[0]["value"]

    def verify(language):
        expected = sources[language]
        actual = children(tree("/sim/checklists"), "checklist")
        assert len(actual) == len(expected) == 4
        for node, wanted in zip(actual, expected):
            assert field(node, "title") == wanted["title"]
            items = children(node, "item")
            assert [(field(i, "name"), field(i, "value")) for i in items] == wanted["items"]
        assert get("/sim/sw233/language") == language

    def screenshot(name):
        time.sleep(.5)
        with urlopen(base + "/screenshot?type=jpg", timeout=30) as response:
            data = response.read()
        with Image.open(io.BytesIO(data)) as image:
            assert image.width >= 1024 and image.height >= 600
        (output / name).write_bytes(data)

    if get("/sim/aircraft") != "sw233" or get("/sim/flight-model") != "null":
        raise ValueError("Use a dedicated SW233 --fdm=null session")
    output.mkdir(parents=True, exist_ok=False)
    version = get("/sim/version/flightgear")
    legacy = bool(get("/sim/sw233/checklist-ascii"))
    assert not legacy, "Accents must be preserved"
    sources = {}
    for language, filename in (("fr", "sw233.xml"), ("en", "sw233-en.xml")):
        lists = ET.parse(ROOT / "src/SW233/Checklists" / filename).findall("checklist")
        sources[language] = [
            {"title": c.findtext("title"),
             "items": [(i.findtext("name"),
                        i.findtext("value")) for i in c.findall("item")]}
            for c in lists]
    # The UI adaptation must not mutate the UTF-8 translation originals.
    for language, filename in (("fr", "sw233.xml"), ("en", "sw233-en.xml")):
        original = ET.parse(ROOT / "src/SW233/Checklists" / filename).findall("checklist")
        loaded = children(tree("/sim/sw233/translations/" + language), "checklist")
        assert len(loaded) == len(original)
        for node, expected in zip(loaded, original):
            assert field(node, "title") == expected.findtext("title")
            assert [(field(i, "name"), field(i, "value")) for i in children(node, "item")] == [
                (i.findtext("name"), i.findtext("value")) for i in expected.findall("item")]
    control_paths = ["/controls/flight/" + name for name in
                     ("aileron", "elevator", "rudder", "elevator-trim", "speedbrake")]
    controls = {p: get(p) for p in control_paths}
    saved_language = get("/sim/sw233/language")
    saved_selection = get("/sim/gui/dialogs/checklist/selected-checklist")
    initially_open = opened()
    report = {"version": version, "aircraft_dir": get("/sim/aircraft-dir"),
              "legacy_ascii": legacy, "lists": [], "transitions": [],
              "scope": "Native display and script tests, not physical keyboard or flight tests"}
    try:
        for language in ("fr", "en"):
            run(f'sw233_language.choose("{language}");')
            verify(language)
            for index, wanted in enumerate(sources[language]):
                close()
                setprop("/sim/gui/dialogs/checklist/selected-checklist", wanted["title"])
                setprop("/sim/gui/dialogs/checklist/selected-page", 0)
                run('gui.showDialog("checklist");')
                assert get("/sim/gui/dialogs/checklist/selected-checklist") == wanted["title"]
                assert opened()
                name = f"{language}-liste-{index}.jpg"
                screenshot(name)
                report["lists"].append({"language": language, "index": index,
                                        "file": name, **wanted})
        for is_open in (True, False):
            for iteration in range(12):
                if is_open:
                    language = get("/sim/sw233/language")
                    setprop("/sim/gui/dialogs/checklist/selected-checklist",
                            sources[language][3]["title"])
                    run('gui.showDialog("checklist");')
                else:
                    close()
                language = "en" if get("/sim/sw233/language") == "fr" else "fr"
                run("sw233_language.toggle();")
                verify(language)
                assert opened() == is_open
                selected = get("/sim/gui/dialogs/checklist/selected-checklist")
                assert selected == (sources[language][0]["title"] if is_open else None)
                if is_open and iteration < 2:
                    screenshot(f"bascule-ouverte-{language}.jpg")
                report["transitions"].append({"open": is_open, "language": language,
                                              "selection": selected})
        setprop("/sim/sw233/language", "invalid")
        verify("fr")
        run('sw233_language.choose("invalid");')
        verify("fr")
        report["invalid_language_falls_back_to_fr"] = True
        report["invalid_choose_ignored"] = True
        report["controls_before"] = controls
        report["controls_after"] = {p: get(p) for p in control_paths}
        assert report["controls_before"] == report["controls_after"]
    finally:
        close()
        run(f'sw233_language.choose("{saved_language}");')
        if saved_selection is not None:
            setprop("/sim/gui/dialogs/checklist/selected-checklist", saved_selection)
        setprop("/sim/gui/dialogs/checklist/selected-page", 0)
        if initially_open:
            run('gui.showDialog("checklist");')
    assert opened() == initially_open
    if initially_open:
        assert get("/sim/gui/dialogs/checklist/selected-page") == 0
        assert get("/sim/gui/dialogs/checklist/selected-checklist") == saved_selection
    report["restoration_verified"] = True
    report["utf8_originals_preserved"] = True
    (output / "checks.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                       encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    capture(args.output, args.port)
