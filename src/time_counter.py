import constants
import pyxel


class TimeCounter:
    """Creates a cycle of a desired number of seconds by converting frames into seconds. Useful for making things happen
    every certain amount of time"""
    def __init__(self, initial_seconds: float, number_of_seconds: float):
        # If it is bigger than 0, the first time the cycle is executed, it ends early
        self.initial_seconds = initial_seconds
        # How many seconds the cycle should last
        self.number_of_seconds = number_of_seconds
        # FPS means frames per second, so if we multiply it by seconds, we get frames
        self.frames = initial_seconds * constants.FPS

    @property
    def frames_per_cycle(self):
        return self.number_of_seconds * constants.FPS

    def add_frame(self):
        """Adds 1 frame and when it reaches the limit of the cycle, it goes back to 0"""
        self.frames += 1
        if self.frames == self.frames_per_cycle:
            self.frames = 0

    def animate(self, x: int, y: int, sprites_tuple: tuple):
        """Given a certain collection of sprites, it draws them sequentially on the desired coordinates
        @param x: int
        @param y: int
        @param sprites_tuple: tuple"""
        # Every sprite of the collection is drawn for an equal amount of time/sprites
        frames_per_sprite = self.frames_per_cycle / len(sprites_tuple)
        # Draws the corresponding sprite within its time/sprites interval
        # For example, if we have a 1-second animation and 2 sprites, the first sprite will be drawn on the interval
        # [0, 0.5) and the second sprite on the interval [0.5, 1)
        for i in range(len(sprites_tuple)):
            if frames_per_sprite * i <= self.frames < frames_per_sprite * (i + 1):
                pyxel.blt(x, y, *sprites_tuple[i], colkey=7)
        # Adds a new frame so the animation keeps going
        self.add_frame()
