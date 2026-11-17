"""Exercise restoration and paired measurements without touching FlightGear."""
import copy
import io
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

from tools.glass_bench import CAMERA_KEYS, OPTIONS, VIEW, capture


class FakeSession:
    def __init__(self, fail_screenshot=None):
        self.view = 2
        self.cameras = {n: dict(zip(CAMERA_KEYS, (n*13+2, n*3-9, n+71)))
                        for n in (0, 1, 2)}
        self.values = dict(zip(OPTIONS, (.31, .17, True, False, 87)))
        self.values.update({'/sim/aircraft': 'sw233', '/sim/flight-model': 'null',
                            '/sim/frame-rate': 0, '/sim/rendering/vsync-enable': False})
        self.initial_values = copy.deepcopy(self.values)
        self.initial_cameras = copy.deepcopy(self.cameras)
        self.frame = 0
        self.count = 0
        self.fail_screenshot = fail_screenshot
        self.writes = []
        buf = io.BytesIO()
        Image.new('RGB', (1024, 600), 'gray').save(buf, format='JPEG')
        self.image = buf.getvalue()

    def get(self, path):
        if path == VIEW + 'view-number':
            return self.view
        if path in CAMERA_KEYS:
            return self.cameras[self.view][path]
        if path == '/sim/frame-number':
            self.frame += 60
            return self.frame
        return self.values.get(path)

    def put(self, path, value):
        self.writes.append((path, value))
        if path == VIEW + 'view-number':
            self.view = value
        elif path in CAMERA_KEYS:
            self.cameras[self.view][path] = value
        else:
            self.values[path] = value

    def screenshot(self):
        self.count += 1
        if self.count == self.fail_screenshot:
            raise OSError('capture failed')
        return self.image


class GlassBenchTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='SW233 glass test ')
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'captures'
        sleeper = patch('tools.glass_bench.time.sleep')
        clock = patch('tools.glass_bench.time.monotonic', side_effect=iter(range(1000)))
        sleeper.start()
        clock.start()
        self.addCleanup(sleeper.stop)
        self.addCleanup(clock.stop)

    def assert_restored(self, session):
        self.assertEqual(session.view, 2)
        self.assertEqual(session.values, session.initial_values)
        self.assertEqual(session.cameras, session.initial_cameras)

    def test_full_matrix_paired_samples_and_all_cameras_restored(self):
        session = FakeSession()
        report = capture(self.output, 0, repeats=2, session=session)
        self.assert_restored(session)
        self.assertTrue(report['restored'])
        self.assertEqual(len(list(self.output.glob('*.jpg'))), 18)
        self.assertEqual(len(report['samples']), 36)
        self.assertEqual(len(report['comparisons']), 6)
        self.assertTrue(all(s['fps'] == 60 for s in report['samples']))
        self.assertEqual([s['state'] for s in report['samples'][:6]],
                         ['sans', 'fort', 'regle', 'regle', 'fort', 'sans'])
        self.assertEqual({s['heading'] for s in report['samples']}, {10, 190})
        self.assertTrue(all(c['median_tuned_minus_off'] == 0 for c in report['comparisons']))

    def test_exception_after_exterior_visit_restores_every_view(self):
        session = FakeSession(fail_screenshot=7)
        with self.assertRaisesRegex(OSError, 'capture failed'):
            capture(self.output, 0, repeats=2, session=session)
        self.assert_restored(session)
        report = json.loads((self.output / 'checks.json').read_text())
        self.assertTrue(report['restored'])
        self.assertEqual(set(report['saved_cameras']), {'0', '1', '2'})
        self.assertIn('capture failed', report['error'])

    def test_rejects_flight_session_before_any_write(self):
        for aircraft, model in [('other', 'null'), ('sw233', 'jsb')]:
            with self.subTest(aircraft=aircraft, model=model):
                session = FakeSession()
                session.values['/sim/aircraft'] = aircraft
                session.values['/sim/flight-model'] = model
                with self.assertRaisesRegex(ValueError, 'Dedicated'):
                    capture(self.output, 0, session=session)
                self.assertFalse(session.writes)
                self.assertFalse(self.output.exists())

    def test_failed_restore_is_reported_without_skipping_other_properties(self):
        session = FakeSession(fail_screenshot=7)
        original_put = session.put

        def fail_restore(path, value):
            if path == OPTIONS[0] and value == session.initial_values[path]:
                raise OSError('restore refused')
            original_put(path, value)

        session.put = fail_restore
        with self.assertRaisesRegex(RuntimeError, 'Restoration incomplete'):
            capture(self.output, 0, repeats=2, session=session)
        report = json.loads((self.output / 'checks.json').read_text())
        self.assertFalse(report['restored'])
        self.assertEqual(session.view, 2)
        self.assertEqual(session.cameras, session.initial_cameras)
        for path in OPTIONS[1:]:
            self.assertEqual(session.values[path], session.initial_values[path])


if __name__ == '__main__':
    unittest.main()
