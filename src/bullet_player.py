import pyxel
from bullet import Bullet


class BulletPlayer(Bullet):
    """The bullets that the player shoots to kill the enemies. They move upwards"""
    def __init__(self, x: int, y: int, speed_x: float = 0, speed_y: float = -3):
        super().__init__(x, y, speed_x, speed_y)
        self.sprite = (0, 41, 0, 11, 11)

    def draw(self):
        """Draws the sprite on screen"""
        pyxel.blt(self.x, self.y, *self.sprite, colkey=7)
