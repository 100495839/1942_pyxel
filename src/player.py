import pyxel
import constants
from plane import Plane
from bullet_player import BulletPlayer
from time_counter import TimeCounter


class Player(Plane):
    """The player plane that lets the user interact with the game. Apart from the things all planes can do, the
    player also has the ability to do a loop to avoid being killed"""
    def __init__(self, x: int = constants.PLAYER_X_INITIAL, y: int = constants.PLAYER_Y_INITIAL):
        super().__init__(x, y)
        self.sprite = (0, 1, 0, 26, 16)
        # Sprites for the helix animation (its default state)
        self.__sprite_helix = ((0, 1, 0, 26, 16),
                         (0, 73, 0, 26, 16),
                         (0, 105, 0, 26, 16),
                         (0, 137, 0, 26, 16),
                         (0, 105, 0, 26, 16),
                         (0, 73, 0, 26, 16))
        # Sprites for the loop animation
        self.__sprite_loop = ((0, 7, 160, 28, 14),
                              (0, 43, 162, 27, 12),
                              (0, 76, 163, 29, 10),
                              (0, 111, 165, 25, 7),
                              (0, 7, 193, 27, 12),
                              (0, 43, 192, 30, 17),
                              (0, 74, 188, 32, 22),
                              (0, 116, 186, 32, 25),
                              (0, 3, 225, 30, 21),
                              (0, 36, 226, 28, 17),
                              (0, 69, 229, 27, 12),
                              (0, 102, 233, 27, 7),
                              (0, 136, 233, 25, 8),
                              (0, 168, 232, 25, 11),
                              (0, 200, 230, 25, 13))
        # Sprites for the die animation
        self.__sprite_die = ((0, 44, 67, 25, 21),
                             (0, 74, 65, 30, 27),
                             (0, 108, 63, 32, 30),
                             (0, 143, 63, 31, 31),
                             (0, 178, 64, 31, 29),
                             (0, 214, 66, 29, 24),
                             (0, 0, 0, 1, 0))
        self.lives = 3
        # The number of times the plane can loop in the game
        self.loop_opportunities = 3
        # Lets the program know if the plane is looping
        # It is important because the plane has different properties while looping (it is invulnerable to enemy bullets)
        self.looping = False
        # A half-second cycle for the helix animation
        self.__counter_helix = TimeCounter(0, 0.5)
        # The loop animation (and so the "looping state") lasts 2 seconds
        self.__counter_loop = TimeCounter(0, 2)
        # The die animation (and so the "dying state") lasts 1 second
        self.__counter_die = TimeCounter(0, 1)

    def move(self):
        """Updates the position of the player for it to move horizontally, vertically and diagonally, with collisions,
        so it cannot exit the screen"""
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < constants.WIDTH - self.x_size:
            self.x += 2
        elif pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x -= 2
        # Notice how the right or left key and the up or down key can be pressed at the same time in order to move
        # diagonally
        if pyxel.btn(pyxel.KEY_UP) and self.y > 0:
            self.y -= 2
        elif pyxel.btn(pyxel.KEY_DOWN) and self.y < constants.PLAYER_Y_INITIAL:
            self.y += 2

    def draw(self):
        """Creates the default helix animation"""
        self.__counter_helix.animate(self.x, self.y, self.__sprite_helix)

    def shoot(self):
        """Returns a bullet at the same coordinates as the plane"""
        return BulletPlayer(self.x + self.x_size / 2 - 6, self.y - self.y_size + 6)

    def loop(self):
        """Creates the loop animation"""
        self.__counter_loop.animate(self.x, self.y, self.__sprite_loop)
        # When the loop animation finishes, it subtracts a loop opportunity goes out of its "looping state"
        if self.__counter_loop.frames == 0:
            self.loop_opportunities -= 1
            self.looping = False

    def die(self):
        """Animates and states the death of the player"""
        self.__counter_die.animate(self.x, self.y, self.__sprite_die)
        # When the die animation finishes, it subtracts a live and transitions from a "dying state" into a "dead state"
        if self.__counter_die.frames == 0:
            self.lives -= 1
            self.dying = False
            # This attribute is used for the program to know that it has to start another round or end the game as there
            # is nothing more to show (the die animation has finished)
            self.is_alive = False
