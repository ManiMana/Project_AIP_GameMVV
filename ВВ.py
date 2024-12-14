import pygame
import sys
import json
import os

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

        self.last_update_time = pygame.time.get_ticks()

        self.buttons = {
            "Лечить": lambda: self.update_stat("Здоровье", 5),
            "Кормить": lambda: self.update_stat("Голод", 5),
            "Играть": lambda: self.update_stat("Счастье", 5),
            "Очистить": lambda: self.update_stat("Чистота", 5),
            "Спать": lambda: self.update_stat("Сон", 5),
        }

        # Инициализация иконок
        self.icons = self.load_icons()

        # Остальная инициализация
        self.background_image = self.load_image("fon.png", (WIDTH, HEIGHT))
        self.avatar_image = self.load_image("avatarka.png", (70, 70))
        self.character_image = self.load_image("character.png", (500, 750))

        self.stats = {
            "Здоровье": 0,
            "Голод": 0,
            "Счастье": 0,
            "Чистота": 0,
            "Сон": 0,
        }

        self.player_name = "Игрок"
        self.player_level = 1
        self.player_points = INITIAL_POINTS

        self.font = pygame.font.Font(None, 36)
        self.run()

    def load_icons(self):
        """Загрузка иконок для состояний."""
        icons = {}
        for stat in ["Здоровье", "Голод", "Счастье", "Чистота", "Сон"]:
            icons[stat] = {
                "good": pygame.transform.scale(pygame.image.load(f"{stat.lower()}_good.png"), (70, 70)),
                "middle": pygame.transform.scale(pygame.image.load(f"{stat.lower()}_middle.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load(f"{stat.lower()}_bad.png"), (70, 70)),
            }
        return icons

    def run(self):
        self.load_data()  # Загрузить данные игрока
        self.show_welcome_screen()  # Показать экран приветствия

    def main_game_loop(self):
        while True:
            self.handle_events()  # Обработка событий

            # Проверка времени
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= 60000:  # 60 секунд
                self.update_stats_over_time()  # Обновление состояний со временем
                self.last_update_time = current_time  # Обновляем время последнего обновления

            self.draw()  # Отрисовка элементов на экране

    def update_stats_over_time(self):
        """Уменьшение значений состояний со временем."""
        for stat in self.stats:
            if stat != "Здоровье":  # Здоровье не уменьшается
                self.stats[stat] = max(self.stats[stat] - 1, 0)  # Уменьшаем значение, не опуская ниже 0

    def show_welcome_screen(self):
        if self.player_name == "Игрок":  # Если аккаунта нет
            self.create_account_screen()
        else:  # Если аккаунт уже существует
            self.existing_account_screen()

    def create_account_screen(self):
        input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        welcome_text = self.font.render("Добро пожаловать в игру!", True, (0, 0, 0))
        start_text = self.font.render("Введите имя вашего питомца:", True, (0, 0, 0))
        exit_text = self.font.render("Выйти из игры", True, (0, 0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN and text:  # Если имя не пустое
                            self.player_name = text
                            self.stats = {stat: 50 for stat in self.stats}  # Начальные значения для питомца
                            self.save_data()  # Сохраняем данные после создания питомца
                            self.main_game_loop()  # Переход к основной игре
                            return  # Выходим из окна создания аккаунта
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            # Отображаем экран создания аккаунта
            self.screen.fill(WHITE)
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, HEIGHT // 2 - 100))
            self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 50))
            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            # Отображаем кнопку "Выйти из игры"
            exit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 40)
            pygame.draw.rect(self.screen, (205, 231, 238), exit_button_rect)
            self.screen.blit(exit_text, (exit_button_rect.x + 5, exit_button_rect.y + 5))

            # Проверка нажатия кнопки "Выйти из игры"
            if exit_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.exit_game()  # Вызов метода выхода из игры

            pygame.display.flip()

    def existing_account_screen(self):
        welcome_text = self.font.render(f"Добро пожаловать, {self.player_name}!", True, (0, 0, 0))
        level_text = self.font.render(f"Уровень: {self.player_level}", True, (0, 0, 0))
        continue_text = self.font.render("Нажмите 'C' для продолжения", True, (0, 0, 0))
        exit_text = self.font.render("Выйти из игры", True, (0, 0, 0))

        delete_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 40)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # Нажатие 'C' для продолжения игры
                        self.main_game_loop()  # Переход к основной игре
                        return  # Выходим из окна приветствия
                    elif event.key == pygame.K_ESCAPE:  # Нажатие 'ESC' для выхода
                        self.exit_game()

            # Отображаем экран приветствия
            self.screen.fill(WHITE)
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, HEIGHT // 2 - 100))
            self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 50))
            self.screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 50))
            self.screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 100))

            # Отображаем кнопку "Удалить аккаунт"
            pygame.draw.rect(self.screen, (205, 231, 238), delete_button_rect)
            delete_button_text = self.font.render("Удалить аккаунт", True, (5, 82, 123))
            self.screen.blit(delete_button_text, (delete_button_rect.x + 5, delete_button_rect.y + 5))

            # Проверка нажатия кнопки "Удалить аккаунт"
            if delete_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.delete_account()  # Удаление аккаунта

            pygame.display.flip()  # Обновляем экран

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
            if value >= 68:
                icon = self.icons[stat]["good"]
            elif value >= 34:
                icon = self.icons[stat]["middle"]
            else:
                icon = self.icons[stat]["bad"]
            icon_x = icon_start_x + i * icon_spacing
            self.screen.blit(icon, (icon_x, 20))

            # Рисуем шкалу состояния
            pygame.draw.rect(self.screen, (0, 0, 0), (icon_x, 100, 70, 20), 2)  # Увеличенная шкала
            pygame.draw.rect(self.screen, (0, 255, 0), (icon_x, 100, value * 0.7, 20))  # Увеличенная шкала

            # Отображаем значение
            value_text = self.font.render(str(value), True, (0, 0, 0))
            self.screen.blit(value_text, (icon_x + 75, 98))

            # Подпись к иконке
            label_text = self.font.render(stat.capitalize(), True, (0, 0, 0))
            self.screen.blit(label_text, (icon_x, 120))

        # Рисуем кнопки состояния внизу экрана
        button_width = 110
        button_height = 40
        button_spacing = (WIDTH - 50 * 2 - button_width * len(self.buttons)) // (len(self.buttons) - 1)

        for i, (text, action) in enumerate(self.buttons.items()):
            button_x = icon_start_x + i * button_spacing  # Расположение кнопок прямо под иконками
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

        # Рисуем кнопки под аватаром
        button_y = 130  # Положение кнопок под аватаром

        # Кнопка "Выйти из игры"
        exit_button_rect = pygame.Rect(20, button_y, 200, button_height)
        pygame.draw.rect(self.screen, (205, 231, 238), exit_button_rect)
        exit_button_text = self.font.render("Выйти из игры", True, (5, 82, 123))
        self.screen.blit(exit_button_text, (exit_button_rect.x + 5, exit_button_rect.y + 5))

        # Кнопка "Удалить аккаунт"
        delete_button_rect = pygame.Rect(20, button_y + button_height + 10, 230, button_height)
        pygame.draw.rect(self.screen, (205, 231, 238), delete_button_rect)
        delete_button_text = self.font.render("Удалить аккаунт", True, (5, 82, 123))
        self.screen.blit(delete_button_text, (delete_button_rect.x + 5, delete_button_rect.y + 5))

        # Проверка нажатия кнопок
        mouse_pos = pygame.mouse.get_pos()
        if exit_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.exit_game()  # Выход из игры
        elif delete_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.delete_account()  # Удаление аккаунта

        # Рисуем персонажа в центре экрана
        character_x = (WIDTH - self.character_image.get_width()) // 2
        character_y = (HEIGHT - self.character_image.get_height()) // 2 + 60
        self.screen.blit(self.character_image, (character_x, character_y))

        pygame.display.flip()  # Обновляем экран

    def update_stat(self, stat, value):
        """Обновление значения шкалы."""
        cost = 5  # Стоимость повышения состояния
        if self.player_points >= cost:  # Проверка, достаточно ли очков
            self.stats[stat] = min(self.stats[stat] + value, 100)  # Увеличиваем значение, не превышая 100
            self.player_points -= cost  # Уменьшаем количество очков
            self.save_data()  # Сохраняем данные после обновления

    def save_data(self):
        """Сохранение данных игрока в файл."""
        data = {
            "player_name": self.player_name,
            "player_level": self.player_level,
            "player_points": self.player_points,
            "stats": self.stats,
            "last_update_time": self.last_update_time,
        }
        with open("player_data.json", "w") as f:
            json.dump(data, f)

    def exit_game(self):
        """Выход из игры с сохранением данных."""
        self.save_data()  # Сохраняем данные перед выходом
        pygame.quit()
        sys.exit()

    def delete_account(self):
        """Удаление аккаунта и данных игрока."""
        if os.path.exists("player_data.json"):
            os.remove("player_data.json")  # Удаляем файл с данными
        self.player_name = "Игрок"  # Сбрасываем имя
        self.player_level = 1  # Сбрасываем уровень
        self.player_points = INITIAL_POINTS  # Сбрасываем очки
        self.stats = {stat: 0 for stat in self.stats}  # Сбрасываем статистику
        self.show_welcome_screen()  # Показать экран приветствия снова

    def load_data(self):
        """Загрузка данных игрока из файла."""
        try:
            with open("player_data.json", "r") as f:
                data = json.load(f)
                self.player_name = data["player_name"]
                self.player_level = data["player_level"]
                self.player_points = data["player_points"]
                self.stats = data["stats"]
                self.last_update_time = data.get("last_update_time", pygame.time.get_ticks())

                # Вычисляем, сколько времени прошло с последнего обновления
                current_time = pygame.time.get_ticks()
                elapsed_time = (current_time - self.last_update_time) / 1000  # Время в секундах

                # Уменьшаем значения состояний, кроме здоровья, на основе прошедшего времени
                minutes_passed = int(elapsed_time // 60)
                for stat in self.stats:
                    if stat != "Здоровье":
                        self.stats[stat] = max(self.stats[stat] - minutes_passed, 0)  # Уменьшаем значение
                        self.stats[stat] = min(self.stats[stat], 100)  # Убедитесь, что значение не превышает 100

                # Обновляем last_update_time после уменьшения
                self.last_update_time = pygame.time.get_ticks()

        except FileNotFoundError:
            print("Файл с данными не найден. Начинаем новую игру.")
        except json.JSONDecodeError:
            print("Ошибка при чтении файла данных. Начинаем новую игру.")

    def load_image(self, filename, size=None):
        """Загрузка изображения с обработкой ошибок."""
        try:
            image = pygame.image.load(filename)
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"Не удалось загрузить изображение {filename}: {e}")
            return None  # Возвращаем None, если изображение не удалось загрузить


# Запуск приложения
if __name__ == "__main__":
    VirtualVirusApp()
