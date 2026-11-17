"""Record native crew/livery evidence in a dedicated SW233 null-FDM session."""
import argparse
import hashlib
import io
import json
import statistics
import time
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

from tools.flightgear import execute

VIEW = '/sim/current-view/'
CAMERA = [VIEW + name for name in
          ('heading-offset-deg', 'pitch-offset-deg', 'field-of-view')]
FRONT = '/fdm/jsbsim/inertia/pointmass-weight-lbs'
REAR = FRONT + '[1]'
CREW = '/sim/sw233/visuals/crew'
LIVERY = '/sim/sw233/visuals/livery'
WINGS = '/sim/sw233/visuals/wings'
STATES = {
    'no-crew': (False, True, False, 180, 180),
    'both': (True, True, False, 180, 180),
    'front-only': (True, True, False, 180, 0),
    'rear-only': (True, True, False, 0, 180),
    'wings': (True, True, True, 180, 180),
    'livery-off': (True, False, False, 180, 180),
}


def capture(output, port=18142, samples=8, interval=1.0,
            heading=120, pitch=15, fov=30):
    if samples < 2 or interval <= 0:
        raise ValueError('At least two FPS samples and a positive interval are required')
    base = f'http://127.0.0.1:{port}'

    def get(path):
        with urlopen(base + '/json' + path, timeout=15) as response:
            return json.load(response).get('value')

    def set_values(values):
        normalized = {p: int(v) if isinstance(v, bool) else v for p, v in values.items()}
        script = "".join(f"setprop({json.dumps(p)},{json.dumps(v)});"
                         for p, v in normalized.items())
        execute(script, port)

    def read_values(paths):
        values = {p: get(p) for p in paths}
        if any(v is None for v in values.values()):
            raise ValueError(f'Required properties missing: {values}')
        return values

    if get('/sim/aircraft') != 'sw233' or get('/sim/flight-model') != 'null':
        raise ValueError('Dedicated SW233 null-FDM session required; no flight session is modified')
    settings = [CREW, LIVERY, WINGS, FRONT, REAR, '/sim/freeze/master',
                '/sim/menubar/visibility']
    saved = read_values(settings)
    original_view = read_values([VIEW + 'view-number', *CAMERA])
    evidence = dict(
        aircraft=get('/sim/aircraft'), flight_model=get('/sim/flight-model'),
        aircraft_dir=get('/sim/aircraft-dir'), version=get('/sim/version/flightgear'),
        purpose='Native visual evidence only; null FDM cannot validate weight or flight dynamics',
        fps_note='Sequential samples; paused scene, camera and graphics settings held fixed. '
                 'Not a hardware-independent performance benchmark.',
        initial_properties=saved, initial_camera=original_view, states={},
    )
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    exterior_saved = None
    restoration_errors = []
    try:
        set_values({'/sim/freeze/master': True, '/sim/menubar/visibility': False})
        set_values({VIEW + 'view-number': 1})
        exterior_saved = read_values(CAMERA)
        set_values(dict(zip(CAMERA, (heading, pitch, fov))))
        evidence['camera'] = read_values([VIEW + 'view-number', *CAMERA])
        for name, state in STATES.items():
            desired = dict(zip((CREW, LIVERY, WINGS, FRONT, REAR), state))
            set_values(desired)
            time.sleep(1)
            actual = read_values(desired)
            if actual != desired:
                raise RuntimeError(f'Property update failed for {name}: {actual}')
            rates = []
            raw_rates = []
            previous_frame = get('/sim/frame-number')
            previous_time = time.monotonic()
            for _ in range(samples):
                time.sleep(interval)
                rate = get('/sim/frame-rate')
                frame_number = get('/sim/frame-number')
                sampled_time = time.monotonic()
                if (not isinstance(frame_number, (float, int))
                        or not isinstance(previous_frame, (float, int))
                        or frame_number <= previous_frame):
                    raise ValueError(
                        f'Frame counter did not advance: {previous_frame}, {frame_number}')
                rates.append((frame_number - previous_frame) / (sampled_time - previous_time))
                raw_rates.append(rate)
                previous_frame, previous_time = frame_number, sampled_time
            with urlopen(base + '/screenshot?type=jpg', timeout=20) as response:
                content = response.read()
            with Image.open(io.BytesIO(content)) as frame:
                if frame.width < 1024 or frame.height < 600:
                    raise ValueError('Restore FlightGear window before capturing')
                dimensions = list(frame.size)
                frame.verify()
            (output / f'{name}.jpg').write_bytes(content)
            evidence['states'][name] = dict(
                properties=actual, expected_visibility=dict(
                    front=bool(state[0] and state[3] > 0),
                    rear=bool(state[0] and state[4] > 0),
                    wings=bool(state[0] and state[2]), livery=state[1]),
                screenshot=f'{name}.jpg', dimensions=dimensions,
                sha256=hashlib.sha256(content).hexdigest(), fps_samples=rates,
                fps_method='delta /sim/frame-number divided by monotonic elapsed seconds',
                frame_rate_property_samples=raw_rates,
                fps_median=statistics.median(rates), fps_min=min(rates), fps_max=max(rates))
        baseline = evidence['states']['no-crew']['fps_median']
        for state in evidence['states'].values():
            state['fps_delta_from_no_crew'] = state['fps_median'] - baseline
        evidence['visibility_note'] = (
            'Expected visibility follows XML conditions; inspect images '
            'to confirm rendering, placement and occlusion.')
    except Exception as exc:
        evidence['error'] = str(exc)
        raise
    finally:
        # Each step is attempted independently so a failed camera operation does not
        # prevent restoring masses or visibility. Restore view-specific offsets first.
        restores = []
        if exterior_saved is not None:
            restores.append(exterior_saved)
        restores.extend([{VIEW + 'view-number': original_view[VIEW + 'view-number']},
                         {p: original_view[p] for p in CAMERA}, saved])
        for values in restores:
            try:
                set_values(values)
                actual = read_values(values)
                if actual != values:
                    restoration_errors.append(f'Expected {values}, observed {actual}')
            except Exception as exc:
                restoration_errors.append(str(exc))
        evidence['restored'] = not restoration_errors
        evidence['restoration_errors'] = restoration_errors
        (output / 'capture.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
        if restoration_errors:
            raise RuntimeError('Session restoration incomplete; inspect capture.json: '
                               + '; '.join(restoration_errors))
    return evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--port', type=int, default=18142)
    parser.add_argument('--samples', type=int, default=8)
    parser.add_argument('--interval', type=float, default=1.0)
    parser.add_argument('--heading', type=float, default=120)
    parser.add_argument('--pitch', type=float, default=15)
    parser.add_argument('--fov', type=float, default=30)
    args = parser.parse_args()
    capture(args.output, args.port, args.samples, args.interval,
            args.heading, args.pitch, args.fov)
