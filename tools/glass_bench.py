"""Paired glass comparisons with every visited camera restored in SW233 null FDM."""
import argparse
import hashlib
import io
import json
import statistics
import time
from pathlib import Path
from urllib.request import urlopen

from PIL import Image, ImageChops, ImageStat

from tools.flightgear import execute

VIEW = '/sim/current-view/'
CAMERA_KEYS = tuple(VIEW + p for p in
                    ('heading-offset-deg', 'pitch-offset-deg', 'field-of-view'))
VIEWS = {'pilote': (0, 0, -18, 65), 'oblique': (0, 70, 0, 75),
         'exterieur': (1, 140, 15, 25)}
STRENGTHS = {'sans': (0, 0), 'fort': (1, 1), 'regle': (.25, .12)}
VISUAL = '/sim/sw233/visuals/'
OPTIONS = (VISUAL + 'canopy-reflection', VISUAL + 'instrument-reflection',
           '/sim/menubar/visibility', '/sim/freeze/master', '/orientation/heading-deg')


class Session:
    def __init__(self, port):
        self.port = port
        self.base = f'http://127.0.0.1:{port}'

    def get(self, path):
        with urlopen(self.base + '/json' + path, timeout=15) as response:
            return json.load(response).get('value')

    def put(self, path, value):
        value = int(value) if isinstance(value, bool) else value
        execute(f'setprop({json.dumps(path)},{json.dumps(value)});', self.port)

    def screenshot(self):
        with urlopen(self.base + '/screenshot?type=jpg', timeout=30) as response:
            return response.read()


def capture(output, port, repeats=3, interval=1.0, session=None):
    if repeats < 2 or interval <= 0:
        raise ValueError('Use at least two paired repetitions and a positive interval')
    fg = session if session is not None else Session(port)
    if fg.get('/sim/aircraft') != 'sw233' or fg.get('/sim/flight-model') != 'null':
        raise ValueError('Dedicated SW233 --fdm=null session required')

    def read(keys):
        result = {p: fg.get(p) for p in keys}
        if any(v is None for v in result.values()):
            raise ValueError(f'Required property missing: {result}')
        return result

    saved = read(OPTIONS)
    original_view = fg.get(VIEW + 'view-number')
    if original_view is None:
        raise ValueError('Missing current view')
    cameras = {original_view: read(CAMERA_KEYS)}
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    report = dict(version=fg.get('/sim/version/flightgear'),
                  aircraft_dir=fg.get('/sim/aircraft-dir'),
                  skydome_shader=fg.get('/sim/rendering/shaders/skydome'),
                  vsync_enable=fg.get('/sim/rendering/vsync-enable'),
                  scope='Static fair-sky cubemap; heading 010/190, not measured sun azimuth',
                  fps_method='Frame counter difference / monotonic elapsed seconds; paired '
                             'repetitions with alternating state order, not GPU timing',
                  interval_seconds=interval, repeats=repeats, samples=[], comparisons=[],
                  initial_properties=saved, original_view=original_view)
    errors = []
    try:
        fg.put('/sim/freeze/master', 1)
        fg.put('/sim/menubar/visibility', 0)
        for heading in (10, 190):
            fg.put('/orientation/heading-deg', heading)
            for name, camera in VIEWS.items():
                fg.put(VIEW + 'view-number', camera[0])
                if camera[0] not in cameras:
                    cameras[camera[0]] = read(CAMERA_KEYS)
                for p, value in zip(CAMERA_KEYS, camera[1:]):
                    fg.put(p, value)
                frames = {}
                pairs = []
                for repeat in range(repeats):
                    rates = {}
                    order = list(STRENGTHS)
                    if repeat % 2:
                        order.reverse()
                    for state in order:
                        for p, value in zip(OPTIONS[:2], STRENGTHS[state]):
                            fg.put(p, value)
                        time.sleep(.6)
                        actual = read((OPTIONS[0], OPTIONS[1], OPTIONS[-1], *CAMERA_KEYS))
                        desired = dict(zip(OPTIONS[:2], STRENGTHS[state]))
                        desired[OPTIONS[-1]] = heading
                        desired.update(zip(CAMERA_KEYS, camera[1:]))
                        if actual != desired:
                            raise RuntimeError(f'Comparison settings not applied: {actual}')
                        first = fg.get('/sim/frame-number')
                        start = time.monotonic()
                        time.sleep(interval)
                        last = fg.get('/sim/frame-number')
                        elapsed = time.monotonic() - start
                        if (not isinstance(first, (int, float))
                                or not isinstance(last, (int, float))):
                            raise ValueError('Frame counter unavailable')
                        if last <= first or elapsed <= 0:
                            raise ValueError('Frame counter did not advance')
                        rates[state] = (last - first) / elapsed
                        sample = dict(heading=heading, view=name, state=state, repeat=repeat,
                                      fps=rates[state], frames=last-first, elapsed_seconds=elapsed,
                                      frame_rate_property=fg.get('/sim/frame-rate'),
                                      settings=actual)
                        if repeat == 0:
                            data = fg.screenshot()
                            with Image.open(io.BytesIO(data)) as raw:
                                if raw.width < 1024 or raw.height < 600:
                                    raise ValueError('Restore simulator window before capture')
                                frames[state] = raw.convert('RGB')
                            filename = f'h{heading:03d}-{name}-{state}.jpg'
                            (output / filename).write_bytes(data)
                            sample.update(screenshot=filename,
                                          sha256=hashlib.sha256(data).hexdigest())
                        report['samples'].append(sample)
                    pairs.append(dict(repeat=repeat, fps=rates,
                                      strong_minus_off=rates['fort']-rates['sans'],
                                      tuned_minus_off=rates['regle']-rates['sans']))
                difference = ImageChops.difference(frames['sans'], frames['fort'])
                report['comparisons'].append(dict(
                    heading=heading, view=name, camera=camera, paired_rates=pairs,
                    median_strong_minus_off=statistics.median(p['strong_minus_off'] for p in pairs),
                    median_tuned_minus_off=statistics.median(p['tuned_minus_off'] for p in pairs),
                    mean_rgb_difference_0_to_1=ImageStat.Stat(difference).mean))
    except Exception as exc:
        report['error'] = str(exc)
        raise
    finally:
        def restore(path, value):
            try:
                fg.put(path, value)
                if fg.get(path) != value:
                    errors.append(f'Not restored: {path}')
            except Exception as exc:
                errors.append(f'{path}: {exc}')

        for number, values in cameras.items():
            restore(VIEW + 'view-number', number)
            for p, value in values.items():
                restore(p, value)
        restore(VIEW + 'view-number', original_view)
        for p, value in saved.items():
            restore(p, value)
        # A view switch may reset offsets, so restore the original camera last.
        for p, value in cameras[original_view].items():
            restore(p, value)
        report.update(saved_cameras=cameras, restoration_errors=errors, restored=not errors)
        (output / 'checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        if errors:
            raise RuntimeError('Restoration incomplete; inspect checks.json: ' + '; '.join(errors))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--interval', type=float, default=1.0)
    args = parser.parse_args()
    capture(args.output, args.port, args.repeats, args.interval)
