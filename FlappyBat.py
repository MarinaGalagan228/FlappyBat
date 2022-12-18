import random

import pygame, sys

# Задаем графическое окно и его разрешение
pygame.init()
screen = pygame.display.set_mode((580, 780))

# Задаем частоту кадров
FPS = 120
FramePerSecond = pygame.time.Clock()

# Задаем начальные парметры игры
score = 0
record_score = 0
if_game = False
collision = True

# Загружаем шрифты для таймера и меню
font = pygame.font.Font('assets/font.ttf', 55)
font_menu_1 = pygame.font.Font('assets/font1.otf', 63)
font_menu_2 = pygame.font.Font('assets/font1.otf', 40)

# Загружаем изображения для стартового экрана:
startscreen = pygame.image.load('assets/welcome.png').convert_alpha()
startscreen = pygame.transform.scale(startscreen, (250, 200))

# Для фона игры, подгон картинки под разрешение окна:
background = pygame.image.load('assets/background.jpg').convert()
background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

# Для земли, подгон картинки под разрешение окна:
clouds = pygame.image.load('assets/clouds.png').convert()
clouds = pygame.transform.scale(clouds, (screen.get_width(), clouds.get_height() + 170))
clouds_x = 0

# Для мыши (5 вариаций изображения):
bat1 = pygame.image.load('assets/b1.png').convert()
bat1 = pygame.transform.scale(bat1, (100, 100))
bat2 = pygame.image.load('assets/b2.png').convert()
bat2 = pygame.transform.scale(bat2, (100, 100))
bat3 = pygame.image.load('assets/b3.png').convert()
bat3 = pygame.transform.scale(bat3, (100, 100))
bat4 = pygame.image.load('assets/b4.png').convert()
bat4 = pygame.transform.scale(bat4, (100, 100))
bat5 = pygame.image.load('assets/b5.png').convert()
bat5 = pygame.transform.scale(bat5, (100, 100))

bat_all_images = [bat1, bat2, bat3, bat4, bat5, bat4, bat3, bat2]

bat = bat_all_images[0]
bat_rect = bat.get_rect(center=(100, 500))
bat_move = 0
# (Cоздание "движения" крыльев засчет смены изображения каждые 45 мс)
BATEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BATEVENT, 45)
bat_counter = 0

# Для колонн:
pipe = pygame.image.load('assets/pipe.png').convert()
pipe = pygame.transform.scale(pipe, (100, 600))

# Список с высотой колонн, из которой текущая высота будет выбираться методом .random
pipe_Choices = [650, 700, 750, 800, 850, 900]
pipes = []

# (Таймер появления колонн каждые 1000 мс)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)


def menu_design(font_menu_1, font_menu_2):
    """ Функция, добавляющая надписи 'FlappyBat', 'SPACE to play' и 'ESCAPE to exit' в меню игры
    :param font_menu_1: шрифт для меню №1
    :param font_menu_2: шрифт для меню №2
    """
    flappybat_text = font_menu_1.render('FlappyBat', True, (0, 0, 0))
    screen.blit(flappybat_text, (37, 100))

    space_text = font_menu_2.render('SPACE', True, (0, 0, 0))
    screen.blit(space_text, (35, 250))

    to_play_text = font_menu_2.render('to play', True, (0, 0, 0))
    screen.blit(to_play_text, (20, 310))

    esc_text = font_menu_2.render('ESCAPE', True, (0, 0, 0))
    screen.blit(esc_text, (335, 250))

    to_exit_text = font_menu_2.render('to exit', True, (0, 0, 0))
    screen.blit(to_exit_text, (337, 310))


def count_points(pipes, score):
    """ Функция, начисляющая очки каждый раз, когда положение мыши по Х совпадает с центром колонны по Х
    :param pipes: список колонн
    :param score: текущие очки
    :return: текущие очки + 1 за каждую пройденную колонну
    """
    for pipe in pipes:
        if bat_rect.centerx == pipe.centerx:
            score += 1
    return score


def score_display(if_game, score, record_score, font):
    """ Функция, отвечающая за вывод на экран текущих очков во время игры
        и максимального количества набранных очков в меню по окончании игры
    :param if_game: параметр отвечающий за статус игры: True - игра активна, False - меню игры
    :param score: текущие очки
    :param record_score: максимальное количество набранных очков
    """

    score_text = "Score: " + str(int(score / 2))
    record_score_text = "Record score: " + str(int(record_score / 2))

    if if_game == False:
        score_display = font.render(score_text, True, (0, 0, 0))
        screen.blit(score_display, (188, 48))

    if if_game == True:
        record_score_display = font.render(record_score_text, True, (0, 0, 0))
        screen.blit(record_score_display, (100, 48))


