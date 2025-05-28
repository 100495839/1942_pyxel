import pyxel
import constants

from plane import Plane
from time_counter import TimeCounter


class Enemy(Plane):
    """Enemies are planes that try to shoot the player and that the player has to destroy to gain points"""
    def __init__(self, x, y):
        super().__init__(x, y)
        # The maximum number of times the enemy can shoot at the player
        self.maximum_bullets = 0
        # The points it gives when the player shoots at it
        self.points = 0
        # The sprites for the die animation
        self.sprite_die = ((0, 102, 24, 12, 11),
                             (0, 117, 24, 14, 12),
                             (0, 134, 22, 16, 15),
                             (0, 154, 22, 17, 15),
                             (0, 175, 22, 15, 15),
                             (0, 194, 22, 16, 15))
        # The die animation lasts 0.4 seconds
        self.counter_die = TimeCounter(0, 0.4)

    def die(self):
        """Animates and states the death of the enemy"""
        # The animation appears in the center of the sprite of the enemy
        self.counter_die.animate(self.x + self.x_size / 2, self.y + self.y_size / 2, self.sprite_die)
        # When the animation is over, it transitions from a "dying state" into a "dead state" so the program knows the
        # enemy is no longer useful
        if self.counter_die.frames == 0:
            self.dying = False
            self.is_alive = False
