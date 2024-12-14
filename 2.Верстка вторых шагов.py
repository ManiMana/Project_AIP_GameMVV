import pygame
import sys

# Константы
WIDTH, HEIGHT = 1440, 810  # Увеличенные размеры окна
THRESHOLD_GOOD = 50
INITIAL_POINTS = 100  # Начальное количество очков

# Цвета
WHITE = (255, 255, 255)

class VirtualVirusApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Мой виртуальный вирус")

        # Загружаем изображение фона и изменяем его размер
        self.background_image = pygame.transform.scale(pygame.image.load("fon.png"), (WIDTH, HEIGHT))

        # Загружаем изображение аватара и изменяем его размер
        self.avatar_image = pygame.transform.scale(pygame.image.load("avatarka.png"), (70, 70))

        # Загружаем изображение персонажа и изменяем его размер
        self.character_image = pygame.transform.scale(pygame.image.load("character.png"),(500, 500))  # Измените размер по необходимости

        # Параметры вируса
        self.stats = {
            "Здоровье": 0,
            "Голод": 0,
            "Счастье": 0,
            "Чистота": 0,
            "Сон": 0,
        }

        # Имя, уровень и количество очков
        self.player_name = "Игрок"
        self.player_level = 1
        self.player_points = INITIAL_POINTS

        # Загружаем иконки и увеличиваем их размер
        self.icons = {
            "Здоровье": {
                "good": pygame.transform.scale(pygame.image.load("health_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("health_bad.png"), (70, 70)),
            },
            "Голод": {
                "good": pygame.transform.scale(pygame.image.load("hunger_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("hunger_bad.png"), (70, 70)),
            },
            "Счастье": {
                "good": pygame.transform.scale(pygame.image.load("happiness_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("happiness_bad.png"), (70, 70)),
            },
            "Чистота": {
                "good": pygame.transform.scale(pygame.image.load("clean_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("clean_bad.png"), (70, 70)),
            },
            "Сон": {
                "good": pygame.transform.scale(pygame.image.load("sleep_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("sleep_bad.png"), (70, 70)),
            },
        }

        self.font = pygame.font.Font(None, 36)
        self.buttons = {
            "Лечить": lambda: self.update_stat("Здоровье", 5),
            "Кормить": lambda: self.update_stat("Голод", 5),
            "Играть": lambda: self.update_stat("Счастье", 5),
            "Очистить": lambda: self.update_stat("Чистота", 5),
            "Спать": lambda: self.update_stat("Сон", 5),
        }

        self.run()

    def run(self):
        while True:
            self.handle_events()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        # Отображаем фон
        self.screen.blit(self.background_image, (0, 0))

        # Рисуем аватар в левом верхнем углу
        self.screen.blit(self.avatar_image, (20, 20))  # Положение аватара
        name_text = self.font.render(self.player_name, True, (0, 0, 0))
        level_text = self.font.render(f"Уровень: {self.player_level}", True, (0, 0, 0))
        points_text = self.font.render(f"Очки: {self.player_points}", True, (0, 0, 0))
        self.screen.blit(name_text, (100, 20))  # Положение имени
        self.screen.blit(level_text, (100, 50))  # Положение уровня
        self.screen.blit(points_text, (100, 80))  # Положение очков
        # Рисуем иконки и шкалы по верхней грани окна
        icon_start_x = 300  # Начальная позиция для иконок состояния
        icon_spacing = (WIDTH - icon_start_x) // len(self.stats)  # Расстояние между иконками

        for i, (stat, value) in enumerate(self.stats.items()):
            icon = self.icons[stat]["good"] if value >= THRESHOLD_GOOD else self.icons[stat]["bad"]
            icon_x = icon_start_x + i * icon_spacing  # Расположение иконок по верхней грани окна
            self.screen.blit(icon, (icon_x, 20))  # Рисуем иконку (высота 100)
            pygame.draw.rect(self.screen, (0, 0, 0), (icon_x, 100, 100, 20), 2)  # Увеличенная шкала
            pygame.draw.rect(self.screen, (0, 255, 0), (icon_x, 100, value, 20))  # Увеличенная шкала

            # Отображаем значение
            value_text = self.font.render(str(value), True, (0, 0, 0))
            self.screen.blit(value_text, (icon_x + 110, 98))

            # Подпись к иконке
            label_text = self.font.render(stat.capitalize(), True, (0, 0, 0))
            self.screen.blit(label_text, (icon_x, 120))

        # Рисуем кнопки внизу экрана, прямо под иконками
        button_width = 110
        button_height = 40
        button_spacing = (WIDTH - 50 * 2 - button_width * len(self.buttons)) // (len(self.buttons) - 1)

        for i, (text, action) in enumerate(self.buttons.items()):
            button_x = icon_start_x + i * icon_spacing  # Расположение кнопок прямо под иконками
            button_rect = pygame.Rect(button_x, HEIGHT - 45, button_width, button_height)
            pygame.draw.rect(self.screen, (205, 231, 238), button_rect)  # Измененный цвет кнопки
            button_text = self.font.render(text, True, (5, 82, 123))  # Измененный цвет текста
            self.screen.blit(button_text, (button_rect.x + 5, button_rect.y + 5))

            # Проверка нажатия кнопки
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:  # Если кнопка мыши нажата
                    action()  # Вызываем действие, связанное с кнопкой
                    pygame.time.delay(200)  # Задержка, чтобы избежать многократного нажатия
                    break  # Выходим из цикла, чтобы избежать повторного срабатывания

        # Рисуем персонажа в центре экрана
        character_x = (WIDTH - self.character_image.get_width()) // 2
        character_y = (HEIGHT - self.character_image.get_height()) // 2 + 40
        self.screen.blit(self.character_image, (character_x, character_y))

        pygame.display.flip()  # Обновляем экран

    def update_stat(self, stat, value):
        """Обновление значения шкалы."""
        cost = 5  # Стоимость повышения состояния
        if self.player_points >= cost:  # Проверка, достаточно ли очков
            self.stats[stat] = min(self.stats[stat] + value, 100)  # Увеличиваем значение, не превышая 100
            self.player_points -= cost  # Уменьшаем количество очков


# Запуск приложения
if __name__ == "__main__":
    VirtualVirusApp()


