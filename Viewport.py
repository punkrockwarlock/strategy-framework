# -*- coding: utf-8 -*-

import unittest
from pygame import Rect, Surface
from GameEntity import GameEntity
from pygame import locals


class Viewport(GameEntity):
    """ Viewport class designed to be game independant."""

    def __init__(self, screen):
        GameEntity.__init__(self)

        # pygame screen
        self.screen = screen

        # defines the movement limit for the screen
        self.limits = [None, None, None, None]

        # set the viewport dimensions to screen dimensions       
        self.setDimensions(self.screen.get_width(), self.screen.get_height())

        # used to centre the viewport on a gameObject's position
        self.track = None

    def inView(self, rect):
        """ Checks if any part of a rect is in the viewport """

        return self.getRect().colliderect(rect)

    def setLimit(self, index, limit):
        """ Sets the limits that the viewport can move in global co-ords """

        self.limits[index] = limit

    def inLimits(self, offset):
        pos = self.getPosition() + offset
        if (self.limits[0]):
            if (pos.x < self.limits[0]):
                return False

        if (self.limits[1]):
            if ((self._rect.topright[0] + offset.x) >= self.limits[1]):
                return False

        if (self.limits[2]):
            if (pos.y < self.limits[2]):
                return False

        if (self.limits[3]):
            if ((self._rect.bottomright[1] + offset.y) >= self.limits[3]):
                return False

        return True

    def enforceLimits(self):
        """ Checks if the current viewport position is beyond bounds """

        pos = self.getPosition()
        if (self.limits[0]):
            if (pos.x < self.limits[0]):
                self._rect.x = self.limits[0]

        if (self.limits[1]):
            if (self._rect.topright[0] > self.limits[1]):
                self._rect.x = self.limits[1] - self._rect.width

        if (self.limits[2]):
            if (pos.y < self.limits[2]):
                self._rect.y = self.limits[2]

        if (self.limits[3]):
            if (self._rect.bottomright[1] > self.limits[3]):
                self._rect.y = self.limits[3] - self._rect.height

    def update(self):
        self.enforceLimits()

    def draw(self, image, position):
        # get a vector of the local position of the sprite
        local_vec = position - self.getPosition()

        # draw the sprite's image to the local position
        self.screen.blit(image, (local_vec.x, local_vec.y))

    def getLocalPosition(self, position):
        return position - self.getPosition()

    def fillScreen(self):
        self.screen.fill(locals.Color(255, 255, 255))


# unit testing
class testViewport(unittest.TestCase):
    def setUp(self):
        self.screen = Surface((600, 600))

    def test_setLimit(self):
        vp = Viewport(self.screen)
        vp.setLimit(0, 101)
        vp.setLimit(1, 1001)
        vp.setLimit(2, 202)
        vp.setLimit(3, 2002)

        self.assertEqual(vp.limits[0], 101)
        self.assertEqual(vp.limits[1], 1001)
        self.assertEqual(vp.limits[2], 202)
        self.assertEqual(vp.limits[3], 2002)

    def test_checkLimits(self):
        vp = Viewport(self.screen)
        vp.setLimit(0, 101)
        vp.setLimit(1, 1001)
        vp.setLimit(2, 202)
        vp.setLimit(3, 2002)

        vp.setPosition(50, 100)
        vp.checkLimits()
        self.assertEqual(vp._rect.x, 101)
        self.assertEqual(vp._rect.y, 202)

        vp.setPosition(1500, 2500)
        vp.checkLimits()
        self.assertEqual(vp._rect.x, 401)
        self.assertEqual(vp._rect.y, 1402)

    def test_inView(self):
        vp = Viewport(self.screen)
        vp.setPosition(0, 0)
        vp.setDimensions(1000, 1000)

        rect = Rect(100, 100, 100, 100)
        self.assertTrue(vp.inView(rect))

        rect = Rect(2000, 2000, 100, 100)
        self.assertFalse(vp.inView(rect))

if __name__ == "__main__":
    unittest.main()
