import pyxel
import random

import constants
from enemy import Enemy
from bullet_enemy import BulletEnemy


class SuperBombardier(Enemy):
    """Super bombardiers are the biggest enemies, and they come alone. It shoots several times, 3 bullets at a time. It
    needs to be shot many times to be killed and gives a lot of points"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = (0, 1, 101, 63, 48)
        self.lives = 15
        self.maximum_bullets = random.randint(5, 8)
        self.points = 200
        # The plane appears on the bottom part of the screen and starts going up
        self.__direction = "linear"
        # Necessary attributes for angular motion
        self.__angle = 0
        self.__x_cons = self.x
        # The y-coordinate it will have after 3.8 seconds
        self.__y_cons = self.y - constants.FPS * (3.8)
        self.__current_frames = pyxel.frame_count
        self.__go_backwards = False

    @property
    def y_size(self):
        # Because the sprite is so big, we made the y_size smaller to offer a better user experience
        return self.sprite[4] - 20

    def move(self):
        """Updates the position of the sprite, so it follows a specific trajectory"""
        if self.__direction == "linear":
            self.y -= 1
        elif self.__direction == "sine":
            if self.x >= constants.WIDTH - self.x_size:
                self.__go_backwards = True
            elif self.x <= 0:
                self.__go_backwards = False
            if self.__go_backwards:
                self.x -= 1
            else:
                self.x += 1
            self.y = self.__y_cons + pyxel.sin(self.__angle) * 20
            self.__angle += 3
        # When 3.8 seconds have passed since its creation, it starts describing a sine trajectory
        if pyxel.frame_count == self.__current_frames + constants.FPS * 3.8:
            self.__direction = "sine"
        # When it goes out of bullets, it goes up again to exit the screen
        if self.maximum_bullets <= 0:
            self.__direction = "linear"

    def draw(self):
        """Draws the sprite on screen"""
        pyxel.blt(self.x, self.y, *self.sprite, colkey=7)

    def shoot(self):
        """Returns 3 bullets at the same coordinates as the plane"""
        # Shoots only while in the sine trajectory
        if self.maximum_bullets != 0 and self.lives > 0 and self.__direction == "sine":
            # Shoot if it has been more than a random number between 1 and 3 seconds since it has last shot
            if pyxel.frame_count > random.randint(self.__current_frames + constants.FPS,
                                                  self.__current_frames + constants.FPS * 3):
                self.maximum_bullets -= 1
                # Stores the frame in which it has shot so that it can shoot again after some time
                self.__current_frames = pyxel.frame_count
                # One of the bullets follows a horizontal trajectory. The other 2 follow a diagonal trajectory
                return BulletEnemy(self.x + self.x_size / 2, self.y + self.y_size / 2), \
                       BulletEnemy(self.x + self.x_size / 2, self.y + self.y_size / 2, -0.3), \
                       BulletEnemy(self.x + self.x_size / 2, self.y + self.y_size / 2, 0.3)
