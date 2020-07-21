import ctypes
import os
import time
from typing import List
from typing import Optional

import pygame

import const
from model.base import MatrixObject
from model.game import Game

SCALE = 0.5
FPS = 100

if os.name == 'nt':
    SCALE *= ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    ctypes.windll.user32.SetProcessDPIAware()
else:
    SCALE *= 1

const.scale(SCALE)


def sc(*args):
    return tuple(round(a * SCALE) for a in args) if len(args) != 1 else round(args[0] * SCALE)


FONT32: Optional[pygame.font.SysFont] = None
FONT72: Optional[pygame.font.SysFont] = None


class PygameView(object):
    def __init__(self, game: Game):
        self.height = const.BOARD_HEIGHT * const.BOARD_TILE_PX
        self.width = const.BOARD_WIDTH * const.BOARD_TILE_PX + 2 * const.SIDEBAR_WIDTH_PX
        self.game = game
        self.screen = None
        self.pressed_keys = {}
        self.scheduler = TickScheduler()

    def start(self):
        global FONT32, FONT72
        pygame.init()
        pygame.display.set_caption("pytetris")
        FONT32 = pygame.font.SysFont(None, sc(32))
        FONT72 = pygame.font.SysFont(None, sc(72))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.scheduler.add_task(20, self.game.update_tetromino_fall)
        self.scheduler.add_task(1, self.redraw_screen)
        self.scheduler.add_task(4, self.check_repeating_keys)

    def run(self):
        running = True

        while running:
            start = time.perf_counter()
            for event in pygame.event.get():
                if event.type != pygame.MOUSEMOTION:
                    print(event)
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.pressed_keys[event.key] = 0
                    if event.key == pygame.K_LEFT:
                        self.game.input_move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.game.input_move_right()
                    elif event.key == pygame.K_UP:
                        self.game.input_turn_clockwise()
                    elif event.key == pygame.K_a:
                        self.game.input_turn_clockwise()
                    elif event.key == pygame.K_d:
                        self.game.input_turn_counterclockwise()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.KEYUP:
                    del self.pressed_keys[event.key]

            self.scheduler.run()
            loop_time = time.perf_counter() - start
            # print(f"loop time: {round(loop_time, 3)}s")
            time.sleep(max(0, 1 / FPS - loop_time))
        self.exit()

    def check_repeating_keys(self):
        if pygame.K_DOWN in self.pressed_keys:
            self.game.input_move_down()
        if pygame.K_LEFT in self.pressed_keys:
            if self.pressed_keys[pygame.K_LEFT] >= 10:
                self.game.input_move_left()
            else:
                self.pressed_keys[pygame.K_LEFT] += 1
        if pygame.K_RIGHT in self.pressed_keys:
            if self.pressed_keys[pygame.K_RIGHT] >= 10:
                self.game.input_move_right()
            else:
                self.pressed_keys[pygame.K_RIGHT] += 1

    def redraw_screen(self):
        self.screen.fill((0, 0, 0))
        board_left = self.width // 2 - (const.BOARD_WIDTH * const.BOARD_TILE_PX // 2)
        board_right = self.width // 2 + (const.BOARD_WIDTH * const.BOARD_TILE_PX // 2)
        for xx in range(const.BOARD_WIDTH):
            for yy in range(const.BOARD_HEIGHT):
                rect = (board_left + xx * const.BOARD_TILE_PX, yy * const.BOARD_TILE_PX,
                        const.BOARD_TILE_PX, const.BOARD_TILE_PX)
                pygame.draw.rect(self.screen, (25, 25, 25), rect, 2)
                board_color = self.game.get_color_at(xx, yy)
                if board_color is not None:
                    pygame.draw.rect(self.screen, board_color.rgb, rect)

        fimg = FONT32.render("Rows:", True, (255, 255, 255))
        y1 = round(self.height * 0.8)
        self.screen.blit(fimg, (board_left // 2 - fimg.get_rect().width // 2, y1))

        y2 = y1 + fimg.get_rect().height + sc(8)
        fimg = FONT72.render(str(self.game.rows), True, (255, 255, 255))
        self.screen.blit(fimg, (board_left // 2 - fimg.get_rect().width // 2, y2))

        right_sidebar_middle = (board_right + self.width) // 2

        fimg = FONT32.render("Next:", True, (255, 255, 255))
        y1 = self.height // 10
        self.screen.blit(fimg, (right_sidebar_middle - fimg.get_rect().width // 2, y1))
        y2 = y1 + fimg.get_rect().height + sc(8)
        self.draw_matrix_object(self.game.tetromino_queue[1].shape, right_sidebar_middle, y2)

        pygame.display.update()

    def draw_matrix_object(self, obj: MatrixObject, x_center: int, y_top: int) -> None:
        x_left = round(x_center - const.BOARD_TILE_PX * obj.width / 2)
        for x, y in obj.all_colored_coords():
            pygame.draw.rect(self.screen, obj[x, y].rgb,
                             (x_left + x * const.BOARD_TILE_PX, y_top + y * const.BOARD_TILE_PX,
                              const.BOARD_TILE_PX, const.BOARD_TILE_PX))

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
