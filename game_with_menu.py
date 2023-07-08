import time

import pygame
import random
from pygame.locals import *
from pygame import Surface

SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

pygame.init()

BG = (52, 78, 91)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Menu')


class ParticlePrinciple:
    def __init__(self):
        self.particles = []
        self.surface = pygame.image.load('star.png').convert_alpha()
        self.width = self.surface.get_rect().width
        self.height = self.surface.get_rect().height

    def emit(self):
        if self.particles:
            self.delete_particle()
            for particle in self.particles:
                particle[0].x += particle[1]
                particle[0].y += particle[2]
                particle[3] -= 0.2
                screen.blit(self.surface, particle[0])

    def add_particle(self, x, y):
        pos_x = x - self.width / 2
        pos_y = y - self.height / 2

        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)

        lifetime = random.randint(4, 10)
        particle_rect = pygame.Rect(pos_x, pos_y, self.width, self.height)

        self.particles.append([particle_rect, direction_x, direction_y, lifetime])

    def delete_particle(self):
        particle_copy = [particle for particle in self.particles if particle[3] > 0]
        self.particles = particle_copy


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Player(pygame.sprite.Sprite):
    def __init__(self, pic_name, rgb_color, pic_scale):
        super().__init__()

        if not pic_name:
            self.surf = Surface((40, 40))
            self.surf.fill(Color(rgb_color))
        else:
            self.surf = pygame.image.load(pic_name).convert()
            self.surf = pygame.transform.rotozoom(self.surf, 0, pic_scale)
            self.surf.set_colorkey(rgb_color, RLEACCEL)

        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -25)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 25)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-25, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(25, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Entity(pygame.sprite.Sprite):
    def __init__(self, pic_name, rgb_color, speed_range, pic_scale, x_gen=0, y_gen=0):
        super().__init__()

        if not pic_name:
            self.surf = Surface((40, 40))
            self.surf.fill(Color(rgb_color))
        else:
            self.surf = pygame.image.load(pic_name).convert()
            self.surf = pygame.transform.rotozoom(self.surf, 0, pic_scale)
            self.surf.set_colorkey(rgb_color, RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                x_gen,
                y_gen,
            )
        )

        self.speed = random.randint(5, speed_range)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


start_img = pygame.image.load('buttons/BUT_START.png').convert_alpha()
start_button = Button(304, 125, start_img, 1)

options_img = pygame.image.load('buttons/BUT_OPT.png').convert_alpha()
option_button = Button(297, 250, options_img, 1)

quit_img = pygame.image.load('buttons/BUT_EXIT.png').convert_alpha()
quit_button = Button(336, 375, quit_img, 1)


def main_func():
    pygame.init()

    particle = ParticlePrinciple()

    pygame.mixer.pre_init(44100, -16, 1, 512)
    collide_mus = pygame.mixer.Sound("sound.wav")
    win_mus = pygame.mixer.Sound("win.wav")
    bg_mus = pygame.mixer.Sound("1.ogg")

    clock = pygame.time.Clock()
    SIZE = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(SIZE)

    pygame.font.init()

    score = 0
    score_life = 3
    score_font = pygame.font.SysFont('arial', 36)

    score_text = score_font.render(f"Score: {score}", True, (180, 0, 0))
    score_text_life = score_font.render(f"Life: {score_life}", True, (180, 0, 0))

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 1000)

    ADDCOIN = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCOIN, 1000)

    player = Player('dino1.png', BLACK, 0.5)
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.3)

    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    coins_lose = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    music_on = False
    #pygame.mouse.set_visible(False)
    delay_val = 2000

    t0 = time.time()

    set_game_duration = 20
    score_to_catch = 5

    running = True
    while running:

        t1 = time.time()

        game_time = t1 - t0
        game_time_text = score_font.render(f"Time: {game_time:.0f}", True, (180, 0, 0))

        pygame.display.set_caption("Game")

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    delay_val = 0

                elif event.key == K_SPACE:
                    if music_on:
                        bg_mus.stop()
                        music_on = False
                    else:
                        bg_mus.play()
                        music_on = True

            elif event.type == ADDENEMY:
                enemy = Entity("ball.gif", BLACK, 50, 0.7, random.randint(20, SCREEN_WIDTH - 20))
                enemies.add(enemy)
                all_sprites.add(enemy)

            elif event.type == ADDCOIN:
                coin = Entity('cactus.png', BLACK, 10, 0.7, random.randint(20, SCREEN_WIDTH - 20))
                coins.add(coin)
                all_sprites.add(coin)

            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)

        enemies.update()
        coins.update()

        coins_lose.update()

        screen.fill(SKY_BLUE)

        for obj in all_sprites:
            screen.blit(obj.surf, obj.rect)

        enm = pygame.sprite.spritecollideany(player, enemies)
        if enm:
            collide_mus.play()
            enm.kill()
            score_life -= 1
            score_text_life = score_font.render(f"Life: {score_life}", True, (180, 0, 0))

            for _ in range(score):
                coin_l = Entity('cactus.png',
                                BLACK,
                                10,
                                0.5,
                                random.randint(player.rect.x - 40, player.rect.x + 40),
                                random.randint(player.rect.y - 40, player.rect.y + 40))
                coins_lose.add(coin_l)
                all_sprites.add(coins_lose)
                pygame.display.update()

            if score_life == 0:
                player.kill()
                lose_text = score_font.render("Game over", True, (180, 0, 0))
                screen.blit(lose_text, CENTER)
                running = False

        cns = pygame.sprite.spritecollideany(player, coins)
        if cns:
            collide_mus.play()
            cns.kill()
            score += 1
            score_text = score_font.render(f"Score: {score}", True, (180, 0, 0))

            particle.add_particle(player.rect.x, player.rect.y)
            particle.add_particle(player.rect.x, player.rect.y)
            particle.add_particle(player.rect.x, player.rect.y)
            pygame.display.flip()

        if game_time <= set_game_duration and score == score_to_catch:
            win_mus.play()
            win_text = score_font.render(f"You win!!!", True, (180, 0, 0))
            screen.blit(win_text, CENTER)
            running = False

        if game_time >= set_game_duration:
            lose_text = score_font.render(f"You lose", True, (180, 0, 0))
            screen.blit(lose_text, CENTER)
            running = False

        particle.emit()
        screen.blit(game_time_text, (10, 100))
        screen.blit(score_text_life, (10, 20))
        screen.blit(score_text, (10, 60))

        pygame.display.flip()
        clock.tick(30)

        if not running:
            pygame.time.wait(delay_val)


menu_state = 'main'

run = True
while run:
    screen.fill(WHITE)

    if menu_state == 'main':
        if start_button.draw(screen):
            main_func()
        elif option_button.draw(screen):
            menu_state = 'options'
        elif quit_button.draw(screen):
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            run = False

    pygame.display.update()

pygame.quit()