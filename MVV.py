import os
import json
import time
import pygame
import sys

# Константы
WIDTH, HEIGHT = 1440, 810  # Увеличенные размеры окна
INITIAL_POINTS = 100  # Начальное количество очков

# Цвета
WHITE = (255, 255, 255)


class VirtualVirusApp:
    def __init__(self):

        self.timer = 0
        self.last_update_time = time.time()

        # Добавьте начальные параметры кастомизации
        self.current_hat = 0
        self.current_dress = 0
        self.current_shoes = 0

        self.load_customization()  # Загружаем кастомизацию при запуске


        self.buttons = {
            "Лечить": lambda: self.update_stat("Здоровье", 5),
            "Кормить": lambda: self.update_stat("Голод", 5),
            "Играть": lambda: self.update_stat("Счастье", 5),
            "Очистить": lambda: self.update_stat("Чистота", 5),
            "Спать": lambda: self.update_stat("Сон", 5),
        }

        # Инициализация иконок
        self.icons = {
            "Здоровье": {
                "good": pygame.transform.scale(pygame.image.load("health_good.png"), (70, 70)),
                "middle": pygame.transform.scale(pygame.image.load("health_middle.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("health_bad.png"), (70, 70)),
            },
            "Голод": {
                "good": pygame.transform.scale(pygame.image.load("hunger_good.png"), (70, 70)),
                "middle": pygame.transform.scale(pygame.image.load("hunger_middle.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("hunger_bad.png"), (70, 70)),
            },
            "Счастье": {
                "good": pygame.transform.scale(pygame.image.load("happiness_good.png"), (70, 70)),
                "middle": pygame.transform.scale(pygame.image.load("happiness_middle.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("happiness_bad.png"), (70, 70)),
            },
            "Чистота": {
                "good": pygame.transform.scale(pygame.image.load("clean_good.png"), (70, 70)),
                "middle": pygame.transform.scale(pygame.image.load("clean_middle.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("clean_bad.png"), (70, 70)),
            },
            "Сон": {
                "good": pygame.transform.scale(pygame.image.load("sleep_good.png"), (70, 70)),
                "middle": pygame.transform.scale(pygame.image.load("sleep_middle.png"), (70, 70)),
                "bad": pygame.transform.scale(pygame.image.load("sleep_bad.png"), (70, 70)),
            },
        }
        # Загрузка изображений для кастомизации
        self.hat_images = [
            self.load_image('assets/hat.png', (500, 750)),
            self.load_image('assets/cap.png', (500, 750)),
            self.load_image('assets/beret.png', (500, 750)),
            self.load_image('assets/glasses.png', (500, 750)),
            self.load_image('assets/shapka.png', (500, 750)),
            self.load_image('assets/empty.png', (500, 750)),
        ]
        self.dress_images = [
            self.load_image('assets/dress.png', (500, 750)),
            self.load_image('assets/kostum.png', (500, 750)),
            self.load_image('assets/pijama.png', (500, 750)),
            self.load_image('assets/t-shirt.png', (500, 750)),
            self.load_image('assets/uniform.png', (500, 750)),
            self.load_image('assets/empty.png', (500, 750)),
        ]
        self.shoe_images = [
            self.load_image('assets/shoes.png', (500, 750)),
            self.load_image('assets/boots.png', (500, 750)),
            self.load_image('assets/kedy.png', (500, 750)),
            self.load_image('assets/snickers.png', (500, 750)),
            self.load_image('assets/slippers.png', (500, 750)),
            self.load_image('assets/empty.png', (500, 750)),
        ]


        self.stats = {
            "Здоровье": 50,
            "Голод": 50,
            "Счастье": 50,
            "Чистота": 50,
            "Сон": 50,
        }

        self.player_name = "Игрок"
        self.player_level = 1
        self.player_points = INITIAL_POINTS

        self.font = pygame.font.Font(None, 36)
        self.load_data()

        self.run()

    def initialize_pygame(self):
        """Инициализация Pygame и создание окна."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Мой виртуальный вирус")
        self.background_image = self.load_image("fon.png", (WIDTH, HEIGHT))
        self.avatar_image = self.load_image("avatarka.png", (70, 70))
        self.character_image = self.load_image("assets/char.png", (500, 750))

    def run(self):

        self.initialize_pygame()  # Инициализация Pygame
        self.show_welcome_screen()  # Показать экран приветствия

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Очистка экрана
            self.screen.fill((255, 255, 255))

            # Отрисовка кастомизированного персонажа
            self.draw_customized_character()

            pygame.display.flip()

    def main_game_loop(self):
        while True:
            self.handle_events()  # Обработка событий

            # Проверка времени для уменьшения статов
            current_time = time.time()
            if current_time - self.last_update_time >= 60:  # Каждые 60 секунд
                self.update_stats_over_time()  # Уменьшаем значения состояний
                self.last_update_time = current_time  # Обновляем время последнего обновления

            self.draw()  # Отрисовка элементов на экране
            pygame.display.flip()  # Обновление окна

    def load_customization(self):
        """Загрузка данных кастомизации из файла."""
        if os.path.exists("customization_data.json"):
            with open("customization_data.json", "r") as f:
                customization_data = json.load(f)
                self.current_hat = customization_data.get("hat", 0)
                self.current_dress = customization_data.get("dress", 0)
                self.current_shoes = customization_data.get("shoes", 0)

    def show_welcome_screen(self):
        if self.player_name == "Игрок":  # Если аккаунта нет
            self.create_account_screen()
        else:  # Если аккаунт уже существует
            self.existing_account_screen()

    def open_customization(self):
        """Открыть экран кастомизации."""
        customization_screen = CustomizationScreen(self)
        customization_screen.run()

    def update_stats_over_time(self):
        """Уменьшение значений состояний, кроме здоровья, на 1 каждую минуту."""
        for stat in self.stats:
            if stat != "Здоровье":
                self.stats[stat] = max(self.stats[stat] - 1, 0)  # Уменьшаем значение, не опуская ниже 0

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
                        if event.key == pygame.K_RETURN:
                            if text:  # Если имя не пустое
                                self.player_name = text
                                self.stats = {stat: 50 for stat in self.stats}  # Начальные значения для питомца
                                self.save_data()  # Сохраняем данные после создания питомца
                                self.main_game_loop()  # Переход к основной игре
                                return  # Выходим из окна создания аккаунта
                            else:
                                continue  # Игнорируем нажатие Enter, если имя пустое
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

        # Кнопка "Удалить аккаунт"
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

    def add_points(self, points):
        """Добавляет очки к текущему значению."""
        self.player_points += points
        self.save_data()  # Сохраняем данные после добавления очков

    def load_customization(self):
        """Загружаем кастомизацию из файла."""
        try:
            with open("customization_data.json", "r") as f:
                customization_data = json.load(f)
                self.current_hat = customization_data.get("hat", 0)
                self.current_dress = customization_data.get("dress", 0)
                self.current_shoes = customization_data.get("shoes", 0)
        except FileNotFoundError:
            print("Файл кастомизации не найден. Используются значения по умолчанию.")

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

        # Рисуем кастомизированного персонажа
        self.draw_customized_character()

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

            pygame.draw.rect(self.screen, (0, 0, 0), (icon_x, 100, 100, 20), 2)  # Увеличенная шкала
            pygame.draw.rect(self.screen, (0, 255, 0), (icon_x, 100, value, 20))  # Увеличенная шкала

            # Отображаем значение
            value_text = self.font.render(str(value), True, (0, 0, 0))
            self.screen.blit(value_text, (icon_x + 110, 98))

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
        button_width = 150
        button_height = 40
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

        # Кнопка "Кастомизация" рядом с кнопкой "Удалить аккаунт"
        customization_button_rect = pygame.Rect(20, button_y + (button_height + 10) * 2, 230, button_height)
        pygame.draw.rect(self.screen, (205, 231, 238), customization_button_rect)
        customization_button_text = self.font.render("Кастомизация", True, (5, 82, 123))
        self.screen.blit(customization_button_text, (customization_button_rect.x + 5, customization_button_rect.y + 5))

        # Кнопка "Мини-игры"
        mini_games_button_rect = pygame.Rect(20, button_y + (button_height + 10) * 3, 230, button_height)
        pygame.draw.rect(self.screen, (205, 231, 238), mini_games_button_rect)
        mini_games_button_text = self.font.render("Мини-игры", True, (5, 82, 123))
        self.screen.blit(mini_games_button_text, (mini_games_button_rect.x + 5, mini_games_button_rect.y + 5))

        # Проверка нажатия кнопки "Мини-игры"
        if mini_games_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.open_mini_games_menu()  # Открываем меню мини-игр

        # Проверка нажатия кнопок
        mouse_pos = pygame.mouse.get_pos()
        if exit_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.exit_game()  # Выход из игры
        elif delete_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.delete_account()  # Удаление аккаунта
        elif customization_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.open_customization()  # Открытие кастомизации


        pygame.display.flip()  # Обновляем экран

    def draw_customized_character(self):
        """Отрисовка кастомизированного персонажа."""
        base_x = (WIDTH - self.character_image.get_width()) // 2
        base_y = (HEIGHT - self.character_image.get_height()) // 2 + 60

        # Рисуем персонажа в центре экрана
        character_x = (WIDTH - self.character_image.get_width()) // 2
        character_y = (HEIGHT - self.character_image.get_height()) // 2 + 60
        self.screen.blit(self.character_image, (character_x, character_y))

        # Отображаем текущие элементы кастомизации
        hat_image = self.hat_images[self.current_hat]
        dress_image = self.dress_images[self.current_dress]
        shoes_image = self.shoe_images[self.current_shoes]

        # Позиционирование одежды
        if dress_image:
            self.screen.blit(dress_image, (base_x, base_y))  # Платье на уровне тела

        # Позиционирование головного убора
        if hat_image:
            self.screen.blit(hat_image, (base_x, base_y - hat_image.get_height() + 750))  # Поднимаем шляпу над головой

        # Позиционирование обуви
        if shoes_image:
            self.screen.blit(shoes_image, (
                base_x, base_y + self.character_image.get_height() - shoes_image.get_height()))  # Обувь на уровне ног

    def open_mini_games_menu(self):
        """Открывает меню мини-игр."""
        run_menu(self)  # Запускаем меню мини-игр

    def update_stat(self, stat, value):
        """Обновление значения шкалы."""
        cost = 5  # Стоимость повышения состояния
        current_value = self.stats[stat]

        # Если текущее значение уже 100, ничего не делаем
        if current_value >= 100:
            return

        # Вычисляем, сколько нужно для достижения 100
        needed = 100 - current_value

        # Проверяем, достаточно ли очков для увеличения
        if self.player_points >= cost:
            if needed < cost:  # Если нужно меньше очков, чем стоимость
                self.stats[stat] = 100  # Увеличиваем до 100
                self.player_points -= needed  # Тратим только нужное количество очков
            else:
                self.stats[stat] = min(current_value + value, 101)  # Увеличиваем значение, не превышая 100
                self.player_points -= cost  # Уменьшаем количество очков
            self.last_update_time = time.time()  # Обновляем время последнего обновления
            self.save_data()  # Сохраняем данные после обновления


    def save_data(self):
        """Сохранение данных игрока в файл."""
        data = {
            "player_name": self.player_name,
            "player_level": self.player_level,
            "player_points": self.player_points,
            "stats": self.stats,
            "last_update_time": time.time(),
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
        self.last_update_time = time.time()

    def apply_time_effect(self, elapsed_minutes):
        """Уменьшение значений состояний в зависимости от прошедшего времени."""
        for stat in self.stats:
            if stat != "Здоровье":  # Например, здоровье не уменьшается
                self.stats[stat] = max(self.stats[stat] - elapsed_minutes, 0)

    def show_main_screen(self):
        """Показать главный экран с персонажем."""
        self.main_game_loop()  # Запускаем основной игровой цикл

    def load_data(self):
        """Загрузка данных игрока из файла."""
        if os.path.exists("player_data.json"):
            with open("player_data.json", "r") as f:
                data = json.load(f)
                self.player_name = data.get("player_name", "Игрок")
                self.player_level = data.get("player_level", 1)
                self.player_points = data.get("player_points", INITIAL_POINTS)
                self.stats = data.get("stats", {stat: 50 for stat in self.stats})
                last_update_time = data.get("last_update_time", time.time())

                # Вычисляем, сколько времени прошло с последнего обновления
                current_time = time.time()
                elapsed_minutes = int((current_time - last_update_time) / 60)

                if elapsed_minutes > 0:
                    self.apply_time_effect(elapsed_minutes)
        else:
            self.create_account_screen()

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


class CustomizationScreen:
    def __init__(self, app):
        # Устанавливаем текущую кастомизацию из VirtualVirusApp
        self.current_hat = app.current_hat
        self.current_dress = app.current_dress
        self.current_shoes = app.current_shoes

        self.app = app
        self.screen_width, self.screen_height = 1440, 810
        self.char_image = pygame.image.load('assets/char.png')
        self.background_image = pygame.image.load('assets/backgr.png')
        self.right_arrow = pygame.image.load('assets/right_arrow.png')
        self.left_arrow = pygame.image.load('assets/left_arrow.png')

        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.hats = [
            pygame.image.load('assets/hat.png'),
            pygame.image.load('assets/cap.png'),
            pygame.image.load('assets/beret.png'),
            pygame.image.load('assets/glasses.png'),
            pygame.image.load('assets/shapka.png'),
            pygame.image.load('assets/empty.png'),
        ]
        self.dresses = [
            pygame.image.load('assets/dress.png'),
            pygame.image.load('assets/kostum.png'),
            pygame.image.load('assets/pijama.png'),
            pygame.image.load('assets/t-shirt.png'),
            pygame.image.load('assets/uniform.png'),
            pygame.image.load('assets/empty.png'),
        ]
        self.shoes = [
            pygame.image.load('assets/shoes.png'),
            pygame.image.load('assets/boots.png'),
            pygame.image.load('assets/kedy.png'),
            pygame.image.load('assets/snickers.png'),
            pygame.image.load('assets/slippers.png'),
            pygame.image.load('assets/empty.png'),
        ]
        self.current_hat = 0
        self.current_dress = 0
        self.current_shoes = 0

        self.char_image = pygame.transform.scale(self.char_image, (400, 600))
        self.hats = [pygame.transform.scale(hat, (400, 600)) for hat in self.hats]
        self.dresses = [pygame.transform.scale(dress, (400, 600)) for dress in self.dresses]
        self.shoes = [pygame.transform.scale(shoe, (400, 600)) for shoe in self.shoes]

        self.button_width = 80
        self.button_height = 80

        self.button_left_hat = pygame.Rect(400, self.screen_height // 2 - 200, self.button_width, self.button_height)
        self.button_left_dress = pygame.Rect(400, self.screen_height // 2 - 50, self.button_width, self.button_height)
        self.button_left_shoes = pygame.Rect(400, self.screen_height // 2 + 100, self.button_width, self.button_height)

        self.button_right_hat = pygame.Rect(self.screen_width - 530, self.screen_height // 2 - 200, self.button_width, self.button_height)
        self.button_right_dress = pygame.Rect(self.screen_width - 530, self.screen_height // 2 - 50, self.button_width, self.button_height)
        self.button_right_shoes = pygame.Rect(self.screen_width - 530, self.screen_height // 2 + 100, self.button_width, self.button_height)

        # Кнопка выхода
        self.exit_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 100, 200, 40)
        # Кнопка сохранения
        self.save_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 150, 200, 40)

    def draw_char(self):
        base_x, base_y = 500, 150
        self.app.screen.blit(self.char_image, (base_x, base_y))
        self.app.screen.blit(self.hats[self.current_hat], (base_x, base_y))
        self.app.screen.blit(self.dresses[self.current_dress], (base_x, base_y))
        self.app.screen.blit(self.shoes[self.current_shoes], (base_x, base_y))

    def draw_buttons(self):
        button_color = (200, 200, 200)
        button_hover_color = (170, 170, 170)
        mouse_pos = pygame.mouse.get_pos()

        def draw_button(rect, text):
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.app.screen, button_hover_color, rect)
            else:
                pygame.draw.rect(self.app.screen, button_color, rect)

            text_surface = self.app.font.render(text, True, (0, 0, 0))
            self.app.screen.blit(text_surface, (rect.x + 5, rect.y + 5))

        draw_button(self.button_left_hat, "<")
        draw_button(self.button_left_dress, "<")
        draw_button(self.button_left_shoes, "<")
        draw_button(self.button_right_hat, ">")
        draw_button(self.button_right_dress, ">")
        draw_button(self.button_right_shoes, ">")

        # Отрисовка кнопки выхода
        draw_button(self.exit_button_rect, "Выход")
        # Отрисовка кнопки сохранения
        draw_button(self.save_button_rect, "Сохранить")

    def save_customization(self):
        """Сохранить текущую кастомизацию и обновить данные в VirtualVirusApp."""
        customization_data = {
            "hat": self.current_hat,
            "dress": self.current_dress,
            "shoes": self.current_shoes,
        }
        with open("customization_data.json", "w") as f:
            json.dump(customization_data, f)

        # Обновление данных в VirtualVirusApp
        self.app.current_hat = self.current_hat
        self.app.current_dress = self.current_dress
        self.app.current_shoes = self.current_shoes

        print("Кастомизация сохранена!")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.button_left_hat.collidepoint(mouse_pos):
                        self.current_hat = (self.current_hat - 1) % len(self.hats)
                    elif self.button_left_dress.collidepoint(mouse_pos):
                        self.current_dress = (self.current_dress - 1) % len(self.dresses)
                    elif self.button_left_shoes.collidepoint(mouse_pos):
                        self.current_shoes = (self.current_shoes - 1) % len(self.shoes)

                    if self.button_right_hat.collidepoint(mouse_pos):
                        self.current_hat = (self.current_hat + 1) % len(self.hats)
                    elif self.button_right_dress.collidepoint(mouse_pos):
                        self.current_dress = (self.current_dress + 1) % len(self.dresses)
                    elif self.button_right_shoes.collidepoint(mouse_pos):
                        self.current_shoes = (self.current_shoes + 1) % len(self.shoes)

                    # Проверка нажатия кнопки выхода
                    if self.exit_button_rect.collidepoint(mouse_pos):
                        return  # Возвращаемся в основной экран игры

                    # Проверка нажатия кнопки сохранения
                    if self.save_button_rect.collidepoint(mouse_pos):
                        self.save_customization()  # Сохранить кастомизацию

            # Отрисовка фона и элементов
            self.app.screen.blit(self.background_image, (0, 0))
            self.draw_char()
            self.draw_buttons()

            pygame.display.flip()


def save_money(money):
    """Сохраняет количество денег в файл.

        Записывает переданное количество денег в файл "money.txt".
        Если файл не существует, он будет создан.

        Args:
            money (int): Количество денег, которое нужно сохранить.

        Returns:
            None
    """
    with open("money.txt", "w") as file:
        file.write(str(money))

def load_money():
    """Загружает количество денег из файла.

        Читает количество денег из файла "money.txt". Если файл не найден,
        возвращает 0.

        Returns:
            int: Количество денег, загруженное из файла, или 0, если файл не найден.
    """
    try:
        with open("money.txt", "r") as file:
            money = int(file.read())
            return money
    except FileNotFoundError:
        return 0  # Если файл не найден, возвращаем 0
# Классы для игровых объектов
class Strawberry:
    def __init__(self, x, y):
        self.image = pygame.image.load('strawberry.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True
        self.speed = 5

    def move(self):
        if self.visible:
            self.rect.y += self.speed
            if self.rect.y > screen_height:
                self.rect.y = 0
                self.rect.x = random.randint(0, screen_width - self.rect.width)

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect.topleft)

class Mushroom:
    def __init__(self, x, y):
        self.image = pygame.image.load('mashroom.jpg')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True
        self.speed = 5

    def move(self):
        if self.visible:
            self.rect.y += self.speed
            if self.rect.y > screen_height:
                self.rect.y = 0
                self.rect.x = random.randint(0, screen_width - self.rect.width)

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect.topleft)

class Oclock:
    def __init__(self, x, y):
        self.image = pygame.image.load('oclock.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True
        self.speed = 1

    def move(self):
        if self.visible:
            self.rect.y += self.speed
            if self.rect.y > screen_height:
                self.rect.y = 0
                self.rect.x = random.randint(0, screen_width - self.rect.width)

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect.topleft)

class Player:
    def __init__(self):
        self.image = pygame.image.load('player_down.png')
        self.rect = self.image.get_rect(topleft=(character_x, character_y))
        self.speed = 10

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - self.rect.width:
            self.rect.x = screen_width - self.rect.width

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Функция для создания новых объектов
def create_new_strawberry():
    """Создает новый объект Strawberry со случайной координатой x.

       Координата y устанавливается в 0. Координата x генерируется случайным образом
       в пределах ширины экрана минус ширина объекта Strawberry.

       Returns:
           Strawberry: Новый объект Strawberry со случайной координатой x.
    """
    return Strawberry(random.randint(0, screen_width - 30), 0)

def create_new_mushroom():
    """Создает новый объект Mushroom со случайной координатой x.

        Координата y устанавливается в 0. Координата x генерируется случайным образом
        в пределах ширины экрана минус ширина объекта Mushroom.

        Returns:
            Mushroom: Новый объект Mushroom со случайной координатой x.
    """
    return Mushroom(random.randint(0, screen_width - 30), 0)

def create_new_oclock():
    """Создает новый объект Oclock с случайной координатой x.

        Координата y устанавливается в 0. Координата x генерируется случайным образом
        в пределах ширины экрана минус ширина объекта Oclock.

        Returns:
            Oclock: Новый объект Oclock с случайной координатой x.
    """
    return Oclock(random.randint(0, screen_width - 30), 0)

# Основная функция игры
def run_game(app):
    """Запускает игру "Падающая клубника".

        Инициализирует Pygame, устанавливает размеры окна, загружает фон и
        настраивает игровую логику, включая создание объектов, обработку событий,
        движение персонажа и проверку столкновений. Игра продолжается в течение
        30 секунд, после чего отображается итоговый счет и возможность вернуться в меню.

        В процессе игры игрок может собирать клубнику для увеличения счета,
        избегать столкновений с грибами, которые уменьшают счет, и собирать часы,
        которые добавляют время.

        Returns:
            None
    """
    global screen_width, screen_height, character_x, character_y
    pygame.init()
    # Установка размера окна
    screen_width, screen_height = 1440, 810
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Загрузка и изменение размера фона
    background = pygame.image.load('forest.png')
    background = pygame.transform.scale(background, (screen_width, screen_height))  # Изменяем размер фона
    pygame.display.set_caption("Игра падающая клубника")

    # Установка времени
    duration = 30000  # 30 секунд в миллисекундах
    start_time = pygame.time.get_ticks()  # Инициализация времени
    # Настройка анимации/смены кадров
    clock = pygame.time.Clock()
    FPS = 30

    # Счет
    score = 0
    score_screen_text = pygame.font.Font(None, 74)
    BLACK = (0, 0, 0)

    # Итог
    end_screen_text = pygame.font.Font(None, 90)
    text_surface_menu = score_screen_text.render("Обратно в меню", True, (148, 0, 211))
    text_rect_menu = text_surface_menu.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

    # Настройка положения и движения
    speed = 50
    character_y = screen_height / 2 + 150
    character_x = (screen_width / 2) - 10
    button_click_menu = False  # Если кнопка нажата

    # Создание объектов
    strawberry = create_new_strawberry()
    mushroom = create_new_mushroom()
    oclock = create_new_oclock()
    player = Player()

    running = True
    while running:
        # Обработка событий
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левый клик мыши
                    if text_rect_menu.collidepoint(event.pos):  # Проверяем, попадает ли курсор в область текста
                        button_click_menu = True  # Устанавливаем состояние нажатия кнопки
        if button_click_menu:
            current_money = load_money()  # Загружаем деньги из файла
            total_points = score * 5 + current_money
            save_money(total_points)  # Сохраняем деньги
            app.add_points(score * 5)  # Добавляем очки к текущему значению
            running = False  # Выход из игры, чтобы вернуться в меню
            run_menu(app)  # Возвращаемся в меню
            break
        # Движение персонажа
        player.move()

        # Проверка на столкновение
        if player.rect.colliderect(oclock.rect) and oclock.visible:
            oclock.visible = False  # Скрыть часы при столкновении
            duration += 5000
            oclock = create_new_oclock()  # Создать новые часы

        if player.rect.colliderect(mushroom.rect) and mushroom.visible:
            mushroom.visible = False  # Скрыть гриб при столкновении
            if score > 0:
                score -= 1
            mushroom = create_new_mushroom()  # Создать новую гриб

        if player.rect.colliderect(strawberry.rect) and strawberry.visible:
            strawberry.visible = False  # Скрыть клубнику при столкновении
            score += 1
            strawberry = create_new_strawberry()  # Создать новую клубнику

        # Проверяем, прошло ли 30 секунд
        current_time = pygame.time.get_ticks()
        screen.fill((0, 0, 0))

        # Инициализация текстов
        text_score = score_screen_text.render(str(score), True, (0, 0, 0))  # Счет на экране
        text_rect_score = text_score.get_rect(center=(100, 100))

        text_time = score_screen_text.render(f'{(duration - (current_time - start_time)) // 1000} сек', True, (0, 0, 0))  # Счетчик времени
        text_rect_time = text_time.get_rect(center=(300, 100))

        text_end = score_screen_text.render('Время вышло', True, (0, 0, 0))  # Итог
        text_rect_end = text_end.get_rect(center=(screen_width / 2, screen_height / 2 - 200))

        text_score_end = score_screen_text.render(f'Ваш счёт: {score * 5}', True, (0, 0, 0))  # Счёт в конце игры
        text_score_end = score_screen_text.render(f'Ваш счёт: {score * 5}', True, (0, 0, 0))  # Счёт в конце игры
        text_rect_score_end = text_score_end.get_rect(center=(screen_width / 2, screen_height / 2 - 100))

        # Прорисовка заднего фона
        screen.blit(background, (0, 0))
        if current_time - start_time < duration:
            screen.blit(text_score, text_rect_score)
            screen.blit(text_time, text_rect_time)
            oclock.move()
            oclock.draw(screen)
            strawberry.move()
            strawberry.draw(screen)
            mushroom.move()
            mushroom.draw(screen)
            player.draw(screen)
        else:
            text_money = score_screen_text.render(f'Количество денег: {str(score * 5 + load_money())}', True,
                                                  (0, 0, 0))  # Счет на экране
            text_rect_money = text_money.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text_money, text_rect_money)
            screen.blit(text_end, text_rect_end)
            screen.blit(text_score_end, text_rect_score_end)
            screen.blit(text_surface_menu, text_rect_menu)

            # Сохранение денег при нажатии кнопки
            if button_click_menu:
                current_money = load_money()  # Загружаем деньги из файла
                save_money(score * 5 + current_money)
                running = False  # Выход из игры, чтобы вернуться в меню
                run_menu(app)  # Возвращаемся в меню
                break

        pygame.display.flip()  # Обновляем экран

    pygame.quit()  # Закрываем Pygame
import pygame
import random

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры окна и плиток
width, height = 400, 400
tile_size = width // 4
fps = 30

font_plays = pygame.font.Font(None, 30)  # Используем стандартный шрифт
text_surface_menu = font_plays.render("Меню", True, (148, 0, 211))  # Создаем поверхность текста
text_rect_menu = text_surface_menu.get_rect(center=(35, 13))  # Получаем прямоугольник текста

# Определяем цвета
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
green = (1, 55, 32)

# Функция для создания доски
def create_board():
    """Создает игровое поле для игры в 15.

        Генерирует случайное расположение 15 плиток и одной пустой клетки.
        Плитки представлены числами от 1 до 15, а пустая клетка обозначается нулем.
        Возвращает двумерный список, представляющий игровое поле с 4 строками.

        Returns:
            list: Двумерный список размером 4x4, содержащий числа от 1 до 15 и 0.
    """
    numbers = list(range(1, 16)) + [0]  # 15 плиток и одна пустая клетка
    random.shuffle(numbers)
    return [numbers[i:i + 4] for i in range(0, 16, 4)]  # Создаем 4 строки

# Функция для отрисовки доски
def draw_board(board):
    """Отображает игровое поле на экране.

        Рисует 4 строки и 4 столбца плиток на экране, представляя игровое поле
        для игры в пятнашки. Плитки отображаются в сером цвете, а пустая клетка — в белом.
        Числа на плитках отображаются черным цветом.

        Args:
            board (list): Двумерный список размером 4x4, содержащий числа от 1 до 15 и 0,
                          где 0 представляет пустую клетку.

        Returns:
            None
    """
    for i in range(4):  # 4 строки
        for j in range(4):  # 4 столбца
            number = board[i][j]
            rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
            if number == 0:
                pygame.draw.rect(screen, white, rect)  # Пустая клетка
            else:
                pygame.draw.rect(screen, gray, rect)  # Плитка
                font = pygame.font.Font(None, 74)
                text = font.render(str(number), True, black)
                screen.blit(text, (j * tile_size + tile_size // 4, i * tile_size + tile_size // 4))
            pygame.draw.rect(screen, black, rect, 1)  # Граница плитки

# Функция для перемещения плитки
def move_tile(board, row, col):
    """Перемещает плитку на игровом поле.

        Если плитка, находящаяся в позиции (row, col), соседствует с пустой клеткой,
        плитка перемещается на место пустой клетки. Функция обновляет состояние
        игрового поля и возвращает True, если перемещение успешно, и False в противном случае.

        Args:
            board (list): Двумерный список размером 4x4, представляющий игровое поле,
                          где 0 обозначает пустую клетку.
            row (int): Индекс строки плитки, которую нужно переместить.
            col (int): Индекс столбца плитки, которую нужно переместить.

        Returns:
            bool: True, если перемещение успешно, иначе False.
    """
    empty_row, empty_col = find_empty_tile(board)
    if (abs(empty_row - row) == 1 and empty_col == col) or (abs(empty_col - col) == 1 and empty_row == row):
        board[empty_row][empty_col], board[row][col] = board[row][col], board[empty_row][empty_col]
        return True
    return False

# Функция для нахождения пустой плитки
def find_empty_tile(board):
    """Находит координаты пустой клетки на игровом поле.

        Ищет пустую клетку, обозначенную нулем, в двумерном списке, представляющем
        игровое поле. Возвращает индексы строки и столбца пустой клетки. Если пустая
        клетка не найдена, возвращает None (что не должно происходить, если доска корректна).

        Args:
            board (list): Двумерный список размером 4x4, представляющий игровое поле,
                          где 0 обозначает пустую клетку.

        Returns:
            tuple: Кортеж из двух целых чисел (row, col), представляющий координаты
                   пустой клетки, или None, если пустая клетка не найдена.
    """
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return i, j
    return None  # Это не должно происходить, если доска корректна

# Функция для проверки выигрыша
def check_win(board):
    """Проверяет, выиграл ли игрок.

        Сравнивает текущее состояние игрового поля с правильным порядком плиток.
        Если плитки расположены в порядке от 1 до 15, а пустая клетка находится
        в последнем месте, функция возвращает True. В противном случае возвращает False.

        Args:
            board (list): Двумерный список размером 4x4, представляющий игровое поле,
                          где 0 обозначает пустую клетку.

        Returns:
            bool: True, если игрок выиграл (плитки расположены в правильном порядке),
                  иначе False.
    """
    correct_order = list(range(1, 16)) + [0]
    flat_board = [num for row in board for num in row]
    return flat_board == correct_order

# Основная функция игры
def run_game_pyatnashki(app):
    """Запускает игру "Пятнашки".

        Инициализирует Pygame, создает игровое окно и запускает основной игровой цикл.
        Обрабатывает события, такие как нажатия мыши для перемещения плиток. Проверяет,
        выиграл ли игрок, и отображает сообщение о победе. Позволяет вернуться в меню
        и сохраняет деньги при выигрыше.

        Returns:
            None
    """
    global screen  # Делаем экран глобальным, чтобы использовать его в других функциях
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Пятнашки")

    clock = pygame.time.Clock()
    board = create_board()
    running = True
    button_pressed_menu = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // tile_size, y // tile_size
                if 0 <= col < 4 and 0 <= row < 4:  # Проверяем, что клик внутри границ
                    move_tile(board, row, col)
                if event.button == 1:  # Левый клик мыши
                    if text_rect_menu.collidepoint(event.pos):  # Проверяем, попадает ли курсор в область текста
                        button_pressed_menu = True
        if button_pressed_menu:
            if check_win(board):
                save_money(load_money() + 300)
            app.add_points(300)  # Добавляем 300 очков к текущему значению
            running = False
            run_menu(app)

        if check_win(board):
            win_message = font_plays.render("Вы выиграли!", True, green)
            win_rect = win_message.get_rect(center=(width // 2, height // 2))
            screen.blit(win_message, win_rect)
            pygame.display.flip()
            pygame.time.wait(2000)  # Ждем 2 секунды перед перезапуском игры
            board = create_board()  # Перезапускаем игру
        if button_pressed_menu:
            if check_win(board):
                save_money(load_money() + 300)
            running = False
            run_menu(app)
        # Отрисовка доски и меню
        screen.fill(white)
        draw_board(board)
        screen.blit(text_surface_menu, text_rect_menu)  # Отрисовываем текст меню
        pygame.display.flip()  # Обновляем экран
        clock.tick(fps)  # Ограничиваем FPS

    pygame.quit()  # Закрываем Pygame

def run_menu(app):
    """Запускает главное меню игры.

        Инициализирует Pygame, создает игровое окно и отображает меню с доступными играми.
        Позволяет игроку перемещать персонажа по экрану, а также выбирать игры "Падающая клубника"
        и "Пятнашки". Обрабатывает события мыши и клавиатуры, отображает текущее количество денег в меню.
        Также присутствует кнопка домой и меню.

        Returns:
            None
    """
    pygame.init()
    screen = pygame.display.set_mode((1440, 810))  # Устанавливаем размер экрана
    background = pygame.image.load('home.jpg')
    background = pygame.transform.scale(background, (1440, 810))  # Изменяем размер фона
    pygame.display.set_caption('Меню игр')
    screen_width, screen_height = 1440, 810

    # Настройка анимации/смены кадров
    clock = pygame.time.Clock()
    FPS = 30
    money = load_money()  # Выгружаем деньги из файла

    # Загрузка изображений для каждого направления игрока
    image_left = pygame.image.load("player_left.png")
    image_right = pygame.image.load("player_right.png")
    image_up = pygame.image.load("player_up.png")
    image_down = pygame.image.load("player_down.png")

    current_image = image_down  # Начальное изображение
    player_rect = current_image.get_rect(center=(screen_width // 2, screen_height // 2))  # Начальная позиция

    # Создание кнопки входа в меню
    button_rect_menu = pygame.Rect(50, -30, 82, 120)  # Позиция и размер кнопки
    button_hover_color_menu = (0, 0, 0, 255)  # Полупрозрачный зеленый

    # Кнопка домой, создаем прямоугольник кнопки
    button_rect_home = pygame.Rect(10, 650, 200, 50)

    # Тексты
    font_plays = pygame.font.Font(None, 50)  # Используем стандартный шрифт
    text_surface_strawberry = font_plays.render("Падающая клубника", True, (148, 0, 211))
    text_rect_strawberry = text_surface_strawberry.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    text_surface_5 = font_plays.render("Пятнашки", True, (148, 0, 211))
    text_rect_5 = text_surface_5.get_rect(center=(screen_width // 2, screen_height // 2))
    text_surface_money = font_plays.render(f'Деньги: {str(money)}', True, (148, 0, 211))
    text_rect_money = text_surface_money.get_rect(center=(150, 50))

    # Переменная для хранения состояния
    button_pressed_strawberry = False
    button_pressed_5 = False
    button_pressed_home = False
    # Шрифт
    big_screen_text = pygame.font.Font(None, 90)
    font_home = pygame.font.Font(None, 36)
    # Настройка положения и движения
    speed = 25
    running = True
    button_click_menu = False  # Если кнопка нажата

    while running:
        # Обработка событий
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_menu.collidepoint(event.pos):  # Проверяем, нажата ли кнопка
                    button_click_menu = True
                if event.button == 1:  # Левый клик мыши
                    if text_rect_strawberry.collidepoint(event.pos):  # Проверяем, попадает ли курсор в область текста
                        button_pressed_strawberry = True  # Устанавливаем состояние нажатия кнопки
                    if text_rect_5.collidepoint(event.pos):  # Проверяем, попадает ли курсор в область текста
                        button_pressed_5 = True  # Устанавливаем состояние нажатия кнопки
                    if button_rect_home.collidepoint(event.pos):  # Проверяем, попадает ли курсор в область кнопки
                        button_pressed_home = True
        if button_pressed_home:
            # Здесь вы можете добавить логику для сохранения текущих очков
            running = False
            app.show_main_screen()  # Возвращаемся на главный экран

        # Получение нажатых клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= speed
            current_image = image_left  # Изменение изображения при движении влево
        elif keys[pygame.K_RIGHT]:
            player_rect.x += speed
            current_image = image_right  # Изменение изображения при движении вправо
        elif keys[pygame.K_UP]:
            player_rect.y -= speed
            current_image = image_up  # Изменение изображения при движении вверх
        elif keys[pygame.K_DOWN]:
            player_rect.y += speed
            current_image = image_down  # Изменение изображения при движении вниз
        else:
            current_image = image_down  # Если ничего не нажато, показываем изображение вниз (или любое другое)

        # Ограничение движения по границам экрана
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > screen_width:
            player_rect.right = screen_width
        if player_rect.top < 80:
            player_rect.top = 80
        if player_rect.bottom > screen_height:
            player_rect.bottom = screen_height

        # Получаем позицию мыши
        mouse_pos = pygame.mouse.get_pos()

        # Инициализация текстов
        text_play = big_screen_text.render('Игры', True, (148, 0, 211))  # Текст на экране
        text_rect_play = text_play.get_rect(center=(screen_width / 2, screen_height / 2 - 200))

        if not button_click_menu:
            # Изменяем цвет кнопки при наведении
            if button_rect_menu.collidepoint(mouse_pos):
                button_color_menu = button_hover_color_menu
            else:
                button_color_menu = (0, 0, 0, 0)  # Полупрозрачный серый

            # Кнопка домой
            if button_pressed_home:
                pass

            # Создаем поверхность для кнопки с альфа-каналом
            button_surface_menu = pygame.Surface(button_rect_menu.size, pygame.SRCALPHA)
            button_surface_menu.fill(button_color_menu)  # Заполняем поверхность цветом с альфа-каналом

            # Создаем текст
            text_surface_home = font_home.render("Домой", True, (0, 0, 0))
            text_rect_home = text_surface_home.get_rect(center=button_rect_home.center)

            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            screen.blit(current_image, player_rect)  # Отрисовка текущего персонажа
            screen.blit(button_surface_menu, button_rect_menu)
            # Отрисовываем кнопку домой
            pygame.draw.rect(screen, (150, 75, 0), button_rect_home)
            pygame.draw.rect(screen, (0, 0, 0), button_rect_home, 2)  # Граница кнопки
            screen.blit(text_surface_home, text_rect_home)
            pygame.display.flip()
        else:
            screen.fill((91, 147, 226))
            screen.blit(text_surface_5, text_rect_5)
            screen.blit(text_surface_strawberry, text_rect_strawberry)
            screen.blit(text_surface_money, text_rect_money)
            screen.blit(text_play, text_rect_play)

            # Здесь можно добавить логику для обработки нажатий на кнопки "Падающая клубника" и "Пятнашки"
            if button_pressed_strawberry:
                # Логика для запуска игры "Падающая клубника"
                run_game(app)

            if button_pressed_5:
                # Логика для запуска игры "Пятнашки"
                run_game_pyatnashki(app)

            pygame.display.flip()

    pygame.quit()

# Запуск приложения
if __name__ == "__main__":
    VirtualVirusApp()


