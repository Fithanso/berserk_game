import pygame
from constants import *


class TopPanel:

    def __init__(self, x=5, y=5):
        self.x = x
        self.y = y
        self.width = WIN_WIDTH - 2 * x
        self.fps_counter = 0
        self.seconds_counter = heal_cd

        self.display_elves = False

        self.lives = 3

        self.lives_img = pygame.image.load('images/objects/red_behelit.png').convert_alpha()
        self.lives_img = pygame.transform.scale(self.lives_img, (90, 90))
        self.lives_img_rect = self.lives_img.get_rect()
        self.lives_img_rect.y = y
        self.lives_img_rect.x = x

        self.cooldown_label = FONT.render(str(self.seconds_counter), True, WHITE)
        self.cooldown_rect = self.cooldown_label.get_rect()
        self.cooldown_rect.x = x + 400
        self.cooldown_rect.y = y + 30
        
        self.puck_img = pygame.image.load('images/puck/1.png').convert_alpha()
        self.puck_img = pygame.transform.scale(self.puck_img, (50, 50))
        self.puck_img_rect = self.puck_img.get_rect()
        self.puck_img_rect.y = y + 20
        self.puck_img_rect.x = x + 290
        
        self.ivalera_img = pygame.image.load('images/ivalera/1.png').convert_alpha()
        self.ivalera_img = pygame.transform.scale(self.ivalera_img, (50, 50))
        self.ivalera_img_rect = self.ivalera_img.get_rect()
        self.ivalera_img_rect.y = y + 20
        self.ivalera_img_rect.x = x + 340

    def restart_timer(self):
        self.seconds_counter = heal_cd

    def update(self, lives):
        self.fps_counter += 1
        if self.fps_counter >= FPS:
            self.fps_counter = 0
            self.seconds_counter -= 1

        self.lives = lives

        self.cooldown_label = FONT.render(str(self.seconds_counter), True, WHITE)

    def draw(self, screen):
        for i in range(self.lives):
            screen.blit(self.lives_img, (self.x + i*80, self.y))

        if self.display_elves:
            screen.blit(self.puck_img, self.puck_img_rect)
            screen.blit(self.ivalera_img, self.ivalera_img_rect)
            if self.seconds_counter >= 0:
                screen.blit(self.cooldown_label, self.cooldown_rect)

