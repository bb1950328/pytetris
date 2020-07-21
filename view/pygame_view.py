import ctypes
import os
import time
from typing import List

import pygame

import const
from model.game import Game

SCALE = 0.5

if os.name == 'nt':
    SCALE *= ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    ctypes.windll.user32.SetProcessDPIAware()
else:
    SCALE *= 1

const.scale(SCALE)


def sc(*args):
    return tuple(round(a * SCALE) for a in args) if len(args) != 1 else round(args[0] * SCALE)


class PygameView(object):
    def __init__(self, game: Game):
        self.height = const.BOARD_HEIGHT * const.BOARD_TILE_PX
        self.width = const.BOARD_WIDTH * const.BOARD_TILE_PX + 2 * const.SIDEBAR_WIDTH_PX
        self.game = game
        self.screen = None
        self.scheduler = TickScheduler()

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.scheduler.add_task(20, self.game.update_tetromino_fall)
        self.scheduler.add_task(1, self.draw_board)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type != pygame.MOUSEMOTION:
                    print(event)
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.game.input_move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.game.input_move_right()
                    elif event.key == pygame.K_a:
                        self.game.input_turn_clockwise()
                    elif event.key == pygame.K_d:
                        self.game.input_turn_clockwise()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            self.scheduler.run()
            time.sleep(0.02)
        self.exit()

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        x1 = self.width // 2 - (const.BOARD_WIDTH * const.BOARD_TILE_PX // 2)
        for xx in range(const.BOARD_WIDTH):
            for yy in range(const.BOARD_HEIGHT):
                rect = (x1 + xx * const.BOARD_TILE_PX, yy * const.BOARD_TILE_PX,
                        const.BOARD_TILE_PX, const.BOARD_TILE_PX)
                pygame.draw.rect(self.screen, (25, 25, 25), rect, 2)
                board_color = self.game.get_color_at(xx, yy)
                if board_color is not None:
                    pygame.draw.rect(self.screen, board_color.rgb, rect)
        pygame.display.update()

    def exit(self):
        pygame.quit()


class TickScheduler(object):
    class Task(object):
        func: callable
        count: int
        args: tuple
        kwargs: dict

        def __init__(self, count, func, *args, **kwargs):
            self.count = count
            self.func = func
            self.args = args
            self.kwargs = kwargs

        def call(self):
            self.func(*self.args, **self.kwargs)

    def __init__(self):
        self.tasks = []
        self.counters: List[int] = [0]

    def add_task(self, count, func, *args, **kwargs):
        self.tasks.append(TickScheduler.Task(count, func, *args, **kwargs))
        self.counters.append(0)

    def run(self):
        for i, task in enumerate(self.tasks):
            c = self.counters[i] + 1
            if c > task.count:
                task.call()
                c = 0
            self.counters[i] = c
