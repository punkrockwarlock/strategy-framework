import pygame
import pygame.locals as locals
import unittest
from Vector import Vec2d


class GameEntity:
    def __init__(self):
        self._rect = locals.Rect(0, 0, 0, 0)
        self._image = None

    def setPosition(self, xOrVec, y=None):
        """ Set the position of the game entity, in global co-ords. _
        Can supply x and y, or a Vector """

        if (y is None):
            self._rect.x = xOrVec.x
            self._rect.y = xOrVec.y
        else:
            self._rect.x = xOrVec
            self._rect.y = y

    def move(self, xOrVec, y=None):
        """ Moves the position of the game entity by the given offset. _
        Can supply x and y, or a Vector """

        if (y is None):
            self.setPosition(self.getPosition() + xOrVec)
        else:
            self._rect.x += xOrVec
            self._rect.y += y

    def getPosition(self):
        """ Gets the current position of the game entity, as a Vector2D """
        return Vec2d(self._rect.x, self._rect.y)

    def getCentre(self):
        """ returns the centre point of the cell as a vector """

        centre = self._rect.center
        return Vec2d(centre[0], centre[1])

    def setDimensions(self, width=None, height=None):
        """ Sets the width and/or height of the game entity """

        if width:
            self._rect.width = width

        if height:
            self._rect.height = height

    def getRect(self):
        """ Returns a rect representing the game entity """

        return self._rect

    def setImage(self, image):
        """ Sets an image for the game entity """

        # check if image is a surface
        if hasattr(image, 'fill'):
            self._image = image
        else:
            loaded_image = pygame.image.load(image)
            self._image = loaded_image.convert_alpha()

    def getImage(self):
        """ Returns the game entity's image """

        return self._image

    def draw(self, viewport):
        """ blits and image to the passed viewport, to its current position """

        viewport.draw(self.getImage(), self.getPosition())

    def distanceTo(self, other):
        vec = None

        if (hasattr(other, 'getPosition')):
            # other is a GameEntity
            vec = other.getPosition()
        elif (hasattr(other, '__slots__')):
            # other is a Vec2d
            vec = other
        else:
            # other is a tuple
            vec = Vec2d(other[0], other[1])

        if (vec is None):
            raise AttributeError

        return (vec - self.getPosition()).get_length()


# unit testing
class testGameEntity(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((100, 100))

    def test_setPosition(self):
        vp = GameEntity()
        vp.setPosition(101, 202)

        self.assertEqual(vp._rect.x, 101)
        self.assertEqual(vp._rect.y, 202)

        vp = GameEntity()
        vec = Vec2d(303, 404)
        vp.setPosition(vec)

        self.assertEqual(vp._rect.x, 303)
        self.assertEqual(vp._rect.y, 404)

    def test_getPosition(self):
        vp = GameEntity()
        vp.setPosition(101, 202)
        vec = vp.getPosition()

        self.assertEqual(vec.x, 101)
        self.assertEqual(vec.y, 202)

    def test_setDimensions(self):
        vp = GameEntity()
        vp.setDimensions(102, 304)

        self.assertEqual(vp._rect.width, 102)
        self.assertEqual(vp._rect.height, 304)

    def test_getRect(self):
        vp = GameEntity()
        vp.setPosition(101, 202)
        vp.setDimensions(303, 404)

        rect = vp.getRect()
        self.assertEqual(rect.x, 101)
        self.assertEqual(rect.y, 202)
        self.assertEqual(rect.width, 303)
        self.assertEqual(rect.height, 404)

    def test_move(self):
        vp = GameEntity()
        vp.setPosition(0, 0)
        vp.setDimensions(1000, 1000)

        vp.move(10, 10)
        self.assertEqual(vp.getPosition(), Vec2d(10, 10))

    def test_setImage(self):
        ge = GameEntity()
        ge.setImage("mario.png")

        self.assertIsNotNone(ge._image)

    def test_getImage(self):
        ge = GameEntity()
        ge.setImage("mario.png")

        temp = None
        temp = ge.getImage()
        self.assertIsNotNone(temp)

    def test_distanceTo(self):
        ge = GameEntity()
        ge.setPosition(100, 100)

        ge1 = GameEntity()
        ge1.setPosition(101, 100)

        self.assertEqual(ge.distanceTo(ge1), 1)
        self.assertEqual(ge.distanceTo(Vec2d(101, 100)), 1)
        self.assertEqual(ge.distanceTo((101, 100)), 1)

if __name__ == "__main__":
    unittest.main()
