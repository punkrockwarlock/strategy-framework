# -*- coding: utf-8 -*-

import pygame
import sys
import pygame.locals as locals
from Vector import Vec2d
import Viewport
import Map
import StrategyEntity

from config import *

clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
viewport = Viewport.Viewport(SCREEN)
viewport.setPosition(0, 0)
viewport.setLimit(0, -CELL_WIDTH)
viewport.setLimit(1, (MAP_WIDTH + CELL_WIDTH))
viewport.setLimit(2, -CELL_HEIGHT)
viewport.setLimit(3, (MAP_HEIGHT + CELL_HEIGHT))

theMap = Map.Map()
theMap.setViewport(viewport)

SCREEN.fill(pygame.locals.Color(255, 255, 255))

test = StrategyEntity.StrategyEntity()
test.setPosition(Vec2d(4 * CELL_WIDTH, 0))
test.setDimensions(CELL_WIDTH, CELL_HEIGHT)
test.setImage(pygame.Surface((test.getRect().width, test.getRect().height)))
test.setPath(theMap.findPath(theMap[4][0], theMap[14][12]))

# main loop
running = True
while running:
    for event in pygame.event.get():
        if (event.type == locals.QUIT):
            pygame.quit()
            sys.exit()
        if (event.type == locals.KEYDOWN):
            if (event.key == locals.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if (event.key == locals.K_a):
                theMove = Vec2d(-CELL_WIDTH, 0)
                if (viewport.inLimits(theMove)):
                    viewport.move(theMove)
                    viewport.fillScreen()
                    theMap.makeScreenCellsDirty()

            if (event.key == locals.K_d):
                theMove = Vec2d(CELL_WIDTH, 0)
                if (viewport.inLimits(theMove)):
                    viewport.move(theMove)
                    viewport.fillScreen()
                    theMap.makeScreenCellsDirty()

            if (event.key == locals.K_s):
                theMove = Vec2d(0, CELL_HEIGHT)
                if (viewport.inLimits(theMove)):
                    viewport.move(theMove)
                    viewport.fillScreen()
                    theMap.makeScreenCellsDirty()

            if (event.key == locals.K_w):
                theMove = Vec2d(0, -CELL_HEIGHT)
                if (viewport.inLimits(theMove)):
                    viewport.move(theMove)
                    viewport.fillScreen()
                    theMap.makeScreenCellsDirty()

            if (event.key == locals.K_RETURN):
                test.move()

    # get the mouse position
    (mouseX, mouseY) = pygame.mouse.get_pos()

    clock.tick(30)

    path = theMap.findPath(theMap[4][0], theMap.getCellFromMouse(mouseX, mouseY))
    theMap.draw()
    test.draw(viewport)

    theMap.drawPath(path)
    pygame.display.flip()
