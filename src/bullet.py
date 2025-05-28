import constants
from sprite import Sprite


class Bullet(Sprite):
    """The mother class of the player and enemy bullets"""
    def __init__(self, x, y, speed_x: float, speed_y: float):
        super().__init__(x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        """Updates the position of the sprite, so it follows a specific trajectory"""
        self.x += self.speed_x
        self.y += self.speed_y
