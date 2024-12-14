import pygame
import sys

# Константы
WIDTH, HEIGHT = 800, 600  # Увеличенные размеры окна
THRESHOLD_GOOD = 50

# Цвета
WHITE = (255, 255, 255)

class VirtualVirusApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Мой виртуальный вирус")

        # Загружаем изображение фона и изменяем его размер
        self.background_image = pygame.transform.scale(pygame.image.load("fon.png"), (1440, 810))

        # Параметры вируса
        self.stats = {
            "health": 0,
            "hunger": 0,
            "happiness": 0,
            "cleanliness": 0,
            "sleep": 0,
        }

        # Загружаем иконки и увеличиваем их размер
        self.icons = {
            "health": {
                "good": pygame.transform.scale(pygame.image.load("health_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("health_bad.png"), (70, 70)),
            },
            "hunger": {
                "good": pygame.transform.scale(pygame.image.load("hunger_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("hunger_bad.png"), (70, 70)),
            },
            "happiness": {
                "good": pygame.transform.scale(pygame.image.load("happiness_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("happiness_bad.png"), (70, 70)),
            },
            "cleanliness": {
                "good": pygame.transform.scale(pygame.image.load("clean_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("clean_bad.png"), (70, 70)),
            },
            "sleep": {
                "good": pygame.transform.scale(pygame.image.load("sleep_good.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("sleep_bad.png"), (70, 70)),
            },
        }

        self.font = pygame.font.Font(None, 36)
        self.buttons = {
            "Спать": lambda: self.update_stat("sleep", 5),        # Под иконкой сна
            "Очистить": lambda: self.update_stat("cleanliness", 5),  # Под иконкой чистоты
            "Кормить": lambda: self.update_stat("hunger", 5),     # Под иконкой голода
            "Играть": lambda: self.update_stat("happiness", 5),    # Под иконкой счастья
            "Лечить": lambda: self.update_stat("health", 5),      # Под иконкой здоровья
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

        # Рисуем иконки и шкалы по верхней грани окна
        for i, (stat, value) in enumerate(self.stats.items()):
            icon = self.icons[stat]["good"] if value >= THRESHOLD_GOOD else self.icons[stat]["bad"]
            self.screen.blit(icon, (50 + i * 150, 20))  # Расположение иконок по верхней грани окна
            pygame.draw.rect(self.screen, (0, 0, 0), (50 + i * 150, 100, 100, 20), 2)  # Увеличенная шкала
            pygame.draw.rect(self.screen, (0, 255, 0), (50 + i * 150, 100, value, 20))  # Увеличенная шкала

            # Отображаем значение
            value_text = self.font.render(str(value), True, (0, 0, 0))
            self.screen.blit(value_text, (50 + i * 150, 130))

        # Рисуем кнопки внизу экрана
        for i, (text, action) in enumerate(self.buttons.items()):
            button_rect = pygame.Rect(50 + i * 150, HEIGHT - 60, 140, 40)  # Расположение кнопок внизу
            pygame.draw.rect(self.screen, (0, 0, 255), button_rect)  # Рисуем кнопку
            button_text = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(button_text, (button_rect.x + 5, button_rect.y + 5))

            # Проверка нажатия кнопки
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:  # Если кнопка мыши нажата
                    action()  # Вызываем действие, связанное с кнопкой
                    pygame.time.delay(200)  # Задержка, чтобы избежать многократного нажатия
                    break  # Выходим из цикла, чтобы избежать повторного срабатывания

        pygame.display.flip()  # Обновляем экран

    def update_stat(self, stat, value):
        """Обновление значения шкалы."""
        self.stats[stat] = min(self.stats[stat] + value, 100)  # Увеличиваем значение, не превышая 100

# Запуск приложения
if __name__ == "__main__":
    VirtualVirusApp()

