import pygame
from pygame import mixer
import random

# Global Vars
S_Width = 800
S_Height = 700


class Spaceship(pygame.sprite.Sprite):
    """
    x: center x of object
    y: center y of object
    width: width of object
    height: height of object
    image: image of sprite
    game_obj: spaceship sprite object
    rect: spaceship rectangle
    health: health of the spaceship
    score: score of spaceship user in game

    """

    def __init__(self, x, y, width, height, image):
        """
        Initialize spaceship object

        """
        pygame.sprite.Sprite.__init__(self)
        game_obj = pygame.image.load(image).convert_alpha()
        self.game_obj = pygame.transform.scale(game_obj, (width, height))
        self.rect = self.game_obj.get_rect(center=(x, y))
        self.health = 5
        self.score = 0

    def update(self, screen: pygame.Surface):
        """
        Update the spaceship when the user moves it left or right on the screen
        """
        key = pygame.key.get_pressed()
        # User clicks left and position not out of screen
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.centerx -= 3
        # User clicks right and position not out of screen
        if key[pygame.K_RIGHT] and self.rect.x < S_Width - 50:
            self.rect.centerx += 3

        screen.blit(self.game_obj, (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
    """
    x: center x of object
    y: center y of object
    width: width of object
    height: height of object
    image: image of sprite
    game_obj: enemy sprite object
    rect: enemy rectangle
    speed: speed of enemy
    """
    def __init__(self, x, y, width, height, alien_num, speed):
        """
        Initialize enemy object
        """
        pygame.sprite.Sprite.__init__(self)
        image = "images/alien" + str(alien_num) + ".png"
        game_obj = pygame.image.load(image).convert_alpha()
        self.game_obj = pygame.transform.scale(game_obj, (width, height))
        self.rect = self.game_obj.get_rect(center=(x, y))
        self.speed = speed

    def update(self, screen: pygame.Surface):
        """
        Update enemy when spawned on screen
        """
        screen.blit(self.game_obj, (self.rect.x, self.rect.y))
        # Enemy in the screen boundary
        if self.rect.y < S_Height:
            self.rect.centery += self.speed
        # Enemy out of screen boundary
        else:
            rand_x = random.randint(0, S_Width - 50)
            self.rect.center = rand_x, 0


class Bullet(pygame.sprite.Sprite):
    """
    x: center x of object
    y: center y of object
    width: width of object
    height: height of object
    image: image of sprite
    game_obj: bullet sprite object
    rect: bullet rectangle

    """
    def __init__(self, x: int, y: int, width: int, height: int, image: str):
        """
        Initialize bullet object

        """
        pygame.sprite.Sprite.__init__(self)
        game_obj = pygame.image.load(image).convert_alpha()
        self.game_obj = pygame.transform.scale(game_obj, (width, height))
        self.rect = self.game_obj.get_rect(center=(x, y))

    def update(self, screen: pygame.Surface):
        """
        Update the movement of bullet when shot on screen

        """
        screen.blit(self.game_obj, (self.rect.x, self.rect.y))
        self.rect.centery -= 5
        # Bullet out of screen boundary
        if self.rect.y < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """
    x: center x of object
    y: center y of object
    width: width of object
    height: height of object
    curr_frame: current frame of explosion animation

    """
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize explosion sprite object
        """
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.curr_frame = 1

    def update(self, screen) -> bool:
        """
        Update the explosion animation on screen

        :return: True if game not over False in game over
        """
        # Current animation frame is less than 10
        if self.curr_frame < 10:
            exp = pygame.image.load("images/exp" + str(self.curr_frame) + ".png").convert_alpha()
            exp = pygame.transform.scale(exp, (self.width, self.height))
            screen.blit(exp, (self.x, self.y))
            return True
        # Current animation frame is greater/equal to 10
        else:
            self.curr_frame = 1
            return False


def display_text(screen: pygame.Surface, text: str, x_pos: int,
                 y_pos: int, size: int):
    """

    :param size: font size
    :param screen: screen to display text
    :param text: display text
    :param x_pos: x position of the text
    :param y_pos: y position of text
    """
    font = pygame.font.Font('freesansbold.ttf', size)
    surface = font.render(text, True, (255, 255, 255))
    rect = surface.get_rect(center=(x_pos, y_pos))
    screen.blit(surface, rect)


def main_menu():
    """
    Run main menu loop
    """

    pygame.init()
    # Create screen
    screen = pygame.display.set_mode((S_Width, S_Height))

    # Create clock
    clock = pygame.time.Clock()

    menu = True

    # Create Background
    bg = pygame.image.load("images/bg.jpg").convert()
    # help run pygame at consistent speed (convert method)
    bg = pygame.transform.scale(bg, (S_Width, S_Height))
    bg_y_pos = 0

    # Create menu logo
    logo = pygame.image.load("images/logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (500, 200))

    while menu:
        # Draw background
        bg_y_pos -= 1
        screen.blit(bg, (0, bg_y_pos))
        screen.blit(bg, (0, S_Height + bg_y_pos))
        screen.blit(logo, (150, 50))

        # Draw text
        display_text(screen, "Click Anywhere To Play", 400, 500, 30)

        # Update background position
        if bg_y_pos < -S_Height:
            bg_y_pos = 0

        # Wait for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP:
                menu = False

        # Update screen
        pygame.display.flip()
        clock.tick(15)

    if not menu:
        game_loop(0)


def game_loop(high_score: int):
    """
    Run game loop
    """

    pygame.init()
    # Create screen
    screen = pygame.display.set_mode((S_Width, S_Height))

    # Create clock
    clock = pygame.time.Clock()

    game_state = True

    # Create background
    bg = pygame.image.load("images/bg.jpg").convert()
    # help run pygame at consistent speed (convert method)
    bg = pygame.transform.scale(bg, (S_Width, S_Height))
    bg_y_pos = 0
    # Add background music
    mixer.music.load("sounds/background.wav")
    mixer.music.play(-1)

    # Create Spaceship
    spaceship = Spaceship(400, 600, 50, 100, "images/spaceship.png")

    # Create user event to spawn enemy
    spawn_enemy = pygame.USEREVENT
    pygame.time.set_timer(spawn_enemy, 2000)

    # lists of game sprites
    bullet_lst = pygame.sprite.Group()
    enemy_lst = pygame.sprite.Group()

    # Explosion animation variables
    exp_animation = False
    explosion = None

    # Create user event to run explosion animation
    exp_fps = pygame.USEREVENT
    pygame.time.set_timer(exp_fps, 40)

    # Game loop
    while game_state:

        # Draw background
        bg_y_pos -= 1
        screen.blit(bg, (0, bg_y_pos))
        screen.blit(bg, (0, S_Height + bg_y_pos))

        # Draw health bar
        pygame.draw.rect(screen, (255, 255, 255),  (5, 5, 110, 5))
        pygame.draw.rect(screen, (255, 255, 255),  (5, 30, 110, 5))
        pygame.draw.rect(screen, (255, 255, 255),  (5, 10, 5, 20))
        pygame.draw.rect(screen, (255, 255, 255),  (110, 10, 5, 20))
        pygame.draw.rect(screen, (0, 255, 0),  (10, 10, 20*spaceship.health,
                                                20))

        # Draw score number
        display_text(screen, "Score : " + str(spaceship.score), 750, 20, 20)

        # set background position
        if bg_y_pos < -S_Height:
            bg_y_pos = 0

        # Wait for an event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create bullet object
                    bullet = Bullet(spaceship.rect.centerx,
                                    spaceship.rect.centery,
                                    20, 20, "images/bullet.png")
                    bullet_lst.add(bullet)
                    # Play bullet sound
                    bullet_sound = pygame.mixer.Sound("sounds/laser.wav")
                    bullet_sound.set_volume(1.0)
                    bullet_sound.play()
            if event.type == spawn_enemy:
                if len(enemy_lst) < 5:
                    # Generate random number for variables for enemy
                    rand_x = random.randint(50, S_Width - 50)
                    rand_scale = random.randint(40, 100)
                    rand_speed = random.randint(1, 3)
                    alien_num = random.randint(1, 6)
                    # Create enemy object
                    enemy = Enemy(rand_x, -50, rand_scale, rand_scale, alien_num, rand_speed)
                    enemy_lst.add(enemy)
            if event.type == exp_fps and exp_animation:
                # Update the frame number for explosion animation
                explosion.curr_frame += 1

        # Update game sprites
        spaceship.update(screen)
        enemy_lst.update(screen)
        bullet_lst.update(screen)

        # Enemy an bullet collision
        for bullet in bullet_lst:
            for enemy in enemy_lst:
                if pygame.sprite.collide_rect(bullet, enemy):
                    exp_x = enemy.rect.x
                    exp_y = enemy.rect.y
                    exp_width = enemy.rect.width
                    exp_height = enemy.rect.height
                    enemy.kill()
                    bullet.kill()
                    spaceship.score += 1
                    exp_animation = True
                    # Create explosion object
                    explosion = Explosion(exp_x, exp_y, exp_width, exp_height)
                    # Play explosion sound
                    exp_sound = pygame.mixer.Sound("sounds/explosion.wav")
                    exp_sound.play()

        # Enemy and space ship collision
        for enemy in enemy_lst:
            if pygame.sprite.collide_rect(spaceship, enemy):
                exp_x = enemy.rect.x
                exp_y = enemy.rect.y
                exp_width = enemy.rect.width
                exp_height = enemy.rect.height
                enemy.kill()
                # Decrease health of spaceship
                spaceship.health -= 1
                exp_animation = True
                # Play explosion sound
                exp_sound = pygame.mixer.Sound("sounds/explosion.wav")
                exp_sound.play()
                if spaceship.health == 0:
                    # game over
                    game_state = False
                    explosion = Explosion(0, 0, S_Width, S_Height)
                else:
                    explosion = Explosion(exp_x, exp_y, exp_width, exp_height)

        # Run explosion animation
        if exp_animation:
            exp_animation = explosion.update(screen)

        # Update screen
        pygame.display.flip()
        clock.tick(120)

    # Go to game over screen
    if not game_state:
        if spaceship.score > high_score:
            # Change high score if current score greater
            high_score = spaceship.score

        game_over(spaceship.score, high_score)


def game_over(score: int, high_score: int):
    """
    Run game over loop
    """
    pygame.init()
    # Create Screen
    screen = pygame.display.set_mode((S_Width, S_Height))

    # Create Clock
    clock = pygame.time.Clock()

    menu = True

    # Create background
    bg = pygame.image.load("images/bg.jpg").convert()
    # help run pygame at consistent speed (convert method)
    bg = pygame.transform.scale(bg, (S_Width, S_Height))
    bg_y_pos = 0

    # Create game over title logo
    logo = pygame.image.load("images/gameover.png").convert_alpha()
    logo = pygame.transform.scale(logo, (500, 400))

    # Game over menu loop
    while menu:
        # Draw background
        bg_y_pos -= 1
        screen.blit(bg, (0, bg_y_pos))
        screen.blit(bg, (0, S_Height + bg_y_pos))
        screen.blit(logo, (150, 50))

        # Draw scores
        display_text(screen, "High Score : " + str(high_score), 400, 500, 30)
        display_text(screen, "Score : " + str(score), 400, 550, 30)

        # Draw text
        display_text(screen, "Click Anywhere To Play Again", 400, 650, 30)

        # Update position of back ground
        if bg_y_pos < -S_Height:
            bg_y_pos = 0

        # Wait for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP:
                # Play again
                menu = False

        # Update screen
        pygame.display.flip()
        clock.tick(15)

    if not menu:
        # Go back to game screen
        game_loop(high_score)


if __name__ == '__main__':
    main_menu()

