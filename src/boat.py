import pyxel
import random
import constants
from sprite import Sprite


class Boat(Sprite):
    """A boat that moves on the ocean of the background and further decorates it"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sprite = (2, 12, 70, constants.BOAT_X_SIZE, constants.BOAT_Y_SIZE)

    def draw(self):
        """Draws the sprite on screen"""
        pyxel.blt(self.x, self.y, *self.sprite, colkey=7)
        # When the boat goes outside the screen, it is drawn at a random position x and above the screen (position y)
        # so it appears again after some time
        if self.y > constants.HEIGHT:
            self.x = random.randint(0, constants.HEIGHT - constants.BOAT_X_SIZE*2)
            self.y = - constants.BOAT_Y_SIZE * random.randint(2, 4)

    def move(self):
        """Updates the position of the sprite, so it follows a specific trajectory"""
        # This slow downwards velocity creates the illusion of the player plane flying high up in the air
        self.y += 0.5

