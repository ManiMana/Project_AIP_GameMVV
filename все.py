import pygame
import random
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
def run_game():
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
                run_menu()  # Возвращаемся в меню
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
def run_game_pyatnashki():
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
            run_menu()
        # Отрисовка доски и меню
        screen.fill(white)
        draw_board(board)
        screen.blit(text_surface_menu, text_rect_menu)  # Отрисовываем текст меню
        pygame.display.flip()  # Обновляем экран
        clock.tick(fps)  # Ограничиваем FPS

    pygame.quit()  # Закрываем Pygame

def run_menu():
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
                run_game()

            if button_pressed_5:
                # Логика для запуска игры "Пятнашки"
                run_game_pyatnashki()

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_menu()