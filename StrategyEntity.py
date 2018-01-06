import GameEntity
import Path


class StrategyEntity(GameEntity.GameEntity):
    def __init__(self):
        GameEntity.GameEntity.__init__(self)

        self.path = Path.Path()

    def setPath(self, path):
        self.path = Path.Path(path)

    def move(self):
        if (self.path is not None):
            theMove = self.path.getNext()

            if (theMove is not None):
                self.setPosition(theMove.getPosition())

            for cell in self.path:
                cell.setDirty(True)
