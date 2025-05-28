import pyxel
import random
import constants
from background import Background
from player import Player
from time_counter import TimeCounter
from boat import Boat
from regular_enemy import RegularEnemy
from red_enemy import RedEnemy
from bombardier import Bombardier
from super_bombardier import SuperBombardier
from bullet_player import BulletPlayer
from bullet_enemy import BulletEnemy


class Board:
    """Brings all the other classes together to create the game"""
    def __init__(self):
        # The program begins on the start screen
        self.__screen = 0
        self.__score = 0
        self.__high_score = 0
        # The list where the enemies that need to appear on screen will be stored
        self.__enemies_list = []
        # The list where the bullets that need to appear on screen will be stored
        # By storing enemies and bullets on different lists, even if the planes are killed, their bullets will still
        # remain on screen
        self.__bullets_list = []
        # A 2-second cycle that starts at 1 second
        self.__counter_screen0 = TimeCounter(1, 2)
        # Used for making a random enemy appear every 2 seconds
        # When the game starts, the first enemy appears in only 1 second so the user does not get bored
        self.__counter_enemies = TimeCounter(1, 2)
        # The player plane is placed at the bottom center of the screen
        self.__player = Player()
        # The background boat is placed at a random position x, and above the screen so the user sees it slowly
        # appearing
        self.__boat = Boat(random.randint(0, constants.WIDTH - constants.BOAT_X_SIZE * 2), - constants.BOAT_Y_SIZE)
        # The background is created
        self.background = Background(0.3, 64, (0, 0))
        self.background.initiate()
        # Initializes the game
        pyxel.init(constants.WIDTH, constants.HEIGHT, title="1942", fps=constants.FPS)
        # Loads the sprites file created with pyxel edit
        pyxel.load("assets.pyxres")
        # Invokes the update and draw methods on each frame
        pyxel.run(self.update, self.draw)

    def __draw_screen(self):
        """Draws the elements of each screen"""
        # Start screen
        if self.__screen == 0:
            # Black background
            pyxel.cls(0)
            # Draws the 1942 logo
            pyxel.blt(3, 60, 2, 8, 8, 184, 60, colkey=7)
            pyxel.text(12, 228, "A GAME BY SERGIO CERNUDA AND MARIA VAZQUEZ", 7)
            pyxel.text(68, 240, "(C) 2022 UC3M", 7)
            # Creates a flickering effect/animation on the text in a 2-second cycle
            # The cycle starts at 1 second so the user can notice the animation (He/She has to wait 0.5 seconds instead
            # of 1.5 seconds to see it)
            # The text is shown for 1.5 seconds, and then it is hidden (not drawn) for 0.5 seconds
            self.__counter_screen0.add_frame()
            if self.__counter_screen0.frames < constants.FPS * 1.5:
                pyxel.text(60, constants.HEIGHT / 2 + 30, "PRESS SPACE TO PLAY", 10)
        # Game screen
        elif self.__screen == 1:
            pyxel.cls(0)
            self.background.draw()
        # Game over screen
        elif self.__screen == 2:
            # Black background
            pyxel.cls(0)
            pyxel.text(70, constants.HEIGHT / 2 - 10, "GAME OVER", 7)
            # Shows the user how many points he/she made during the game
            pyxel.text(70, constants.HEIGHT / 2 + 10, "POINTS: " + str(self.__score), 10)
            pyxel.text(45, constants.HEIGHT / 2 + 60, "PRESS SPACE TO PLAY AGAIN", 7)
            pyxel.text(45, constants.HEIGHT / 2 + 70, "PRESS Q TO QUIT", 7)
            # Lets the user know if he/she surpassed the highscore
            # The color of the text changes in every frame
            if self.__score > self.__high_score:
                pyxel.text(70, constants.HEIGHT / 2 + 20, "NEW HIGHSCORE!", pyxel.frame_count % 16)

    def __change_screen(self):
        """Changes the screen if the conditions are met (start, game, game over)"""
        # The user is told in the start screen to press space in order to start playing
        if self.__screen == 0 and pyxel.btnp(pyxel.KEY_SPACE):
            self.__screen = 1
        # When the user loses, it goes to the game over screen
        if self.__player.lives == 0 and not self.__player.is_alive:
            self.__screen = 2
        # The user is told in the game over screen to press space in order to play again
        # It goes to the start screen and invokes the restart method so values are changed to be able to play again
        if self.__screen == 2 and pyxel.btnp(pyxel.KEY_SPACE):
            self.__screen = 0
            self.__restart(True)

    def __draw_stats(self):
        """Draws current points, highscore, lives and loop opportunities"""
        pyxel.text(10, 5, "POINTS", 0)
        pyxel.text(10, 15, str(self.__score), 0)
        pyxel.text(140, 5, "HIGH SCORE", 0)
        pyxel.text(140, 15, str(self.__high_score), 0)
        # Draws a heart on screen for each life the player has
        for live in range(self.__player.lives):
            pyxel.blt(10 + 10 * live, 243, 0, 168, 0, 9, 8, colkey=7)
        # Draws an R on screen for each loop opportunity the player has
        for loop_opportunity in range(self.__player.loop_opportunities):
            pyxel.text(165 + 6 * loop_opportunity, 245, "R", 15)

    def __restart(self, new_game: bool = False):
        """Changes appropriate values so the user can play another round or a new game
        @param new_game: bool"""
        # Deletes all the elements of the enemies and bullets lists
        self.__enemies_list.clear()
        self.__bullets_list.clear()
        # Restarts the timer that controls enemy appearance
        self.__counter_enemies = TimeCounter(1, 2)
        # The player returns to its initial position
        self.__player.x = constants.PLAYER_X_INITIAL
        self.__player.y = constants.PLAYER_Y_INITIAL
        # The player is not dead anymore
        self.__player.is_alive = True
        # If instead of just beginning a new round, a new game is created
        if new_game:
            # the boat returns to its random initial position
            self.__boat.x = random.randint(0, constants.WIDTH - constants.BOAT_X_SIZE * 2)
            self.__boat.y = - constants.BOAT_Y_SIZE
            # The player's stats return to their initial value
            self.__player.lives = 3
            self.__player.loop_opportunities = 3
            # If a new high score has been achieved, it updates its value and then the score returns to zero
            if self.__score > self.__high_score:
                self.__high_score = self.__score
            self.__score = 0

    def __clean(self, my_list: list):
        """Removes the elements of a list if they are not being used, in order to save memory space
        @param my_list: list"""
        for element in my_list:
            # Elements are not being used if have gone out of the screen or have disappeared because they have been
            # killed (in the case of enemies) or have hit a plane (in the case of bullets)
            if element.out_of_screen or not element.is_alive:
                my_list.remove(element)

    def __randomize_enemies(self):
        """Chooses a random enemy to appear next in the game"""
        # Checks if any of the elements of the enemies list is a super bombardier or a red enemy
        is_there_super_or_red = False
        for enemy in self.__enemies_list:
            if type(enemy) == SuperBombardier or type(enemy) == RedEnemy:
                is_there_super_or_red = True
        # Because the trajectories of super bombardiers and red enemies overlap, they cannot appear at the same time
        # Only regular enemies and bombardiers can appear while a super bombardier or a red enemy is already shown on
        # the screen
        if is_there_super_or_red:
            type_of_enemy = random.randint(0, 1)
        else:
            type_of_enemy = random.randint(0, 3)
        if type_of_enemy == 0:
            self.__generate_regular_enemy()
        elif type_of_enemy == 1:
            self.__generate_bombardier()
        elif type_of_enemy == 2:
            self.__generate_super_bombardier()
        elif type_of_enemy == 3:
            self.__generate_red_enemy()

    def __generate_regular_enemy(self):
        """Adds between 3 and 5 regular enemies to the enemies list"""
        # Randomly chooses if the planes will appear on the left (0) or right (1) half of the screen. And the direction
        # they will move along, right (0), left (1)
        direction = random.randint(0, 1)
        # Chooses randomly where the planes will appear
        # Concerning the x-axis: if left area is chosen, then it is between 20 and the half of the screen. If it is
        # right then it adds half of the (width - 20) for the planes to appear between the half of the screen and the
        # end of the screen (screen - 20)
        # Concerning the y-axis: when generating it creates planes at an increasingly higher y coordinate, so it takes
        # longer for the second plane to appear on screen than the first plane and so on.
        for i in range(random.randint(3, 5)):
            self.__enemies_list.append(RegularEnemy(random.randint(20, constants.WIDTH / 2) +
                                                    direction * (constants.WIDTH / 2 - 20), - (20 + i * 30), direction))

    def __generate_red_enemy(self):
        """Adds 7 red enemies to the enemies list"""
        # They are created on the left side of the screen at an increasingly smaller x coordinate, so it takes longer
        # for the second plane to appear than the first plane and so on
        for i in range(7):
            self.__enemies_list.append(RedEnemy(-20 - i * 25, 40))

    def __generate_bombardier(self):
        """Adds 1 bombardier to the enemies list"""
        # They are created on the upper side of the screen at a random x coordinate and with a random direction
        # Left = 0, right = 1
        self.__enemies_list.append(Bombardier(random.randint(0, constants.WIDTH), -20, random.randint(0, 1)))

    def __generate_super_bombardier(self):
        """Adds 1 super bombardier to the enemies list"""
        # They are created on the down side of the screen at a random x coordinate
        self.__enemies_list.append(SuperBombardier(random.randint(5, constants.WIDTH - 65), constants.HEIGHT))

    def __add_bullets(self, bullets):
        """Adds the number of bullets a plane is shooting to the bullets list
        @param bullets: BulletPlayer or BulletEnemy or tuple"""
        if bullets is not None:
            # For planes that shoot more than one bullet at a time (super bombardier)
            if type(bullets) == tuple:
                for element in bullets:
                    self.__bullets_list.append(element)
            else:
                self.__bullets_list.append(bullets)

    def __collisions(self):
        """Checks for those objects that are "touching" each other and removes lives or destroys them. It also adds
        points when an enemy is destroyed"""
        for enemy in self.__enemies_list:
            # Checks if an enemy is inside the area of the player if so destroys the player and the enemy
            if not self.__player.looping and self.__player.x - enemy.x_size <= enemy.x <= self.__player.x +\
                    self.__player.x_size and self.__player.y - enemy.y_size <= enemy.y <= self.__player.y + \
                    self.__player.y_size:
                self.__player.dying = True
                enemy.dying = True
            for bullet in self.__bullets_list:
                if type(bullet) == BulletPlayer:
                    # Checks if a player bullet is inside the area of an enemy and if so removes one live from the
                    # enemy, makes the bullet disappear and adds the corresponding points
                    if enemy.x - bullet.x_size <= bullet.x <= enemy.x + enemy.x_size and enemy.y - bullet.y_size <= \
                            bullet.y <= enemy.y + enemy.y_size:
                        bullet.is_alive = False
                        enemy.lives -= 1
                        self.__score += enemy.points
                        if enemy.lives == 0:
                            enemy.dying = True
                elif type(bullet) == BulletEnemy and not self.__player.looping:
                    # Checks if an enemy bullet is inside the area of the player and provokes the death of the player
                    # and the disappearance bullet
                    if self.__player.x - bullet.x_size <= bullet.x <= self.__player.x + self.__player.x_size \
                            and self.__player.y - bullet.y_size <= bullet.y <= self.__player.y + self.__player.y_size:
                        bullet.is_alive = False
                        self.__player.dying = True

    def update(self):
        """Invokes methods that involve some type of change in every frame"""
        self.__change_screen()
        # The game can be closed at any time
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # If we are on the game screen
        if self.__screen == 1:
            if self.__player.is_alive:
                self.__collisions()
            self.__boat.move()
            self.__clean(self.__enemies_list)
            self.__clean(self.__bullets_list)
            # Runs the counter_enemies
            self.__counter_enemies.add_frame()
            # When the cycle is completed, a new random enemy appears
            if self.__counter_enemies.frames == 0:
                self.__randomize_enemies()
            # Enemy-related invocations
            for enemy in self.__enemies_list:
                if not enemy.dying:
                    enemy.move()
                    enemy.check_out_of_screen()
                    self.__add_bullets(enemy.shoot())
            # Bullet-related invocations
            for bullet in self.__bullets_list:
                bullet.move()
                bullet.check_out_of_screen()
            # Player-related invocations
            if self.__player.lives > 0 and not self.__player.dying:
                self.__player.move()
                if pyxel.btnp(pyxel.KEY_S) and not (self.__player.looping or self.__player.dying):
                    self.__add_bullets(self.__player.shoot())
                if pyxel.btnp(pyxel.KEY_Z) and self.__player.loop_opportunities > 0:
                    self.__player.looping = True
                if not self.__player.is_alive:
                    self.__restart()

    def draw(self):
        """Invokes draw related methods in every frame so sprites and animations are shown on screen. An element whose
         method is invoked after another one is drawn on top of it"""
        self.__draw_screen()
        if self.__screen == 1:
            # The boat is in the background
            self.__boat.draw()
            # Enemy-related invocations
            for enemy in self.__enemies_list:
                if enemy.dying:
                    enemy.die()
                else:
                    enemy.draw()
            # Bullet-related invocations
            for bullet in self.__bullets_list:
                bullet.draw()
            # Player-related invocations
            if self.__player.looping:
                self.__player.loop()
            elif self.__player.dying:
                self.__player.die()
            else:
                self.__player.draw()
            self.__draw_stats()
