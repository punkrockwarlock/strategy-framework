import collections
import heapq

"""
 classes copied from:
  https://www.redblobgames.com/pathfinding/a-star/implementation.html
"""


class myQueue:
    def __init__(self, startList=None):
        self.elements = collections.deque()
        if(startList is not None):
            self.elements.extend(startList)

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        try:
            return self.elements.popleft()
        except IndexError:
            return None

    def extend(self, extendList):
        self.elements.extend(extendList)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(a.x - b.x) + abs(a.y - b.y)
