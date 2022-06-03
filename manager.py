# -*- coding: utf-8 -*-

# python imports
from copy import deepcopy
from time import time, sleep

# project imports
from simulator import Simulator
from gui import GUI


class Manager:

    def __init__(self, world, controller, dt=0.1, fps=60, monitor_width=1200, monitor_height=300):
        self.dt = dt
        self.fps = fps
        self.controller = controller

        self.simulator = Simulator(deepcopy(world))
        self.gui = GUI(monitor_width, monitor_height)


    def run(self):
        while True:
            now = time()

            force = self.controller.decide(self.simulator.world)
            print 'force:', force

            self.simulator.apply_force(force)
            self.simulator.tick(self.dt)

            self.gui.draw(self.simulator.world)
            sleep(max((1. / self.fps) - (time() - now), 0))
