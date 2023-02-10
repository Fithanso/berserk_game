import random

import pygame
import time

from constants import *
import objects
import menu


class Game:
    bg_start = pygame.image.load("images/bgs/berserk_poster.png")
    bg_death = pygame.image.load("images/bgs/guts_sad.jpg")
    bg_finish = pygame.image.load("images/bgs/guts_finish.png")
    behelit_track = pygame.mixer.Sound("sounds/behelit_music.mp3")
    haiyo_track = pygame.mixer.Sound("sounds/haiyo.mp3")
    sign2_track = pygame.mixer.Sound("sounds/sign2.mp3")
    guts_theme_track = pygame.mixer.Sound("sounds/guts_theme.mp3")
    elf_sound = pygame.mixer.Sound("sounds/bird_flying.mp3")

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("It's berserkin time!")
        self.clock = pygame.time.Clock()

        self.all_sprite_list = pygame.sprite.Group()
        self.single_sword_sprite = pygame.sprite.Group()
        self.elves_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()

        self.state = 'START'
        self.scene = 1
        self.max_scenes = 3

        self.player = None
        self.platform_list = None

        self.top_panel = menu.TopPanel()
        self.music_channel = pygame.mixer.Channel(5)
        self.music_channel.set_volume(0.3)

        self.create_elves()

    def create_elves(self):
        puck = objects.Elf(-50, 300, WIN_WIDTH+50, 'puck', 4)
        self.elves_list.add(puck)
        self.all_sprite_list.add(puck)

        ivalera = objects.Elf(-50, 400, WIN_WIDTH+50, 'ivalera', 4)
        self.elves_list.add(ivalera)
        self.all_sprite_list.add(ivalera)

    def create_scene_1(self):
        self.bg = pygame.image.load("images/bgs/bg1.png")
        self.player = objects.Player(20, 700, 0, 'guts_1', 17)

        sword_image = pygame.image.load('images/objects/sword_1.png').convert_alpha()
        sword_image = pygame.transform.rotate(sword_image, -90)
        sword_image = pygame.transform.scale(sword_image, (200, 30))

        sword = objects.PlayerSword(self.player.rect.x + self.player.rect.width - 40, self.player.rect.y + 30,
                                    sword_image)

        self.player.sword = sword
        self.all_sprite_list.add(self.player)
        self.single_sword_sprite.add(sword)

        self.platform_list = pygame.sprite.Group()
        self.create_platforms(scene_1_platforms)
        self.player.platforms = self.platform_list
        self.player.elves = self.elves_list

        self.enemy_list = pygame.sprite.Group()

        griffith = objects.Enemy(820, 130, 380, gif='griffith_1', frames_num=17)
        self.enemy_list.add(griffith)
        self.all_sprite_list.add(griffith)

        casca = objects.Enemy(300, 400, 300, gif='casca_1', frames_num=18)
        self.enemy_list.add(casca)
        self.all_sprite_list.add(casca)

        self.player.enemies = self.enemy_list

        self.music_channel.play(self.behelit_track)

    def create_scene_2(self):
        self.music_channel.stop()
        self.music_channel.play(self.haiyo_track)
        self.top_panel.display_elves = True
        self.top_panel.restart_timer()

        self.bg = pygame.image.load("images/bgs/bg2.png")
        self.all_sprite_list.empty()
        self.single_sword_sprite.empty()
        self.player = objects.Player(20, 700, 1, 'guts_2', 18)

        sword_image = pygame.image.load('images/objects/sword_2.png').convert_alpha()
        sword_image = pygame.transform.rotate(sword_image, -45)
        sword_image = pygame.transform.scale(sword_image, (170, 200))

        sword = objects.PlayerSword(self.player.rect.x + self.player.rect.width - 30,
                                    self.player.rect.y - 50, sword_image)
        self.player.sword = sword
        self.all_sprite_list.add(self.player)
        self.single_sword_sprite.add(sword)

        self.platform_list = pygame.sprite.Group()
        self.create_platforms(scene_2_platforms)
        self.player.platforms = self.platform_list
        self.player.elves = self.elves_list

        self.enemy_list = pygame.sprite.Group()

        farnese = objects.Enemy(680, 510, 380, gif='farnese', frames_num=9)
        self.enemy_list.add(farnese)
        self.all_sprite_list.add(farnese)

        for info_list in scene_2_serpico_coords:
            serpico = objects.Enemy(info_list[0], info_list[1], info_list[2], gif='serpico', frames_num=10)
            self.enemy_list.add(serpico)
            self.all_sprite_list.add(serpico)

        self.player.enemies = self.enemy_list

    def create_scene_3(self):
        self.music_channel.stop()
        self.music_channel.play(self.sign2_track)
        self.bg = pygame.image.load("images/bgs/bg3.png")
        self.all_sprite_list.empty()
        self.single_sword_sprite.empty()
        self.player = objects.Player(20, 700, 1, 'guts_3', 18)

        sword_image = pygame.image.load('images/objects/sword_2.png').convert_alpha()
        sword_image = pygame.transform.rotate(sword_image, -45)
        sword_image = pygame.transform.scale(sword_image, (170, 200))

        sword = objects.PlayerSword(self.player.rect.x + self.player.rect.width - 30,
                                    self.player.rect.y - 50, sword_image)
        self.player.sword = sword
        self.all_sprite_list.add(self.player)
        self.single_sword_sprite.add(sword)

        self.platform_list = pygame.sprite.Group()
        self.create_platforms(scene_3_platforms)
        self.player.platforms = self.platform_list
        self.player.elves = self.elves_list

        self.enemy_list = pygame.sprite.Group()

        femto = objects.Enemy(200, 160, 400, gif='femto', frames_num=18)
        self.enemy_list.add(femto)
        self.all_sprite_list.add(femto)

        zodd = objects.Enemy(400, 400, 300, gif='zodd', frames_num=8, scale=(250, 200))
        self.enemy_list.add(zodd)
        self.all_sprite_list.add(zodd)

        self.player.enemies = self.enemy_list

    def create_platforms(self, coords):

        for coord in coords:
            platform = objects.Platform(coord[0], coord[1])
            self.platform_list.add(platform)
            self.all_sprite_list.add(platform)

    def move_elves(self):
        self.elf_sound.play()
        for elf in self.elves_list:
            elf.rect.y = random.randint(WIN_HEIGHT//2, WIN_HEIGHT-50)
            elf.moving = True

    def handle_scene(self, event):
        if self.state == "GAME":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.go_left()
                elif event.key == pygame.K_d:
                    self.player.go_right()
                elif event.key == pygame.K_w:
                    self.player.jump()
                elif event.key == pygame.K_SPACE:
                    self.player.attack()
                elif event.key == pygame.K_e:
                    if self.scene > 1 and self.top_panel.seconds_counter <= 0:
                        self.move_elves()
                        self.top_panel.update(self.player.lives)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_d and self.player.change_x > 0:
                    self.player.stop()

        elif self.state == "DEATH":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "GAME"
                    self.create_scene_1()

        elif self.state == "START":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "GAME"
                    self.create_scene_1()

    def draw_scene(self):
        self.screen.fill(BLACK)
        if self.state == "GAME":

            self.screen.blit(self.bg, (0, 0))

            self.all_sprite_list.draw(self.screen)
            self.elves_list.draw(self.screen)

            if self.player.attacking:
                self.single_sword_sprite.draw(self.screen)

            self.top_panel.update(self.player.lives)
            self.top_panel.draw(self.screen)

        elif self.state == "START":
            self.screen.blit(self.bg_start, (WIN_WIDTH // 2 - 300, 0))
            self.screen.blit(start_text_1, (0, 500))
            self.screen.blit(rules_text_1, (0, 200))
            self.screen.blit(rules_text_2, (0, 300))
            self.screen.blit(rules_text_3, (0, 400))
            self.screen.blit(music_label_1, (1100, 400))
            self.screen.blit(music_label_2, (1100, 500))

        elif self.state == "DEATH":
            self.screen.blit(self.bg_death, (WIN_WIDTH // 2 - 300, 0))
            self.screen.blit(death_text, (0, 500))
            self.music_channel.stop()

        elif self.state == "FINISH":
            self.screen.blit(self.bg_finish, (0, 50))

    def detect_collisions(self):
        for enemy in self.enemy_list:
            if pygame.sprite.collide_rect(enemy, self.player.sword) and self.player.attacking:
                enemy.kill()

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

                self.handle_scene(event)

            if self.state == "GAME":
                self.all_sprite_list.update()
                self.elves_list.update()
                if self.player.rect.x > WIN_WIDTH - 100 and self.player.rect.y > WIN_HEIGHT - 200:
                    if len(self.enemy_list) == 0:
                        self.scene += 1
                        if self.scene > self.max_scenes:
                            self.state = "FINISH"
                            self.music_channel.stop()
                            self.music_channel.play(self.guts_theme_track)
                            continue

                        getattr(self, f'create_scene_{self.scene}')()

                if self.player.lives == 0:
                    self.state = "DEATH"

                for elf in self.elves_list:
                    if elf.rect.x > elf.stop:
                        elf.moving = False
                        elf.rect.x = -50
                        self.top_panel.restart_timer()
                        break

                self.detect_collisions()
            self.draw_scene()
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()


game = Game()
game.run()
