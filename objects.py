import pygame
from constants import *
import utils

pygame.mixer.init()


class PlayerSword(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()

        self.image = img
        self.right_image = self.image
        self.left_image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Player(pygame.sprite.Sprite):
    sword_clang = pygame.mixer.Sound("sounds/clangberserk.mp3")
    guts_scream = pygame.mixer.Sound("sounds/guts_scream_1.mp3")

    def __init__(self, x, y, sword_number, img, frames_num):
        super().__init__()

        self.sword_number = sword_number
        self.change_x = 0
        self.change_y = 0
        self.speed = 10
        self.lives = 3

        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.elves = pygame.sprite.Group()

        self.walking_frames_l = utils.get_anim_frames(img, frames_num)
        self.walking_frames_r = []

        self.direction = "R"

        for img in self.walking_frames_l:
            img = pygame.transform.flip(img, True, False)
            self.walking_frames_r.append(img)

        self.image = self.walking_frames_r[0]

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.sword = None

        self.anim_counter = 0
        self.sword_hide_counter = 0
        self.attacking = False
        self.hit_time = 0
        self.heal_time = 0

        self.sword_adjustment_coefs = [{'x_right': -40, 'x_left': -300, 'y': 30},
                                       {'x_right': -30, 'x_left': -250, 'y': -30}]

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .60

        if self.rect.y >= WIN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = WIN_HEIGHT - self.rect.height

    def update(self):

        if self.attacking:
            self.sword_hide_counter += 1
        if self.sword_hide_counter >= 10:
            self.attacking = False
            self.sword_hide_counter = 0

        time = pygame.time.get_ticks()

        if pygame.sprite.spritecollideany(self, self.enemies):

            if time - self.hit_time > 1000:
                self.lives -= 1
                self.guts_scream.play()
                self.hit_time = time

        if pygame.sprite.spritecollideany(self, self.elves):

            if time - self.hit_time > 1000 and self.lives < 3:
                self.lives += 1
                self.hit_time = time

        self.calc_grav()

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

        self.update_sword_position()
        if self.change_x != 0:
            self.update_animation()

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= WIN_HEIGHT:
            self.change_y = -15

    def go_left(self):
        self.change_x = -self.speed
        self.direction = "L"

    def go_right(self):
        self.change_x = self.speed
        self.direction = "R"

    def stop(self):
        self.change_x = 0

    def update_sword_position(self):

        if self.direction == "R":
            self.sword.image = self.sword.right_image
            self.sword.rect.x = self.rect.x + self.rect.width + self.sword_adjustment_coefs[self.sword_number][
                'x_right']
            self.sword.rect.y = self.rect.y + self.sword_adjustment_coefs[self.sword_number]['y']
        else:
            self.sword.image = self.sword.left_image
            self.sword.rect.x = self.rect.x + self.rect.width + self.sword_adjustment_coefs[self.sword_number]['x_left']
            self.sword.rect.y = self.rect.y + self.sword_adjustment_coefs[self.sword_number]['y']

    def update_animation(self):
        self.anim_counter += 1
        if self.anim_counter >= FPS:
            self.anim_counter = 0

        if self.direction == "R":
            frame = self.anim_counter % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = self.anim_counter % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

    def attack(self):
        self.sword_hide_counter = 0
        self.attacking = True
        self.sword_clang.play()


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, img='images/objects/platform.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class AnimatedMob(pygame.sprite.Sprite):
    def update_animation(self):
        self.anim_counter += 1
        if self.anim_counter >= FPS:
            self.anim_counter = 0

        if self.direction == 1:
            frame = self.anim_counter % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = self.anim_counter % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]


class Enemy(AnimatedMob):
    def __init__(self, x, y, distance, img=None, gif=None, frames_num=None, scale=None):
        super().__init__()

        self.start = x
        self.stop = self.start + distance
        self.direction = 1
        self.speed = 2

        if gif and frames_num:
            self.walking_frames_l = utils.get_anim_frames(gif, frames_num, scale)
            self.walking_frames_r = []

            for img in self.walking_frames_l:
                img = pygame.transform.flip(img, True, False)
                self.walking_frames_r.append(img)

            self.image = self.walking_frames_r[0]

            self.anim_counter = 0

        elif img:
            self.image = pygame.image.load(img).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1

        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1

        self.rect.x += self.direction * self.speed
        self.update_animation()


class Elf(AnimatedMob):
    def __init__(self, x, y, distance, gif, frames_num, scale=None):
        super().__init__()

        self.start = x
        self.stop = self.start + distance
        self.direction = 1
        self.speed = 5
        self.moving = False

        self.walking_frames_l = utils.get_anim_frames(gif, frames_num, scale)
        self.walking_frames_r = []

        for img in self.walking_frames_l:
            img = pygame.transform.flip(img, True, False)
            self.walking_frames_r.append(img)

        self.image = self.walking_frames_r[0]

        self.anim_counter = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        if self.moving:
            if self.rect.x <= self.stop:
                self.rect.x += self.speed

            self.rect.x += self.direction * self.speed
        self.update_animation()
