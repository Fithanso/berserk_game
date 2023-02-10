import pygame
import random


# Настройка игрового окна
def init(caption):
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    return screen, clock


WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 30
# цвета    R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

screen, clock = init('Гонки')


# Здесь можно писать код :)
class Block(pygame.sprite.Sprite):
    def __init__(self, color, size=30, speed=5):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIN_WIDTH)
        self.rect.y = random.randrange(WIN_HEIGHT)
        self.speed = speed

    def update(self):
        # Подвинуть блок "навстречу" автомобилю
        self.rect.y += self.speed
        if self.rect.y > WIN_WIDTH:
            self.rect.y = 0
            self.rect.x = random.randrange(WIN_WIDTH)


# Создаем группы спрайтов:
block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# Создаем блоки - препятствия и добавляем их в группы:
for i in range(10):
    block = Block(BLACK)
    block_list.add(block)
    all_sprites_list.add(block)

# Создаем автомобиль игрока
player = Block(RED)
player.rect.x = WIN_WIDTH // 2
player.rect.y = WIN_HEIGHT - 35

# Добавляем автомобиль в группу all_sprites_list:
all_sprites_list.add(player)
run = True

while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            run = False

    # получаем информацию о положении мыши:
    pos = pygame.mouse.get_pos()

    # перемещаем спрайт игрока
    if run:
        player.rect.x = pos[0] - player.rect.width // 2

    # проверяем столкновения
    if pygame.sprite.spritecollideany(player, block_list):
        run = False

    # начало прорисовки окна
    screen.fill(GRAY)

    # рисуем на экране все спрайты:
    block_list.update()
    all_sprites_list.draw(screen)

    # конец прорисовки окна
    pygame.display.update()
    clock.tick(FPS)
