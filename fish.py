import pygame
import random

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Рыбалка")

# Определяем цвета
blue = (0, 0, 255)  # Цвет воды
green = (0, 255, 0)  # Цвет рыбы
white = (255, 255, 255)  # Цвет текста
black = (0, 0, 0)  # Цвет удочки

# Загружаем изображения
fishing_rod_image = pygame.Surface((10, 100))
fishing_rod_image.fill(black)

fish_image = pygame.Surface((30, 20))
fish_image.fill(green)

# Параметры игры
fishing_rod_x = width // 2
fishing_rod_y = height - 100
caught_fish = []
score = 0
font = pygame.font.Font(None, 36)
fall_speed = 5  # Скорость падения рыбы
fish_list = []  # Список рыб

# Создаем начальные рыбы
for _ in range(5):  # Создаем 5 рыб
    fish_x = random.randint(0, width - 30)
    fish_y = random.randint(-100, -30)  # Начальная позиция выше экрана
    fish_list.append([fish_x, fish_y])

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление удочкой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and fishing_rod_x > 0:
        fishing_rod_x -= 5
    if keys[pygame.K_RIGHT] and fishing_rod_x < width - 10:
        fishing_rod_x += 5

    # Проверка на ловлю рыбы
    for fish in fish_list:
        if (fishing_rod_x < fish[0] + 30 and fishing_rod_x + 10 > fish[0] and
                fishing_rod_y < fish[1] + 20 and fishing_rod_y + 100 > fish[1]):
            caught_fish.append(fish)  # Добавляем пойманную рыбу в список
            score += 1
            fish[0] = random.randint(0, width - 30)  # Сбросить рыбу на верх экрана
            fish[1] = random.randint(-100, -30)  # Начальная позиция выше экрана

    # Обновление позиции рыб
    for fish in fish_list:
        fish[1] += fall_speed  # Рыба падает вниз
        if fish[1] > height:  # Если рыба упала ниже экрана
            fish[0] = random.randint(0, width - 30)
            fish[1] = random.randint(-100, -30)  # Сбросить рыбу на верх экрана

    # Отрисовка
    screen.fill(blue)  # Цвет воды
    screen.blit(fishing_rod_image, (fishing_rod_x, fishing_rod_y))

    for fish in fish_list:
        screen.blit(fish_image, (fish[0], fish[1]))  # Отрисовка каждой рыбы

    # Отображение счета
    score_text = font.render(f"Счет: {score}", True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

