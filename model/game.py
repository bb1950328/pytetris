import collections
import random
from typing import Deque
from typing import List
from typing import Optional
from typing import Tuple

import const
from model.base import MatrixObject
from model.tetrominos import Tetromino


class Game(object):
    def __init__(self):
        self.board = MatrixObject(const.BOARD_WIDTH, const.BOARD_HEIGHT)
        self.tetromino_queue: Deque[Tetromino] = collections.deque()
        self.active_tetromino_pos: Optional[List[int, int]] = None
        self.tetromino_last_step = False
        self._fill_tetromino_queue()

    def _fill_tetromino_queue(self):
        while len(self.tetromino_queue) < 10:
            self.tetromino_queue.append(random.choice(Tetromino.ALL))

    def get_color_at(self, x, y):
        board_color = self.board[x, y]
        if board_color is not None:
            return board_color
        elif self.active_tetromino_pos is not None:
            ap_x, ap_y = self.active_tetromino_pos
            tx = x - ap_x
            ty = y - ap_y
            if self.tetromino_queue[0].shape.are_xy_valid(tx, ty):
                at_color = self.tetromino_queue[0].shape[tx, ty]
                if at_color is not None:
                    return at_color
        return None

    def update_tetromino_fall(self):
        at = self.tetromino_queue[0]
        if self.active_tetromino_pos is None:
            self.active_tetromino_pos = [const.BOARD_WIDTH // 2 - at.shape.width // 2, 0]
        else:
            at_x, at_y = self.active_tetromino_pos
            for tx, ty in at.shape.all_colored_coords():
                if self.board[at_x + tx, at_y + 1 + ty] is not None or at_y + ty == const.BOARD_HEIGHT - 1:
                    if self.tetromino_last_step:
                        self.freeze_active_tetromino()
                    else:
                        self.tetromino_last_step = True
                    break
            else:
                self.tetromino_last_step = False
                self.active_tetromino_pos[1] += 1

    def freeze_active_tetromino(self):
        at = self.tetromino_queue.popleft()
        at_x, at_y = self.active_tetromino_pos
        for tx, ty in at.shape.all_colored_coords():
            self.board[at_x + tx, at_y + ty] = at.shape[tx, ty]
