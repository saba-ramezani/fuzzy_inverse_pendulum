# -*- coding: utf-8 -*-

# python imports
from math import radians


class World:

    def __init__(self,
                 M = 80.        , m = 16.       , l = 1.,
                 x = 0.         , v = 0.        , a = 0.,
                 theta = 0.     , omega = 0.    , alpha = 0.,
                 g = 9.8        , b = .1        , I = .006,
                 min_x = -10.   , max_x = 10.,
                 force = 0.):

        self.M = M # cart mass, kg
        self.m = m # pendulum mass, kg
        self.l = l # pendulum length, m

        self.x = x # cart position, m
        self.v = v # cart velocity, m/s
        self.a = a # cart acceleration, m/s^2

        self.theta = radians(theta) # pendulum central angle, radian
        self.omega = omega # pendulum angular velocity, m/s
        self.alpha = alpha # pendulum angular acceleration, m/s^2

        self.g = g # gravity acceleration, m/s^2
        self.b = b # cart coefficient of friction, newton/m/s
        self.I = I # moment of inertia, kg.m^2

        self.min_x = min_x # cart minimum x, m
        self.max_x = max_x # cart maximum x, m

        self.force = force # force applied on cart, newton
