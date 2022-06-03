# -*- coding: utf-8 -*-

# python imports
from math import sin, cos, pi


class Simulator:

    def __init__(self, world):
        self.world = world


    def tick(self, dt):
        w = self.world
        theta = w.theta + (pi / 2.)

        # calculate and update accelerations
        N = w.m * (w.a - (w.I * (w.omega ** 2.) * sin(theta)) + (w.I * w.alpha * cos(theta)))
        P = w.m * ((w.I * (w.omega ** 2.) * cos(theta)) + (w.I * w.alpha * sin(theta))) + w.g
        w.a = (w.force - N - (w.b * w.v)) / w.M
        w.alpha = -(N * w.I * cos(theta) + P * w.I * sin(theta)) / w.I

        # update velocities
        w.v += w.a * dt
        w.omega += w.alpha * dt

        # update positions
        w.x += w.v * dt
        w.theta += w.omega * dt

        # check limits
        if not (w.min_x <= w.x <= w.max_x):
            w.a = 0.
            w.v = 0.
            w.x = w.min_x if w.x < w.min_x else w.max_x
            #w.x = w.max_x if w.x < w.min_x else w.min_x

        while w.theta > 2. * pi:
            w.theta -= 2. * pi

        while w.theta < 0.:
            w.theta += 2. * pi

        # reset force
        w.force = 0.


    def apply_force(self, force):
        self.world.force += force
