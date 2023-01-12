import os
import sys

import pygame
from pygame import *
import pyganim
import tkinter as tk
import time

from random import randint

clock = pygame.time.Clock()

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)

programIcon = pygame.image.load('icon.png')

pygame.display.set_icon(programIcon)

deth_counter = 0
curlvl = 1
lvllist = ['lvlTEST', 'lvl1', 'lvl2', 'lvl3', 'lvl4', 'lvl5', 'lvl6', 'lvl7']


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/platform.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


root = tk.Tk()

WIN_WIDTH = root.winfo_screenwidth()
WIN_HEIGHT = root.winfo_screenheight()
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(DISPLAY, pygame.FULLSCREEN)
BACKGROUND = transform.scale(image.load('%s/data/Fon.jpg' % ICON_DIR), (WIN_WIDTH, WIN_HEIGHT))


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 4, -t + WIN_HEIGHT / 4

    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)


MOVE_SPEED = 7
WIDTH = 34
HEIGHT = 49
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35
ANIMATION_DELAY = 0.1
ICON_DIR = os.path.dirname(__file__)
ANIMATION_RIGHT = [('%s/data/r1.png' % ICON_DIR),
                   ('%s/data/r2.png' % ICON_DIR),
                   ('%s/data/r3.png' % ICON_DIR),
                   ('%s/data/r4.png' % ICON_DIR),
                   ('%s/data/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/data/l1.png' % ICON_DIR),
                  ('%s/data/l2.png' % ICON_DIR),
                  ('%s/data/l3.png' % ICON_DIR),
                  ('%s/data/l4.png' % ICON_DIR),
                  ('%s/data/l5.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/data/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/data/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/data/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/data/0.png' % ICON_DIR, 0.1)]
ANIMATION_DEATH = [('%s/data/d1.png' % ICON_DIR),
                   ('%s/data/d2.png' % ICON_DIR),
                   ('%s/data/d3.png' % ICON_DIR),
                   ('%s/data/d4.png' % ICON_DIR)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.live = True
        self.onGround = False
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x + 10, y, WIDTH - 10, HEIGHT)
        self.image.set_colorkey(Color(COLOR))
        self.dk = True
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        boltAnim = []
        for anim in ANIMATION_DEATH:
            boltAnim.append((anim, 0.2))
        self.boltAnimDeath = pyganim.PygAnimation(boltAnim, False)

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms, imortal):
        if (self.death()) and not imortal or not self.live:
            self.live = False
            if self.dk and not imortal:
                self.boltAnimDeath.play()
                self.dk = False
            self.image.fill(Color(COLOR))
            self.boltAnimDeath.blit(self.image, (0, 0))

        else:
            if up:
                if self.onGround:
                    self.yvel = -JUMP_POWER
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))

            if left:
                self.xvel = -MOVE_SPEED
                self.image.fill(Color(COLOR))
                if up:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimLeft.blit(self.image, (0, 0))

            if right:
                self.xvel = MOVE_SPEED
                self.image.fill(Color(COLOR))
                if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimRight.blit(self.image, (0, 0))

            if not (left or right):
                self.xvel = 0
                if not up:
                    self.image.fill(Color(COLOR))
                    self.boltAnimStay.blit(self.image, (0, 0))
            if not self.onGround:
                self.yvel += GRAVITY

            self.onGround = False
            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)

            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms)

    def alive(self):
        return self.live

    def death(self):
        if pygame.sprite.spritecollideany(self, enemy_list):
            return True
        if pygame.sprite.spritecollideany(self, EnemyMove_list):
            return True
        return False

    def Escape(self):
        if pygame.sprite.spritecollideany(self, door_list):
            return True
        return False

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0


