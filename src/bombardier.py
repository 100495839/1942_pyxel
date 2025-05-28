import pyxel
import random
import constants
from enemy import Enemy
from bullet_enemy import BulletEnemy


class Bombardier(Enemy):
    """Bombardiers are big enemies that come alone and do a zigzag movement. It shoots several times, it needs to be
    shot more than once to be killed and gives a lot of points"""
    def __init__(self, x: int, y: int, direction: int):
        super().__init__(x, y)
        self.direction = direction
        self.sprite = (0, 1, 66, 31, 22)
        self.lives = 5
        self.maximum_bullets = random.randint(3, 5)
        self.points = 150
        # Used for shooting at random moments
        self.__current_frames = pyxel.frame_count

    def move(self):
        """Updates the position of the sprite, so it follows a specific trajectory"""
        # It goes left
        if self.direction == 0:
            self.x -= 1.2
        # It goes right
        elif self.direction == 1:
            self.x += 1.2
        # When it touches the right side of the screen, it starts going left
        if self.x > constants.WIDTH - self.x_size:
            self.direction = 0
        # When it touches the left side of the screen, it starts going right
        elif self.x < 0:
            self.direction = 1
        # It always goes down
        self.y += 0.7

    def draw(self):
        """Draws the sprite on screen"""
        pyxel.blt(self.x, self.y, *self.sprite, colkey=7)

    def shoot(self):
        """Returns a bullet at the same coordinates as the plane"""
        if self.maximum_bullets != 0 and self.lives > 0:
            # Shoot if it has been more than a random number between 1/2 and 3/2 seconds since it has last shot
            if pyxel.frame_count > random.randint(self.__current_frames + constants.FPS * (1 / 2),
                                                  self.__current_frames + constants.FPS * (3 / 2)):
                self.maximum_bullets -= 1
                # Stores the frame in which it has shot so that it can shoot again after some time
                self.__current_frames = pyxel.frame_count
                return BulletEnemy(self.x + self.x_size / 2, self.y + self.y_size)

