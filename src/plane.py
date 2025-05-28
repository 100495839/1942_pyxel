from sprite import Sprite


class Plane(Sprite):
    """The mother class of the player and the enemies"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.lives = 0
        # When the plane runs out of lives, it shows a die animation before disappearing
        self.dying = False

    def shoot(self):
        """Returns a bullet at the same coordinates as the plane"""
        pass

    def die(self):
        """Animates and states the death of the plane"""
        pass