class SpikeS(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/spikeS.png" % ICON_DIR)
        self.rect = Rect(x, y + 32 - 7, 32, 7)


class SpikeM(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/spikeM.png" % ICON_DIR)
        self.rect = Rect(x, y + 32 - 16, 32, 16)


class SpikeL(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/spikeL.png" % ICON_DIR)
        self.rect = Rect(x, y, 32, 32)


class SpikeS180(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/spikeS180.png" % ICON_DIR)
        self.rect = Rect(x, y, 32, 7)


class SpikeM180(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/spikeM180.png" % ICON_DIR)
        self.rect = Rect(x, y, 32, 16)


class SpikeL180(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/spikeL180.png" % ICON_DIR)
        self.rect = Rect(x, y, 32, 32)


class Rock(sprite.Sprite):
    def __init__(self, x, y, way=10, speedxy=4, side=1):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/rock.png" % ICON_DIR)
        self.rect = Rect(x, y, 32, 32)
        self.speedxy = speedxy * side
        self.k = 0
        self.way = way * 32
        self.side = side

    def update(self):
        if self.k == self.way * self.side:
            self.side = -self.side
            self.speedxy = -self.speedxy
            self.k = 0
        self.rect.x += self.speedxy
        self.k += self.speedxy


class Exit(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 46))
        self.image = image.load("%s/data/exit.png" % ICON_DIR)
        self.rect = Rect(x, y - 16, 32, 46)


def load_level(filename):
    filename = "lvl/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    x = 0
    y = 0
    for row in level:
        rc = 0
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "@":
                xh = x
                yh = y
            if col == "s":
                if level[y // 32 - 1][x // 32] == '-':
                    en = SpikeS180(x, y)
                else:
                    en = SpikeS(x, y)
                enemy_list.add(en)
                enemy.append(en)
            if col == "m":
                if level[y // 32 - 1][x // 32] == '-':
                    en = SpikeM180(x, y)
                else:
                    en = SpikeM(x, y)
                enemy_list.add(en)
                enemy.append(en)
            if col == "l":
                if level[y // 32 - 1][x // 32] == '-':
                    en = SpikeL180(x, y)
                else:
                    en = SpikeL(x, y)
                enemy_list.add(en)
                enemy.append(en)
            if col == "E":
                exit = Exit(x, y)
                entities.add(exit)
                door_list.add(exit)
            if col == "r":
                k = 0
                xr = x // 32
                yr = y // 32
                r = True
                while r:
                    xr += 1
                    if level[yr][xr] == ' ':
                        k += 1
                    else:
                        side = 1
                        r = False
                if k == 0:
                    r = True
                    xr = x // 32
                    yr = y // 32
                    while r:
                        xr -= 1
                        if level[yr][xr] == ' ':
                            k += 1
                        else:
                            side = -1
                            r = False
                rock = Rock(x, y, k, 8, side)
                enemyMoveS.append(rock)
                if not lvllist[curlvl] == 'lvl6':
                    EnemyMove_list.add(rock)
                else:
                    platforms.append(rock)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    return xh, yh


def cool_font(text, w=0, h=0, r=100, s=3):
    pygame.init()
    font = pygame.font.Font("GameF/vergilia.ttf", r)
    gameoverB = font.render(text, True, (0, 0, 255))
    rect = gameoverB.get_rect()
    rect.center = (w + s * 3 + randint(1, s), h + s * 3 + randint(1, s))
    screen.blit(gameoverB, rect)
    gameoverG = font.render(text, True, (0, 255, 0))
    rect = gameoverG.get_rect()
    rect.center = (w + s * 2 + randint(1, s), h + s * 2 + randint(1, s))
    screen.blit(gameoverG, rect)
    gameoverR = font.render(text, True, (255, 0, 0))
    rect = gameoverR.get_rect()
    rect.center = (w + s + randint(1, s), h + s + randint(1, s))
    screen.blit(gameoverR, rect)
    gameoverRGB = font.render(text, True, (255, 255, 255))
    rect = gameoverRGB.get_rect()
    rect.center = (w, h)
    screen.blit(gameoverRGB, rect)


def start_screen():
    pygame.init()
    pygame.display.set_caption("Insame Sqwirtle")
    fon = pygame.transform.scale(BACKGROUND, (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    cool_font("Insame Sqwirtle", WIN_WIDTH // 2, WIN_HEIGHT // 2 - WIN_WIDTH // 25)
    cool_font("Press any button to start", WIN_WIDTH // 2, WIN_HEIGHT // 2 + WIN_HEIGHT // 25)
    clock = pygame.time.Clock()
    pl = pygame.USEREVENT + 50
    t = 50
    pygame.time.set_timer(pl, t)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN:
                return True
            if event.type == pl:
                screen.blit(fon, (0, 0))
                cool_font("Insame Sqwirtle", WIN_WIDTH // 2, WIN_HEIGHT // 2 - WIN_WIDTH // 25)
                cool_font("Press any button to start", WIN_WIDTH // 2, WIN_HEIGHT // 2 + WIN_HEIGHT // 25)
        pygame.display.flip()


def main(curlvl, deth_counter):
    pygame.init()
    pygame.display.set_caption("Insame Sqwirtle")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    left = right = False
    up = False
    a = None
    s = 3
    k = False
    end = False
    imortal = False
    resc = 0
    clock = pygame.time.Clock()

    level = load_level(f"{lvllist[curlvl]}.txt")
    x, y = generate_level(level)

    hero = Player(x, y)
    entities.add(hero)
    font = pygame.font.Font("GameF/vergilia.ttf", 100)

    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_w:
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                running = False
            if e.type == KEYDOWN and e.key == K_LCTRL:
                MOVE_SPEED = 4
            if e.type == KEYUP and e.key == K_LCTRL:
                MOVE_SPEED = 7
            if e.type == KEYDOWN and e.key == K_RALT:
                MOVE_SPEED = 4
            if e.type == KEYUP and e.key == K_RALT:
                MOVE_SPEED = 7
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_w:
                up = False
            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False
            if e.type == KEYUP and e.key == K_r:
                resc = 0
            if e.type == KEYDOWN and e.key == pygame.K_r and not hero.alive():
                if end:
                    end = False
                    curlvl = 1
                    deth_counter = -1
                deth_counter += 1
                return curlvl, deth_counter
            all_keys = pygame.key.get_pressed()
            if all_keys[pygame.K_n] and all_keys[pygame.K_d]:
                imortal = True
            if all_keys[pygame.K_r] and hero.alive():
                resc += 1
        if resc // 60 == 2:
            deth_counter += 1
            return curlvl, deth_counter
        screen.blit(BACKGROUND, (0, 0))
        camera.update(hero)
        hero.update(left, right, up, platforms, imortal)
        EnemyMove_list.update()
        for e in enemyMoveS:
            screen.blit(e.image, camera.apply(e))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        for e in enemy:
            screen.blit(e.image, camera.apply(e))
        if resc != 0:
            cool_font(f'{round(resc / 120 * 100)}%', WIN_WIDTH // 2, WIN_HEIGHT // 2)
        if hero.Escape():
            curlvl = curlvl + 1
            if curlvl + 1 <= len(lvllist):
                return curlvl, deth_counter
            else:
                screen.blit((transform.scale(image.load('%s/data/end.png' % ICON_DIR), (WIN_WIDTH, WIN_HEIGHT))),
                            (0, 0))
                con = font.render('Congratulations, it was the last level!!!^_^', True, (255, 255, 255))
                rect = con.get_rect()
                rect.center = (screen.get_rect().center[0], screen.get_rect().center[1] - 100)
                screen.blit(con, rect)
                con = font.render("Press R to Respawn", True, (255, 255, 255))
                rect = con.get_rect()
                rect.center = (screen.get_rect().center[0], screen.get_rect().center[1])
                screen.blit(con, rect)
                con = font.render("Thx u for playing our game!!!", True, (255, 255, 255))
                rect = con.get_rect()
                rect.center = (screen.get_rect().center[0], screen.get_rect().center[1] + 100)
                screen.blit(con, rect)
                con = font.render(f"U died: {deth_counter} times", True, (255, 255, 255))
                rect = con.get_rect()
                rect.center = (screen.get_rect().center[0], screen.get_rect().center[1] + 250)
                screen.blit(con, rect)
                end = True
                hero.live = False
        elif not hero.alive():
            cool_font("Press R to Respawn", WIN_WIDTH // 2, WIN_HEIGHT // 2)
            pygame.draw.rect(screen, (0, 0, 255), (
                0 + s * 3 * 2 + randint(1, s), 0 + s * 3 * 2 + randint(1, s), WIN_WIDTH, WIN_HEIGHT), 5)
            pygame.draw.rect(screen, (0, 255, 0), (
                0 + s * 2 * 2 + randint(1, s), 0 + s * 2 * 2 + randint(1, s), WIN_WIDTH, WIN_HEIGHT), 5)
            pygame.draw.rect(screen, (255, 0, 0), (
                0 + s * 2 + randint(1, s), 0 + s * 2 + randint(1, s), WIN_WIDTH, WIN_HEIGHT), 5)
            pygame.draw.rect(screen, (255, 255, 255), (
                0, 0, WIN_WIDTH, WIN_HEIGHT), 5)
        cool_font(f"number of deaths: {deth_counter}", 1780, 20, 25, 2)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    runnig = start_screen()
    while runnig:
        enemy_list = pygame.sprite.Group()
        entities = pygame.sprite.Group()
        EnemyMove_list = pygame.sprite.Group()
        platforms = []
        enemy = []
        enemyMoveS = []
        door_list = pygame.sprite.Group()
        curlvl, deth_counter = main(curlvl, deth_counter)
