from GameEntity import GameEntity
import pygame
from Vector import Vec2d
import sys

import config


class Cell(GameEntity):
    def __init__(self, position, perlin):
        self.x = position.x
        self.y = position.y
        self.cost = 0
        self.passable = True

        GameEntity.__init__(self)

        self.setPosition(Vec2d(position.x * config.CELL_WIDTH,
                               position.y * config.CELL_HEIGHT))
        self.setDimensions(config.CELL_WIDTH, config.CELL_HEIGHT)

        self.dirty = True
        self.terrainHeight = perlin

        self.getType()

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self):
        return 'Cell({}, {})'.format(self.x,
                                     self.y)

    def getType(self):
        if (self.terrainHeight > 20):
            image = pygame.image.load('./img/grass_1.png')

        else:
            self.passable = False
            image = pygame.image.load('./img/water_1.png')

        try:
            # convert loaded image to display surface
            image.convert()

        except pygame.error:
            # there will be an error if display mode is not set i.e. if the
            # module is imported by itself, there will be no screen
            pass

        self.setImage(image)

    def setDirty(self, isDirty):
        self.dirty = isDirty

    def getDirty(self):
        return self.dirty
