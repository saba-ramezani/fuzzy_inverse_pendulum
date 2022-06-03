#!/usr/bin/env python
# -*- coding: utf-8 -*-

# project imports
from conf import ConfigReader
from world import World
from my_controller import FuzzyController
from manager import Manager


conf = ConfigReader()

if __name__ == '__main__':
    world = World(**conf.world_config())
    controller = FuzzyController()
    manager = Manager(world, controller, **conf.simulation_config())
    manager.run()
