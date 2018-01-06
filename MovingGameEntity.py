from GameEntity import GameEntity
from Vector import Vec2d
from SteeringManager import SteeringManager
from functions import truncate


class MovingGameEntity(GameEntity):
    def __init__(self):
        GameEntity.__init__(self)
        self.velocity = Vec2d(0, 0)
        self.SManager = SteeringManager(self)

        self._max_speed = 5
        self._mass = 2

    def setVelocity(self, velocity):

        # velocity should be a Vec2d
        self.velocity = velocity

    def getVelocity(self):
        return self.velocity

    def getMass(self):
        return self._mass

    def update(self):
        self.velocity = truncate(self.velocity + self.SManager.getSteering(),
                                 self._max_speed)

        self.setPosition(self.getPosition() + self.velocity)
