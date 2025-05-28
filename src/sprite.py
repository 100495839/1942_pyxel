import pyxel
import constants


class Sprite:
    """The mother class of all the objects of the game that need to appear on screen: planes, bullets and the background
    boat"""
    def __init__(self, x: int, y: int):
        # The x-coordinate of the sprite
        self.x = x
        # The y-coordinate of the sprite
        self.y = y
        # The picture of the sprite in pyxel edit
        self.sprite = (0, 0, 0, 0, 0)
        # False when the sprite is no longer needed because it has disappeared
        self.is_alive = True
        # True when the sprite exits the screen
        self.out_of_screen = False

    @property
    def x_size(self):
        return self.sprite[3]

    @property
    def y_size(self):
        return self.sprite[4]

    def move(self):
        """Updates the position of the sprite, so it follows a specific trajectory"""
        pass

    def draw(self):
        """Draws the sprite on screen and sometimes changes the sprite to do an animation"""
        pass

    def check_out_of_screen(self):
        """Checks if the sprite is no longer needed as it has exited the screen"""
        if self.y < -150 or self.y > constants.HEIGHT:
            self.out_of_screen = True
