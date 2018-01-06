from __future__ import print_function
import Cell
from GameEntity import GameEntity
from Vector import Vec2d
import unittest
import os.path
import pygame
from noise import snoise2
from helpers import PriorityQueue, heuristic
from Path import Path

import config


class Map(GameEntity):
    def __init__(self):
        GameEntity.__init__(self)
        self.mapWidth = config.MAP_WIDTH
        self.mapHeight = config.MAP_HEIGHT
        self.cellWidth = config.CELL_WIDTH
        self.cellHeight = config.CELL_HEIGHT

        self.map = []
        self.generate()

        self.tileset = None
        self.viewport = None

        self.walls = []

    def __repr__(self):
        return 'Map({}, {})'.format(self.mapWidth / self.cellWidth,
                                    self.mapHeight / self.cellHeight)

    def __getitem__(self, position):
        return self.map[position]

    def setViewport(self, viewport):
        if (hasattr(viewport, 'screen')):
            self.viewport = viewport
        else:
            raise AttributeError("setViewport failed. viewport invalid")

    def getViewport(self):
        return self.viewport

    def inBounds(self, position):
        """ Checks if the passed position is in the map bounds
            @return true if in map bounds, false if not"""

        if (hasattr(position, 'x') and hasattr(position, 'y')):
            (x, y) = (position.x, position.y)
        else:
            (x, y) = (position[0], position[1])

        return (0 <= x < (self.mapWidth / self.cellWidth) and
                0 <= y < (self.mapHeight / self.cellHeight))

    def passable(self, position):
        cell = self.map[position[0]][position[1]]
        return cell.passable

    def neighbours(self, cell):
        (x, y) = (cell.x, cell.y)
        results = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1),
                   (x - 1, y - 1), (x - 1, y + 1), (x + 1, y + 1),
                   (x + 1, y - 1)]

        if (x + y) % 2 == 0:
            results.reverse()

        results = filter(self.inBounds, results)
        results = filter(self.passable, results)
        return self.getCells(results)

    def getCellFromMouse(self, mouseX, mouseY):
        (x, y) = (int(abs((mouseX + self.viewport.getPosition().x) / self.cellWidth)),
                  int(abs((mouseY + self.viewport.getPosition().y) / self.cellHeight)))

        if (self.inBounds((x, y))):
            return self.map[x][y]
        else:
            return self.map[0][0]

    def getCells(self, cellTuples):
        """ Returns a list of cells from position tuples """

        returnList = []
        for cellTuple in cellTuples:
            returnList.append(self.map[cellTuple[0]][cellTuple[1]])

        return returnList

    def generate(self):
        for x in range(0, self.mapHeight / self.cellHeight):
            temp = []
            for y in range(0, self.mapWidth / self.cellWidth):
                temp.append(Cell.Cell(Vec2d(x, y),
                                      snoise2(x, y, 10) * 5.0 + 20.0))
            self.map.append(temp)

    def draw(self):
        cellsOnScreen = self.getCellsOnScreen()
        for row in self.map[cellsOnScreen[0]:cellsOnScreen[1]]:
            for cell in row[cellsOnScreen[2]:cellsOnScreen[3]]:
                if (cell.getDirty()):
                    cell.draw(self.viewport)
                    cell.setDirty(False)

    def drawOverlay(self, cell):
        print(cell)
        pygame.draw.rect(self.viewport.screen, pygame.Color(255, 255, 255), cell.getRect())

    def findPath(self, start, finish):
        """ Uses A* algorithm to find the shortest path from start to finish

            Code was copied from:
            https://www.redblobgames.com/pathfinding/a-star/introduction.html"""

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == finish:
                break

            for nextCell in self.neighbours(current):
                new_cost = cost_so_far[current] + nextCell.cost
                if nextCell not in cost_so_far or new_cost < cost_so_far[nextCell]:
                    cost_so_far[nextCell] = new_cost
                    priority = new_cost + heuristic(finish, nextCell)
                    frontier.put(nextCell, priority)
                    came_from[nextCell] = current

        # reconstruct the path
        current = finish
        path = []
        try:
            while current != start:
                path.append(current)
                current = came_from[current]
        except KeyError:
            # if there is no path found, just return the start
            return Path([start])

        path.append(start)
        path.reverse()

        return Path(path)

    def drawPath(self, path):
        """ Draws a path onto the map """

        prevPos = self.viewport.getLocalPosition(path[0].getCentre())
        for cell in path:
            cell.setDirty(True)
            local_pos = self.viewport.getLocalPosition(cell.getCentre())
            pygame.draw.circle(self.viewport.screen,
                               pygame.Color(255, 255, 255),
                               (local_pos.x, local_pos.y),
                               2)
            pygame.draw.aaline(self.viewport.screen,
                               pygame.Color(255, 255, 255),
                               (prevPos.x, prevPos.y),
                               (local_pos.x, local_pos.y))
            prevPos = local_pos

    def printMap(self):
        for row in self.map:
            print("[", end='')
            for cell in row:
                print(cell.__str__() + ", ", end='')
            print("]")

    def makeScreenCellsDirty(self):
        cellsOnScreen = self.getCellsOnScreen()
        for row in self.map[cellsOnScreen[0]:cellsOnScreen[1]]:
            for cell in row[cellsOnScreen[2]:cellsOnScreen[3]]:
                cell.setDirty(True)

    def loadTileset(self, tilesetPath):
        if (os.path.isfile(tilesetPath)):
            self.tileset = pygame.image.load(tilesetPath).convert()
        else:
            raise Exception("Invalid tileset path: " + tilesetPath)

    def getCellsOnScreen(self):
        """ Finds the cell index min and max """

        # the position of the viewport
        viewportPos = self.viewport.getPosition()

        # set the starting index mins and maxes
        x_min, y_min = 0, 0
        x_max = self.mapWidth / self.cellWidth
        y_max = self.mapHeight / self.cellHeight

        if (viewportPos.x > 0):
            x_min = viewportPos.x / self.cellWidth

        if (viewportPos.y > 0):
            y_min = viewportPos.y / self.cellHeight

        mapRight = ((viewportPos.x * -1) + self.mapWidth)
        if (mapRight > self.viewport.getRect().width):
            x_max = x_max - ((mapRight - self.viewport.getRect().width) /
                             self.cellWidth)

        mapTop = ((viewportPos.y * -1) + self.mapHeight)
        if (mapTop > self.viewport.getRect().height):
            y_max = y_max - ((mapTop - self.viewport.getRect().height) /
                             self.cellHeight)

        return (x_min, x_max, y_min, y_max)
