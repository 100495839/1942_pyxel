import pyxel

from enemy import Enemy


class RedEnemy(Enemy):
    """Red enemies are small enemies that come in groups, forming a circle. They do not shoot. They only have 1 life
    and give some more points than regular enemies when killing them"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sprite = (0, 1, 43, 14, 13)
        self.lives = 1
        self.points = 100
        # Necessary attributes for angular motion
        self.__y_cons = self.y
        self.__x_cons = 60
        self.__angle = 0
        self.__amplitude = 30

    def move(self):
        """Updates the position of the sprite, so it follows a specific trajectory"""
        if self.x < self.__x_cons and self.__angle == 0:
            self.x += 2
        elif self.__angle < 3 / 2 * 360:
            self.y = self.__y_cons + pyxel.sin(self.__angle) * self.__amplitude
            self.x = self.__x_cons + self.__amplitude - pyxel.cos(self.__angle) * self.__amplitude
            self.__angle += 4.2
        else:
            self.x += 2

    def draw(self):
        """Draws the sprite on screen"""
        pyxel.blt(self.x, self.y, *self.sprite, colkey=7)