def check_Collision(pipes, bat_rect):
    """ Функция, проверяющая столкновение птицы с колонной и выход птицы за пределы экрана
    :param pipes: список колонн
    :param bat_rect: положение птицы на экране
    :return: True - в случае выхода за пределы экрана или столкновения с колонной, иначе - False
    """
    if bat_rect.centery < 15 or bat_rect.centery > 750:
        return True

    for pipe in pipes:
        if bat_rect.colliderect(pipe):
            return True
    return False


def create_clouds(clouds, clouds_x):
    """ Функция вывода на экран земли и добавления справа вслед за текущей новой земли
    :param clouds: изображение земли
    :param clouds_x: параметр смещения земли по Х
    """
    try:
        screen.blit(clouds, (clouds_x, 670))
        screen.blit(clouds, (clouds_x + screen.get_width(), 670))
    except AttributeError:
        return None, 'AttributeError'
    except TypeError:
        return None, 'TypeError'


def create_pipe():
    """ Функция, отвечающая за создание колонн случайной высоты в нижней и в верхней части экрана на определенном расстоянии друг от друга
    :return: Колонна в нижней (pipe_normal) и в верхней (pipe_flip) части экрана
    """
    pipe_height = random.choice(pipe_Choices)
    pipe_normal = pipe.get_rect(center=(800, pipe_height))
    pipe_flip = pipe.get_rect(center=(800, pipe_height - 900))
    return (pipe_normal, pipe_flip)


def draw_pipes(pipes):
    """ Функция вывода колонн на экран (в обычном и перевернутом по вертикали формате)
    :param pipes: список колонн
    """
    for pipe_i in pipes:
        if pipe_i.bottom >= 800:
            screen.blit(pipe, pipe_i)
        else:
            new_pipe = pygame.transform.flip(pipe, False, True)
            screen.blit(new_pipe, pipe_i)


def move_pipes(pipes):
    """ Функция, задающая расстояние по Х между колонной по центру экрана до новой колонны справа
    :param pipes: список колонн
    :return: Обновленный список колонн со смещением по Х
    """
    try:
        for pipe in pipes:
            pipe.centerx -= 4
        return pipes
    except TypeError:
        return None, 'TypeError'


# Основной цикл игры
while True:
    # Закрытие Pygame, выход из программы
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Назначаем клавиши ПРОБЕЛ для управления мышью, ESC для выхода из игры
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            if event.key in [pygame.K_SPACE]:
                bat_move = 0
                bat_move -= 8

                collision = False

        # Добавление новых колонн в список
        if event.type == SPAWNPIPE:
            pipes.extend(create_pipe())

        # Смена выводимого изображения мыши
        if event.type == BATEVENT:
            bat = bat_all_images[bat_counter % 8]
            bat_counter += 1

    screen.blit(background, (0, 0))

    # Данный цикл выполняется до тех пор, пока не произошло столкновение
    if collision is not True:

        screen.blit(bat, bat_rect)

        bat_move += 0.27
        bat_rect.centery += bat_move

        draw_pipes(pipes)
        move_pipes(pipes)

        collision = check_Collision(pipes, bat_rect)

        score = count_points(pipes, score)

        # Сравниваем максимальное кол-во набранных очков с текущим и обновляем результат в случае превышения
        if score > record_score:
            record_score = score

        score_display(False, score, record_score, font)

    # Обнуляем значения и запускаем стартовый экран при столкновении
    else:
        pipes = []
        bat_rect.centery = 500
        screen.blit(startscreen, (170, 400))
        score_display(True, score, record_score, font)
        menu_design(font_menu_1, font_menu_2)
        score = 0

    # Иллюзия непрерывного "движения" облаков засчет создания очереди из изображений, которая
    # пополняется при выходе текущего изображения за пределы левой части экрана
    clouds_x -= 1
    create_clouds(clouds, clouds_x)
    if abs(clouds_x) == screen.get_width():
        clouds_x = 0

    FramePerSecond.tick(FPS)
    pygame.display.update()
