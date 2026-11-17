"""Native presentation restoration under view resets and transport failures."""
import copy
import io
import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

from tools.visual_demo import BRAKE, CAMERA, VIEW, record


class DemoSession:
    def __init__(self, fail_frame=None, fail_restore=False):
        self.view = 0
        self.cameras = {0: dict(zip(CAMERA, (17, -3, 83, 1.8))),
                        1: dict(zip(CAMERA, (29, 14, 51, -37)))}
        self.defaults = dict(zip(CAMERA, (0, -18, 80, 1.65)))
        self.properties = {'/sim/aircraft': 'sw233', '/sim/flight-model': 'null',
                           '/sim/menubar/visibility': True, '/sim/freeze/master': False,
                           BRAKE: .2, '/sim/sw233/visuals/uv-grid': True}
        self.initial = copy.deepcopy((self.cameras, self.properties))
        self.fail_frame = fail_frame
        self.fail_restore = fail_restore
        self.frames = 0
        self.observed_cameras = []
        buf = io.BytesIO()
        Image.new('RGB', (1024, 600), 'gray').save(buf, format='JPEG')
        self.jpeg = buf.getvalue()

    def urlopen(self, url, **kwargs):
        if '/screenshot?' in url:
            self.frames += 1
            if self.frames == self.fail_frame:
                raise OSError('screenshot unavailable')
            self.observed_cameras.append((self.view, copy.deepcopy(self.cameras[self.view])))
            return io.BytesIO(self.jpeg)
        path = url.split('/json', 1)[1]
        if path == VIEW+'view-number':
            value = self.view
        elif path in CAMERA:
            value = self.cameras[self.view][path]
        else:
            value = self.properties.get(path)
        return io.BytesIO(json.dumps({'value': value}).encode())

    def execute(self, script, port):
        for raw_path, raw_value in re.findall(r'setprop\(("[^"]+"),(.*?)\);', script):
            path, value = json.loads(raw_path), json.loads(raw_value)
            if self.fail_restore and path == '/sim/freeze/master' and value == 0:
                raise OSError('freeze restore failed')
            if path == VIEW+'view-number':
                self.view = value
                if value == 0:
                    self.cameras[0] = copy.deepcopy(self.defaults)
            elif path in CAMERA:
                self.cameras[self.view][path] = value
            else:
                self.properties[path] = value


class VisualDemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='SW233 demo test ')
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)/'frames'

    def run_record(self, session):
        with patch('tools.visual_demo.urlopen', session.urlopen), \
                patch('tools.visual_demo.execute', session.execute), \
                patch('tools.visual_demo.time.sleep'):
            return record(self.folder, 0, fps=1, seconds=1)

    def test_initial_transient_camera_restored_after_final_switch(self):
        session = DemoSession()
        report = self.run_record(session)
        self.assertTrue(report['restored'])
        self.assertEqual(session.view, 0)
        self.assertEqual((session.cameras, session.properties), session.initial)
        self.assertEqual(len(report['frames']), 7)
        for view, camera in session.observed_cameras:
            self.assertEqual(camera[CAMERA[3]], -25 if view == 1 else 1.65)
        self.assertEqual(session.observed_cameras[1][1][CAMERA[1]], 10)

    def test_capture_exception_restores_both_cameras_and_reports_error(self):
        session = DemoSession(fail_frame=4)
        with self.assertRaisesRegex(OSError, 'screenshot unavailable'):
            self.run_record(session)
        self.assertEqual((session.cameras, session.properties), session.initial)
        report = json.loads((self.folder/'record.json').read_text())
        self.assertTrue(report['restored'])
        self.assertEqual(report['error'], 'screenshot unavailable')

    def test_restore_failure_does_not_skip_later_properties_or_report(self):
        session = DemoSession(fail_frame=4, fail_restore=True)
        with self.assertRaisesRegex(RuntimeError, 'Incomplete restoration'):
            self.run_record(session)
        report = json.loads((self.folder/'record.json').read_text())
        self.assertFalse(report['restored'])
        self.assertTrue(any('freeze restore failed' in e for e in report['restoration_errors']))
        self.assertEqual(session.cameras, session.initial[0])
        self.assertEqual(session.properties[BRAKE], .2)
        self.assertTrue(session.properties['/sim/sw233/visuals/uv-grid'])
        self.assertEqual(session.view, 0)


if __name__ == '__main__':
    unittest.main()
