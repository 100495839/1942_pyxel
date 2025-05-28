import pyxel
from bullet import Bullet


class BulletEnemy(Bullet):
    """The bullets that enemies shoot to kill the player. They move downwards"""
    def __init__(self, x: int, y: int, speed_x: float = 0, speed_y: float = 3):
        super().__init__(x, y, speed_x, speed_y)
        self.sprite = (0, 61, 6, 4, 4)

    def draw(self):
        """Draws the sprite on screen"""
        pyxel.blt(self.x, self.y, *self.sprite, colkey=7)
