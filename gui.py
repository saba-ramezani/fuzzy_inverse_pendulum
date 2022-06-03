# -*- coding: utf-8 -*-

# python imports
from math import sin, cos, pi
import pygame


class GUI:

    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)

        self.rail_offset_x  = self.width / 10.
        self.rail_offset_y  = self.height / 2.

        self.display_name = "Fuzzy Inverted Pendulum"
        self._init_pygame()


    def _init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.display_name)


    def draw(self, world):
        # pixels per meter
        ppm = (self.width - 2 * self.rail_offset_x) / (world.max_x - world.min_x)

        # clear screen
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            (0, 0, self.width, self.height)
        )

        # draw rail
        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (int(self.rail_offset_x), int(self.rail_offset_y)),
            (int(self.width - self.rail_offset_x), int(self.rail_offset_y))
        )

        # draw walls
        pygame.draw.line(
            self.screen,
            (200, 0, 0),
            (int(self.rail_offset_x), int(self.rail_offset_y) - 15),
            (int(self.rail_offset_x), int(self.rail_offset_y) + 15)
        )

        pygame.draw.line(
            self.screen,
            (200, 0, 0),
            (int(self.width - self.rail_offset_x), int(self.rail_offset_y) - 15),
            (int(self.width - self.rail_offset_x), int(self.rail_offset_y) + 15)
        )

        # draw cart
        cx = self.rail_offset_x + (world.x - world.min_x) * ppm
        cy = self.rail_offset_y

        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (int(cx), int(cy)),
            10
        )

        # draw pendulum
        theta = world.theta + (pi / 2.)
        px = cx + (world.l * sin(theta)) * ppm
        py = (self.rail_offset_y) + (world.l * cos(theta)) * ppm

        pygame.draw.circle(
            self.screen,
            (0, 200, 0),
            (int(px), int(py)),
            4
        )

        pygame.draw.line(
            self.screen,
            (0, 0, 200),
            (int(cx), int(cy)),
            (int(px), int(py))
        )

        # update screen
        pygame.display.update()
