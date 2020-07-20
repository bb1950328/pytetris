import ctypes
import os
import time

import pygame

import const
from model.game import Game

if os.name == 'nt':
    SCALE = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    ctypes.windll.user32.SetProcessDPIAware()
else:
    SCALE = 1


def sc(*args):
    return tuple(round(a * SCALE) for a in args) if len(args) != 1 else round(args[0] * SCALE)


class PygameView(object):
    def __init__(self, game: Game):
        self.height = const.BOARD_HEIGHT * const.BOARD_TILE_PX
        self.width = const.BOARD_WIDTH * const.BOARD_TILE_PX + 2 * const.SIDEBAR_WIDTH_PX
        self.game = game
        self.screen = None

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(sc(self.width, self.height))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type != pygame.MOUSEMOTION:
                    print(event)
                if event.type == pygame.QUIT:
                    running = False
            self.draw_board()
            self.game.update_tetromino_fall()
            time.sleep(0.2)
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
