import pygame
import random
from pygame.locals import *
from pygame import Surface

SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2


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


class Entity(pygame.sprite.Sprite):
    def __init__(self, pic_name, rgb_color, speed_range, pic_scale):
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
                random.randint(20, SCREEN_WIDTH-20),
                0,
            )
        )

        self.speed = random.randint(5, speed_range)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

pygame.init()

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

all_sprites = pygame.sprite.Group()

all_sprites.add(player)

drawing = False
pygame.mouse.set_visible(False)

running = True
while running:

    game_time = pygame.time.get_ticks()
    game_time_text = score_font.render(f"Time: {game_time/1000:.0f}", True, (180, 0, 0))

    pygame.display.set_caption("Game")

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == ADDENEMY:
            enemy = Entity("ball.gif", BLACK, 50, 0.7)
            enemies.add(enemy)
            all_sprites.add(enemy)

        elif event.type == ADDCOIN:
            coin = Entity(False, GREEN, 10, 0.7)
            coins.add(coin)
            all_sprites.add(coin)

        elif event.type == MOUSEBUTTONDOWN:
            player.rect.center = event.pos
            drawing = True

        elif event.type == MOUSEBUTTONUP:
            player.rect.center = event.pos
            drawing = False

        elif event.type == MOUSEMOTION and drawing:
            player.rect.center = event.pos


    enemies.update()
    coins.update()

    screen.fill(SKY_BLUE)

    for obj in all_sprites:
        screen.blit(obj.surf, obj.rect)

    enm = pygame.sprite.spritecollideany(player, enemies)
    if enm:
        enm.kill()
        score_life -= 1
        score_text_life = score_font.render(f"Life: {score_life}", True, (180, 0, 0))
        if score_life == 0:
            player.kill()
            lose_text = score_font.render("Game over", True, (180, 0, 0))
            screen.blit(lose_text, CENTER)
            running = False

    cns = pygame.sprite.spritecollideany(player, coins)
    if cns:
        cns.kill()
        score += 1
        score_text = score_font.render(f"Score: {score}", True, (180, 0, 0))

    if game_time <= 15000 and score == 10:
        win_text = score_font.render(f"You win!!!", True, (180, 0, 0))
        screen.blit(win_text, CENTER)
        running = False

    if game_time >= 15000 and score < 10:
        lose_text = score_font.render(f"You lose", True, (180, 0, 0))
        screen.blit(lose_text, CENTER)
        running = False


    screen.blit(game_time_text, (10, 100))
    screen.blit(score_text_life, (10, 20))
    screen.blit(score_text, (10, 60))

    pygame.display.flip()
    clock.tick(30)

    if not running:
        pygame.time.wait(2000)

pygame.quit()
