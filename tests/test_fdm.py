"""Behavioral smoke tests, not manufacturer performance acceptance tests."""

import math
import unittest

from tools.glide import aircraft, simulate, trim_glide


class FlightDynamicsTests(unittest.TestCase):
    def test_stabilized_descent_for_sixty_seconds(self):
        result = simulate()
        self.assertAlmostEqual(result["weight_lbs"], 970, places=5)
        self.assertLess(abs(result["final_speed_kts"] - 50), 1)
        self.assertLess(result["final_altitude_ft"], 4900)
        self.assertGreater(result["final_altitude_ft"], 4000)
        self.assertTrue(-1 < result["elevator_norm"] < 1)

    def test_airbrakes_increase_drag_and_reduce_lift(self):
        fdm = aircraft()
        trim_glide(fdm)
        clean_cd = fdm["aero/sw233/CD"]
        clean_cl = fdm["aero/sw233/CL"]
        fdm["fcs/speedbrake-cmd-norm"] = 1
        fdm.run_ic()
        self.assertGreater(fdm["aero/sw233/CD"], clean_cd)
        self.assertLess(fdm["aero/sw233/CL"], clean_cl)

    def test_elevator_roll_and_yaw_signs(self):
        cases = (
            ("fcs/elevator-cmd-norm", "aero/sw233/Cm", -1),
            ("fcs/aileron-cmd-norm", "aero/sw233/Cl", 1),
            ("fcs/rudder-cmd-norm", "aero/sw233/Cn", -1),
        )
        for command, output, sign in cases:
            with self.subTest(command=command):
                fdm = aircraft()
                trim_glide(fdm)
                fdm[command] = -0.2
                fdm.run_ic()
                negative = fdm[output]
                fdm[command] = 0.2
                fdm.run_ic()
                self.assertGreater(sign * (fdm[output] - negative), 0)

    def test_input_saturation(self):
        fdm = aircraft()
        trim_glide(fdm)
        for demand in (-5, 5):
            fdm["fcs/elevator-cmd-norm"] = demand
            fdm["fcs/aileron-cmd-norm"] = demand
            fdm["fcs/speedbrake-cmd-norm"] = demand
            fdm.run_ic()
            self.assertLessEqual(abs(fdm["fcs/elevator-pos-rad"]), math.radians(23))
            self.assertLessEqual(abs(fdm["fcs/left-aileron-pos-rad"]), 0.35)
            self.assertTrue(0 <= fdm["fcs/speedbrake-pos-norm"] <= 1)

    def test_stationary_ground_contact_remains_finite(self):
        fdm = aircraft()
        fdm["ic/h-agl-ft"] = 4.2
        fdm["ic/vc-kts"] = 0
        self.assertTrue(fdm.run_ic())
        for _ in range(1200):
            self.assertTrue(fdm.run())
        self.assertTrue(math.isfinite(fdm["position/h-agl-ft"]))
        self.assertGreater(fdm["position/h-agl-ft"], 0)
        self.assertLess(fdm["position/h-agl-ft"], 10)


if __name__ == "__main__":
    unittest.main()
