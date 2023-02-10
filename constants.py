import pygame
pygame.font.init()

WIN_WIDTH = 1430
WIN_HEIGHT = 800
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (25, 138, 17)
BLUE = (20, 68, 140)
YELLOW = (156, 145, 47)
GRAY = (200, 200, 200)

FONT = pygame.font.SysFont('Arial', 32, True)

start_text_1 = FONT.render('PRESS SPACE TO START GAME', 1, (255, 255, 255))
rules_text_1 = FONT.render('move - wasd', 1, (255, 255, 255))
rules_text_2 = FONT.render('attack - space', 1, (255, 255, 255))
rules_text_3 = FONT.render('e - call for elves (lvls 2&3)', 1, (255, 255, 255))
music_label_1 = FONT.render('MUSIC BY', 1, (255, 255, 255))
music_label_2 = FONT.render('SUSUMU HIRASAWA', 1, (255, 255, 255))
death_text = FONT.render('YOUR STORY TRAGICALLY ENDED', 1, (255, 255, 255))

heal_cd = 10

scene_1_platforms = [
    [850, 630],
    [950, 630],
    [1050, 630],
    [1150, 630],

    [300, 500],
    [400, 500],
    [500, 500],
    [600, 500],

    [0, 450],
    [100, 450],

    [300, 300],
    [400, 300],
    [500, 300],
    [600, 300],

    [850, 250],
    [950, 250],
    [1050, 250],
    [1150, 250],
    [1250, 250],

]

scene_2_platforms = [
    [700, 630],
    [800, 630],
    [900, 630],
    [1000, 630],

    [150, 550],

    [400, 550],

    [0, 430],

    [200, 250],

    [450, 250],

    [700, 250],

    [800, 250],
    [900, 250],
    [1000, 250],

]

scene_2_serpico_coords = [
    [200, 155, 50],

    [450, 155, 50],

    [700, 155, 200],
]

scene_3_platforms = [
    [500, 630],
    [600, 630],
    [700, 630],
    [800, 630],

    [1050, 500],

    [800, 350],

    [600, 250],

    [500, 250],
    [400, 250],
    [300, 250],
    [200, 250],

]