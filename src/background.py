import pyxel

import constants


class Background:
    def __init__(self, speed_y: float, tile_size: int, images: tuple):
        # Speed at which the background will be moving. It has to be a float <= 1
        self.speed_y = speed_y
        # Used for movement. (Later: It comes from adding speed_y and subtracting it 1)
        self.__acumulated_y = 0
        # List that will contain all the data (as form of list: [x-coordinate, y-coordinate, u-image,v-image]) of the
        # tiles in the background.
        self.__background = []
        # Int that should be a divisor of both self.window_wide and self.window_tall.
        self.tile_size = tile_size
        # A tuple that contains two elements (u, v). These are based on the tileset and should be the starting point of
        # a tile with x,y = self.image_size size.
        # For example: If self.image_size = 16 and u = 0, v = 16. Then it will choose a tile that starts at (0, 16) and
        # ends at (16, 32)
        self.images = images
        # Later used for knowing the amount of images to generate in x and y.
        self.__ylements = constants.HEIGHT / self.tile_size
        self.__xlements = constants.WIDTH / self.tile_size
        # Placed here to avoid having to calculated lots of times.
        self.__randoms = len(images) - 1

    def initiate(self):
        # Should only be used once at the beginning of the game. It fills the list self.__background with
        # (self.__ylements + 1) * self.__xlements, amount of elements, enough to cover the whole screen and a bit above
        # so generation seems smooth. This list later will be worked with in def draw().
        for i in range(int(self.__ylements + 1)):
            for g in range(int(self.__xlements)):
                self.__background.append(
                    [(self.__xlements - g - 1) * self.tile_size, (self.__ylements - i) * self.tile_size, *self.images])
        # Remark: list is inversely made, so later we can remove elements in the right order. It first contains the
        # elements below.

    def draw(self):
        # GENERATION
        # Checks if the background, first element, the one below the most has left the frame, so it can create a new
        # tile. Then it removes the element that has left the frame. It does this for all the elements in the row that
        # have left the frame.
        if self.__background[0][1] > constants.HEIGHT:
            y_position = self.__background[-1][1] - self.tile_size
            # y_position will be the y coordinate for this new row to be generated. It is where the last element is
            # located, the one that is above the most. Subtracting the size of a tile, so it fits perfectly
            for g in range(int(self.__xlements)):
                self.__background.append([g * self.tile_size, y_position, *self.images])
                del self.__background[0]
        # DRAWING AND MOVEMENT
        # Draws the tile set first starting from the zero element and changing at a rate of one, that is the reason for
        # the usage of position. Accumulated_y is used for movement when speed_y is lower than 1, so it doesn't make any
        # visual glitch.

        if self.speed_y >=1:
            self.__acumulated_y = self.speed_y
        elif self.__acumulated_y >= 1:
            self.__acumulated_y -= 1
            self.__acumulated_y += self.speed_y
        else:
            self.__acumulated_y += self.speed_y

        position = 0
        for i in range(int(self.__ylements + 1)):
            for g in range(int(self.__xlements)):
                pyxel.bltm(self.__background[position][0], self.__background[position][1], 0, self.__background[position][2],
                           self.__background[position][3], self.tile_size, self.tile_size)
                if self.__acumulated_y >= 1:
                    self.__background[position][1] += 1
                # Changes the position of the y in the list so next time is printed a bit below
                position += 1
