import os
import sqlite3
import sys
from functools import cache

import pygame as pg
import src.consts

CELL_SIZE = src.consts.CELL_SIZE
MAP_SIZE = src.consts.MAP_SIZE


def resource_path(*relative_path, use_abs_path: bool = False):
    save_relative = relative_path

    if not use_abs_path and getattr(sys, "_MEIPASS", False):
        base_path = sys._MEIPASS
        relative_path = relative_path[2:]
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *relative_path), save_relative, relative_path


@cache
def load_image(
        name: str,
        colorkey: pg.Color | int | None = None,
        crop_it: bool = False,
) -> pg.Surface:
    """
    Загрузка изображения в pygame.Surface.

    :param name: Путь до файла, начиная от src/data, e.g. "images/menu/background.png"
    :param colorkey: Пиксель, по которому будет удаляться задний фон. Если -1, то по левому верхнему.
    :param crop_it: Обрезать ли изображение по прозрачному фону.
    :return: pygame.Surface
    """
    fullname, save_rel, rel = resource_path("src", "data", *name.split("/"))
    if not os.path.isfile(fullname):
        raise FileNotFoundError(
            f"Файл с изображением '{fullname}' не найден\n{save_rel}\n{rel}",
        )
    image = pg.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    if crop_it:
        image = crop(image)

    return image


@cache
def load_sound(name, return_path: bool = False) -> pg.mixer.Sound | str:
    """
    Загрузка звука в pygame.Sound.

    :param name: Путь до файла, начиная от src/data, e.g. "sounds/fart.mp3"
    :param return_path: Вернуть ли путь до файла вместо самого звука.
    :return: pygame.Sound или путь до файла
    """
    fullname, save_rel, rel = resource_path("src", "data", *name.split("/"))
    if not os.path.isfile(fullname):
        raise FileNotFoundError(
            f"Файл с звуком '{fullname}' не найден\n{save_rel}\n{rel}",
        )
    if return_path:
        return fullname
    sound = pg.mixer.Sound(fullname)
    return sound


@cache
def crop(screen: pg.Surface) -> pg.Surface:
    """
    Обрезка изображения по крайним не пустым пикселям.

    :param screen: Изображение.
    :return: Обрезанное изображение.
    """
    pixels = pg.PixelArray(screen)
    background = pixels[0][0]
    width, height = screen.get_width(), screen.get_height()
    min_x = width
    min_y = height
    max_x = 0
    max_y = 0

    for x in range(width):
        for y in range(height):
            current = pixels[x][y]
            if current != background:
                max_x = max(x, max_x)
                max_y = max(y, max_y)
                min_x = min(x, min_x)
                min_y = min(y, min_y)

    return screen.subsurface((min_x, min_y, max_x - min_x, max_y - min_y))


def create_data_base():
    con = sqlite3.connect(resource_path("stats.sqlite", use_abs_path=True)[0])
    cur = con.cursor()
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS game_over (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            win_or_loose STRING,
            score INT);
            """,
    )
    con.commit()


def get_cell_coords_from_coords(x: float, y: float) -> tuple[int, int]:
    """
    :param x:
    :param y:
    :return: (a, b)
    чтобы обратиться к клетке cells[a][b]
    """
    half = MAP_SIZE / 2 * CELL_SIZE
    x += half
    y += half
    a = y // CELL_SIZE
    b = x // CELL_SIZE
    return int(a), int(b)


def get_coords_from_cell(a: int, b: int) -> tuple[float, float]:
    """
    :param a:
    :param b:
    :return: (x, y)
    Возвращает координаты центра клетки
    """
    half = MAP_SIZE / 2 * CELL_SIZE
    a *= CELL_SIZE
    b *= CELL_SIZE
    x = b - half + CELL_SIZE // 2
    y = a - half + CELL_SIZE // 2
    return x, y


def get_cell_from_list_coords(cells: list[list[int]], a: int, b: int):
    return cells[MAP_SIZE - a - 1][b]


def get_cell_from_coords(cells, x, y):
    a, b = get_cell_coords_from_coords(x, y)
    return get_cell_from_list_coords(cells, a, b)


def add_db(win_or_loose: str, score: int):
    con = sqlite3.connect(resource_path("stats.sqlite", use_abs_path=True)[0])
    cur = con.cursor()
    cur.execute(
        """INSERT INTO game_over (win_or_loose, score) VALUES (?, ?)""",
        (win_or_loose, score),
    )
    con.commit()


def select_from_db():
    con = sqlite3.connect(resource_path("stats.sqlite", use_abs_path=True)[0])
    cur = con.cursor()
    res = cur.execute("""SELECT * FROM game_over""").fetchall()
    return res
