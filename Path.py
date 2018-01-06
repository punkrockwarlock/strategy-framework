import sys
import pygame
from helpers import myQueue


class Path:
    def __init__(self, nodeList=None):
        self.__list = None
        self.queue = myQueue()

        if nodeList:
            try:
                self.setPath(nodeList)
            except Exception as e:
                sys.stderr.write(str(e))

    def __len__(self):
        return len(self.__list)

    def __repr__(self):
        if (self.__list > 0):
            return 'Path({}, {})'.format(self.__list[0],
                                         self.__list[len(self.__list) - 1])
        else:
            return 'Path(Empty)'

    def __validList(self, nodeList):
        """ Checks if every item in a list is a valid map position """

        for node in nodeList:
            if not (hasattr(node, 'getPosition')):
                return False

        return True

    def __getitem__(self, key):
        return self.__list[key]

    def getNext(self):
        return self.queue.get()

    def setPath(self, nodeList):
        """ Takes a list of map nodes and sets it as the path """

        if (self.__validList(nodeList)):
            self.__list = nodeList
            self.queue.extend(self.__list)
        else:
            raise Exception("Invalid nodes in node list")

    def getPath(self):
        """ """
        return self.__list

    def reverse(self):
        """ Returns a new Path, reversed """

        reversedPath = self.__list[:]
        reversedPath.reverse()
        return Path(reversedPath)
