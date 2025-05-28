import pyxel
import random
import constants
from enemy import Enemy
from bullet_enemy import BulletEnemy


class RegularEnemy(Enemy):
    """Regular enemies are small enemies that come in groups, may shoot once and may go back once they have reached
    half of the screen. They only have 1 life and give little points when killing them"""
    def __init__(self, x: int, y: int, direction: int):
        super().__init__(x, y)
        self.direction = direction
        self.sprite = (0, 1, 22, 15, 14)
        # The sprite of the enemy turned around
        self.__sprite_go_back = (0, 80, 22, 15, 14)
        self.lives = 1
        # It may shoot once or not shoot
        self.maximum_bullets = random.randint(0, 1)
        self.points = 50
        # Every plane starts going down and when it reaches a random y point, it will be decided if it stays going down
        # or if it goes up
        self.__go_back = False
        self.__go_back_where = random.randint(int(constants.HEIGHT / 2 + self.x_size), int(constants.HEIGHT - self.y_size))

    def move(self):
        """Updates the position of the sprite, so it follows a specific trajectory"""
        # It goes to the left
        if self.direction == 1:
            self.x -= 0.4
        # It goes to the right
        elif self.direction == 0:
            self.x += 0.4
        # It goes down if it does not have to go back
        if not self.__go_back:
            self.y += 1.5
        # It goes up when going back
        else:
            self.y -= 1.5
        # When it reaches the self.go_back_where y-coordinate it is randomly decided if it stays going down or if it
        # goes up
        if not self.__go_back and (int(self.y) == self.__go_back_where or int(self.y) == self.__go_back_where + 1):
            self.__go_back = bool(random.randint(0, 1))

    def draw(self):
        """Draws the sprite on screen and changes the sprite if it goes back when reaching the half of the screen"""
        if not self.__go_back:
            pyxel.blt(self.x, self.y, *self.sprite, colkey=7)
        else:
            pyxel.blt(self.x, self.y, *self.__sprite_go_back, colkey=7)

    def shoot(self):
        """Returns a bullet at the same coordinates as the plane"""
        # Shoots only if it is above the possible go back zone so that if it does not go back, it is still able to shoot
        # the player
        if self.maximum_bullets != 0 and self.lives > 0 and self.y > random.randint(30, self.__go_back_where):
            self.maximum_bullets -= 1
            return BulletEnemy(self.x + self.x_size / 2, self.y + self.y_size)
