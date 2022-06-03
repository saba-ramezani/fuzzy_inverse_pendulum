# -*- coding: utf-8 -*-

# python imports
from math import degrees

import matplotlib.pyplot as plt

import numpy as np


# pyfuzzy imports
# from fuzzy.storage.fcl.Reader import Reader


class FuzzyController:

    def __init__(self):
        pass
        # self.system = Reader().load_from_file(fcl_path)

    def _make_input(self, world):
        return dict(
            cp=world.x,
            cv=world.v,
            pa=degrees(world.theta),
            pv=degrees(world.omega)
        )

    def _make_output(self):
        return dict(
            force=0.
        )

    def decide(self, world):
        output = self._make_output()
        inp = self._make_input(world)
        x, force = self.combined_force(inp)
        print inp['pa']
        print inp['pv']
        final_force = self.defuzzification(x, force)
        output['force'] = final_force
        return output['force']

    def line_y_output(self, x1, y1, x2, y2, x_in):
        a = (y2 - y1) / float(x2 - x1)  # calculate the slope of the line
        y_out = a * (x_in - x2) + y2
        return y_out

    def pv_membership(self, x):
        pv = dict()
        # pv_cw_fast
        if x <= -200:
            pv['pv_cw_fast'] = 1
        elif x < -100:
            pv['pv_cw_fast'] = self.line_y_output(-200, 1, -100, 0, x)
        else:
            pv['pv_cw_fast'] = 0
        # pv_cw_slow
        if x < -200:
            pv['pv_cw_slow'] = 0
        elif -200 < x < -100:
            pv['pv_cw_slow'] = self.line_y_output(-200, 0, -100, 1, x)
        elif x <= 0:
            pv['pv_cw_slow'] = self.line_y_output(-100, 1, 0, 0, x)
        else:
            pv['pv_cw_slow'] = 0
        # pv_stop
        if x < -100:
            pv['pv_stop'] = 0
        elif -100 < x < 0:
            pv['pv_stop'] = self.line_y_output(-100, 0, 0, 1, x)
        elif x <= 100:
            pv['pv_stop'] = self.line_y_output(0, 1, 100, 0, x)
        else:
            pv['pv_stop'] = 0
        # pv_ccw_slow
        if x < 0:
            pv['pv_ccw_slow'] = 0
        elif 0 < x < 100:
            pv['pv_ccw_slow'] = self.line_y_output(0, 0, 100, 1, x)
        elif x <= 200:
            pv['pv_ccw_slow'] = self.line_y_output(200, 0, 100, 1, x)
        else:
            pv['pv_ccw_slow'] = 0
        # pv_ccw_fast
        if x <= 100:
            pv['pv_ccw_fast'] = 0
        elif x < 200:
            pv['pv_ccw_fast'] = self.line_y_output(200, 1, 100, 0, x)
        else:
            pv['pv_ccw_fast'] = 1
        return pv

    def pa_membership(self, x):
        pa = dict()
        # pa_up_more_right
        if x < 0:
            pa['pa_up_more_right'] = 0
        elif 0 < x < 30:
            pa['pa_up_more_right'] = self.line_y_output(0, 0, 30, 1, x)
        elif x < 60:
            pa['pa_up_more_right'] = self.line_y_output(30, 1, 60, 0, x)
        else:
            pa['pa_up_more_right'] = 0
        # pa_up_right
        if x < 30:
            pa['pa_up_right'] = 0
        elif 30 < x < 60:
            pa['pa_up_right'] = self.line_y_output(30, 0, 60, 1, x)
        elif x < 90:
            pa['pa_up_right'] = self.line_y_output(60, 1, 90, 0, x)
        else:
            pa['pa_up_right'] = 0
        # pa_up
        if x < 60:
            pa['pa_up'] = 0
        elif 60 < x < 90:
            pa['pa_up'] = self.line_y_output(60, 0, 90, 1, x)
        elif x < 120:
            pa['pa_up'] = self.line_y_output(90, 1, 120, 0, x)
        else:
            pa['pa_up'] = 0
        # pa_up_left
        if x < 90:
            pa['pa_up_left'] = 0
        elif 90 < x < 120:
            pa['pa_up_left'] = self.line_y_output(90, 0, 120, 1, x)
        elif x < 150:
            pa['pa_up_left'] = self.line_y_output(120, 1, 150, 0, x)
        else:
            pa['pa_up_left'] = 0
        # pa_up_more_left
        if x < 120:
            pa['pa_up_more_left'] = 0
        elif 120 < x < 150:
            pa['pa_up_more_left'] = self.line_y_output(120, 0, 150, 1, x)
        elif x < 180:
            pa['pa_up_more_left'] = self.line_y_output(150, 1, 180, 0, x)
        else:
            pa['pa_up_more_left'] = 0
        # pa_down_more_left
        if x < 180:
            pa['pa_down_more_left'] = 0
        elif 180 < x < 210:
            pa['pa_down_more_left'] = self.line_y_output(180, 0, 210, 1, x)
        elif x < 240:
            pa['pa_down_more_left'] = self.line_y_output(210, 1, 240, 0, x)
        else:
            pa['pa_down_more_left'] = 0
        # pa_down_left
        if x < 210:
            pa['pa_down_left'] = 0
        elif 210 < x < 240:
            pa['pa_down_left'] = self.line_y_output(210, 0, 240, 1, x)
        elif x < 270:
            pa['pa_down_left'] = self.line_y_output(240, 1, 270, 0, x)
        else:
            pa['pa_down_left'] = 0
        # pa_down
        if x < 240:
            pa['pa_down'] = 0
        elif 240 < x < 270:
            pa['pa_down'] = self.line_y_output(240, 0, 270, 1, x)
        elif x < 300:
            pa['pa_down'] = self.line_y_output(270, 1, 300, 0, x)
        else:
            pa['pa_down'] = 0
        # pa_down_right
        if x < 270:
            pa['pa_down_right'] = 0
        elif 270 < x < 300:
            pa['pa_down_right'] = self.line_y_output(270, 0, 300, 1, x)
        elif x < 330:
            pa['pa_down_right'] = self.line_y_output(300, 1, 330, 0, x)
        else:
            pa['pa_down_right'] = 0
        # pa_down_more_right
        if x < 300:
            pa['pa_down_more_right'] = 0
        elif 300 < x < 330:
            pa['pa_down_more_right'] = self.line_y_output(300, 0, 330, 1, x)
        elif x < 360:
            pa['pa_down_more_right'] = self.line_y_output(330, 1, 360, 0, x)
        else:
            pa['pa_down_more_right'] = 0
        return pa

    def force_membership(self, x):
        force = dict()
        # force_left_fast
        if x < -100:
            force['force_left_fast'] = 0
        elif -100 < x < -80:
            force['force_left_fast'] = self.line_y_output(-100, 0, -80, 1, x)
        elif x < -60:
            force['force_left_fast'] = self.line_y_output(-80, 1, -60, 0, x)
        else:
            force['force_left_fast'] = 0
        # force_left_slow
        if x < -80:
            force['force_left_slow'] = 0
        elif -80 < x < -60:
            force['force_left_slow'] = self.line_y_output(-80, 0, -60, 1, x)
        elif x < 0:
            force['force_left_slow'] = self.line_y_output(-60, 1, 0, 0, x)
        else:
            force['force_left_slow'] = 0
        # force_stop
        if x < -60:
            force['force_stop'] = 0
        elif -60 < x < 0:
            force['force_stop'] = self.line_y_output(-60, 0, 0, 1, x)
        elif x < 60:
            force['force_stop'] = self.line_y_output(0, 1, 60, 0, x)
        else:
            force['force_stop'] = 0
        # force_right_slow
        if x < 0:
            force['force_right_slow'] = 0
        elif 0 < x < 60:
            force['force_right_slow'] = self.line_y_output(0, 0, 60, 1, x)
        elif x < 80:
            force['force_right_slow'] = self.line_y_output(60, 1, 80, 0, x)
        else:
            force['force_right_slow'] = 0
        # force_right_fast
        if x < 60:
            force['force_right_fast'] = 0
        elif 60 < x < 80:
            force['force_right_fast'] = self.line_y_output(60, 0, 80, 1, x)
        elif x < 100:
            force['force_right_fast'] = self.line_y_output(80, 1, 100, 0, x)
        else:
            force['force_right_fast'] = 0
        return force

    def inference(self, pa_in, pv_in):
        max_force = dict()
        # if pa < 0:
        # pa = -pa
        pa = self.pa_membership(pa_in)
        pv = self.pv_membership(pv_in)

        # force_right_fast
        # RULE 1: IF (pa IS up_more_right) AND (pv IS ccw_slow) THEN force IS right_fast
        f1 = min(pa['pa_up_more_right'], pv['pv_ccw_slow'])
        # RULE 2: IF (pa IS up_more_right) AND (pv IS cw_slow) THEN force IS right_fast
        f2 = min(pa['pa_up_more_right'], pv['pv_cw_slow'])
        # RULE 6: IF (pa IS up_more_right) AND (pv IS cw_fast) THEN force IS right_fast
        f3 = min(pa['pa_up_more_right'], pv['pv_cw_fast'])
        # RULE 9: IF (pa IS down_more_right) AND (pv IS ccw_slow) THEN force IS right_fast
        f4 = min(pa['pa_down_more_right'], pv['pv_ccw_slow'])
        # RULE 17: IF (pa IS down_right) AND (pv IS ccw_slow) THEN force IS right_fast
        f5 = min(pa['pa_down_right'], pv['pv_ccw_slow'])
        # RULE 18: IF (pa IS down_right) AND (pv IS cw_slow) THEN force IS right_fast
        f6 = min(pa['pa_down_right'], pv['pv_cw_slow'])
        # RULE 26: IF (pa IS up_right) AND (pv IS cw_slow) THEN force IS right_fast
        f7 = min(pa['pa_up_right'], pv['pv_cw_slow'])
        # RULE 27: IF (pa IS up_right) AND (pv IS stop) THEN force IS right_fast
        f8 = min(pa['pa_up_right'], pv['pv_stop'])
        # RULE 32: IF (pa IS up_right) AND (pv IS cw_fast) THEN force IS right_fast
        f9 = min(pa['pa_up_right'], pv['pv_cw_fast'])
        # RULE 33: IF (pa IS up_left) AND (pv IS cw_fast) THEN force IS right_fast
        f10 = min(pa['pa_up_left'], pv['pv_cw_fast'])
        # RULE 35: IF (pa IS down) AND (pv IS stop) THEN force IS right_fast
        f11 = min(pa['pa_down'], pv['pv_stop'])
        # RULE 41: IF (pa IS up) AND (pv IS cw_fast) THEN force IS right_fast
        f12 = min(pa['pa_up'], pv['pv_cw_fast'])
        max_force['force_right_fast'] = max(f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12)

        # force_left_fast
        # RULE 3: IF (pa IS up_more_left) AND (pv IS cw_slow) THEN force IS left_fast
        f1 = min(pa['pa_up_more_left'], pv['pv_cw_slow'])
        # RULE 4: IF (pa IS up_more_left) AND (pv IS ccw_slow) THEN force IS left_fast
        f2 = min(pa['pa_up_more_left'], pv['pv_ccw_slow'])
        # RULE 8: IF (pa IS up_more_left) AND (pv IS ccw_fast) THEN force IS left_fast
        f3 = min(pa['pa_up_more_left'], pv['pv_ccw_fast'])
        # RULE 11: IF (pa IS down_more_left) AND (pv IS cw_slow) THEN force IS left_fast
        f4 = min(pa['pa_down_more_left'], pv['pv_cw_slow'])
        # RULE 19: IF (pa IS down_left) AND (pv IS cw_slow) THEN force IS left_fast
        f5 = min(pa['pa_down_left'], pv['pv_cw_slow'])
        # RULE 20: IF (pa IS down_left) AND (pv IS ccw_slow) THEN force IS left_fast
        f6 = min(pa['pa_down_left'], pv['pv_ccw_slow'])
        # RULE 29: IF (pa IS up_left) AND (pv IS ccw_slow) THEN force IS left_fast
        f7 = min(pa['pa_up_left'], pv['pv_ccw_slow'])
        # RULE 30: IF (pa IS up_left) AND (pv IS stop) THEN force IS left_fast
        f8 = min(pa['pa_up_left'], pv['pv_stop'])
        # RULE 31: IF (pa IS up_right) AND (pv IS ccw_fast) THEN force IS left_fast
        f9 = min(pa['pa_up_right'], pv['pv_ccw_fast'])
        # RULE 34: IF (pa IS up_left) AND (pv IS ccw_fast) THEN force IS left_fast
        f10 = min(pa['pa_up_left'], pv['pv_ccw_fast'])
        # RULE 39: IF (pa IS up) AND (pv IS ccw_fast) THEN force IS left_fast
        f11 = min(pa['pa_up'], pv['pv_ccw_fast'])
        max_force['force_left_fast'] = max(f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11)

        # force_left_slow
        # RULE 5: IF (pa IS up_more_right) AND (pv IS ccw_fast) THEN force IS left_slow
        f1 = min(pa['pa_up_more_right'], pv['pv_ccw_fast'])
        # RULE 24: IF (pa IS down_left) AND (pv IS ccw_fast) THEN force IS left_slow
        f2 = min(pa['pa_down_left'], pv['pv_ccw_fast'])
        # RULE 28: IF (pa IS up_left) AND (pv IS cw_slow) THEN force IS left_slow
        f3 = min(pa['pa_up_left'], pv['pv_cw_slow'])
        # RULE 38: IF (pa IS up) AND (pv IS ccw_slow) THEN force IS left_slow
        f4 = min(pa['pa_up'], pv['pv_ccw_slow'])
        max_force['force_left_slow'] = max(f1, f2, f3, f4)

        # force_right_slow
        # RULE 7: IF (pa IS up_more_left) AND (pv IS cw_fast) THEN force IS right_slow
        f1 = min(pa['pa_up_more_left'], pv['pv_cw_fast'])
        # RULE 22: IF (pa IS down_right) AND (pv IS cw_fast) THEN force IS right_slow
        f2 = min(pa['pa_down_right'], pv['pv_cw_fast'])
        # RULE 25: IF (pa IS up_right) AND (pv IS ccw_slow) THEN force IS right_slow
        f3 = min(pa['pa_up_right'], pv['pv_ccw_slow'])
        # RULE 40: IF (pa IS up) AND (pv IS cw_slow) THEN force IS right_slow
        f4 = min(pa['pa_up'], pv['pv_cw_slow'])
        max_force['force_right_slow'] = max(f1, f2, f3, f4)

        # force_stop
        # RULE 10: IF (pa IS down_more_right) AND (pv IS cw_slow) THEN force IS stop
        f1 = min(pa['pa_down_more_right'], pv['pv_cw_slow'])
        # RULE 12: IF (pa IS down_more_left) AND (pv IS ccw_slow) THEN force IS stop
        f2 = min(pa['pa_down_more_left'], pv['pv_ccw_slow'])
        # RULE 13: IF (pa IS down_more_right) AND (pv IS ccw_fast) THEN force IS stop
        f3 = min(pa['pa_down_more_right'], pv['pv_ccw_fast'])
        # RULE 14: IF (pa IS down_more_right) AND (pv IS cw_fast) THEN force IS stop
        f4 = min(pa['pa_down_more_right'], pv['pv_cw_fast'])
        # RULE 15: IF (pa IS down_more_left) AND (pv IS cw_fast) THEN force IS stop
        f5 = min(pa['pa_down_more_left'], pv['pv_cw_fast'])
        # RULE 16: IF (pa IS down_more_left) AND (pv IS ccw_fast) THEN force IS stop
        f6 = min(pa['pa_down_more_left'], pv['pv_ccw_fast'])
        # RULE 21: IF (pa IS down_right) AND (pv IS ccw_fast) THEN force IS stop
        f7 = min(pa['pa_down_right'], pv['pv_ccw_fast'])
        # RULE 23: IF (pa IS down_left) AND (pv IS cw_fast) THEN force IS stop
        f8 = min(pa['pa_down_left'], pv['pv_cw_fast'])
        # RULE 36: IF (pa IS down) AND (pv IS cw_fast) THEN force IS stop
        f9 = min(pa['pa_down'], pv['pv_cw_fast'])
        # RULE 37: IF (pa IS down) AND (pv IS ccw_fast) THEN force IS stop
        f10 = min(pa['pa_down'], pv['pv_ccw_fast'])
        # RULE 42: IF (pa IS up) AND (pv IS stop) THEN force IS stop
        f11 = min(pa['pa_up'], pv['pv_stop'])
        # RULE 0:  IF (pa IS up AND pv IS stop) OR (pa IS up_right AND pv IS ccw_slow) OR (pa IS up_left AND pv IS cw_slow)
        # THEN force IS stop;
        f12 = min(pa['pa_up'], pv['pv_stop'])
        f13 = min(pa['pa_up_right'], pv['pv_ccw_slow'])
        f14 = min(pa['pa_up_left'], pv['pv_cw_slow'])
        max_force['force_stop'] = max(f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14)

        return max_force

    def combined_force(self, inp):
        max_force = self.inference(inp['pa'], inp['pv'])
        x = np.arange(-100, 100 + 0.1, 0.1)
        final_force_values = np.zeros(len(x))
        for i in xrange(len(x)):
            force_memb = self.force_membership(x[i])
            final_force_values[i] = max(
                min(force_memb['force_stop'], max_force['force_stop']),
                min(force_memb['force_left_fast'], max_force['force_left_fast']),
                min(force_memb['force_right_fast'], max_force['force_right_fast']),
                min(force_memb['force_left_slow'], max_force['force_left_slow']),
                min(force_memb['force_right_slow'], max_force['force_right_slow'])
            )
        return x, final_force_values

    def defuzzification(self, x, force):
        numerator = 0.0
        denominator = 0.0
        for i in xrange(len(x)):
            numerator += force[i] * x[i] * 0.1
            denominator += force[i] * 0.1
        if denominator == 0.0:
            return 0.0
        return numerator / denominator
