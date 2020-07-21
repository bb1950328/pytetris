import collections
import copy
import random
from typing import Deque
from typing import List
from typing import Optional

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
        self.rows = 0

    def _fill_tetromino_queue(self):
        while len(self.tetromino_queue) < 10:
            self.tetromino_queue.append(copy.deepcopy(random.choice(Tetromino.ALL)))

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
            if self.is_active_tetromino_colliding(0, 1):
                if self.tetromino_last_step:
                    self._freeze_active_tetromino()
                else:
                    self.tetromino_last_step = True
            else:
                self.tetromino_last_step = False
                self.active_tetromino_pos[1] += 1

    def is_active_tetromino_colliding(self, delta_x: int, delta_y: int) -> bool:
        if self.active_tetromino_pos is not None:
            at_x, at_y = self.active_tetromino_pos
            for tx, ty in self.tetromino_queue[0].shape.all_colored_coords():
                if at_y + ty >= const.BOARD_HEIGHT - 1 \
                        or not (0 <= at_x + tx + delta_x < const.BOARD_WIDTH) \
                        or self.board[at_x + delta_x + tx, at_y + delta_y + ty] is not None:
                    return True
        return False

    def _freeze_active_tetromino(self):
        at = self.tetromino_queue.popleft()
        at_x, at_y = self.active_tetromino_pos
        for tx, ty in at.shape.all_colored_coords():
            self.board[at_x + tx, at_y + ty] = at.shape[tx, ty]
        self.active_tetromino_pos = None
        self._fill_tetromino_queue()
        self.check_full_rows()

    def input_move_left(self):
        if not self.is_active_tetromino_colliding(-1, 0) and self.active_tetromino_pos is not None:
            self.active_tetromino_pos[0] -= 1

    def input_move_right(self):
        if not self.is_active_tetromino_colliding(1, 0) and self.active_tetromino_pos is not None:
            self.active_tetromino_pos[0] += 1

    def input_move_down(self):
        if not self.is_active_tetromino_colliding(0, 1) and self.active_tetromino_pos is not None:
            self.active_tetromino_pos[1] += 1

    def input_turn_clockwise(self):
        self.tetromino_queue[0].shape.rotate_clockwise()

    def input_turn_counterclockwise(self):
        self.tetromino_queue[0].shape.rotate_counterclockwise()

    def check_full_rows(self):
        y = self.board.height - 1
        while y >= 0:
            full = True
            for x in range(self.board.width):
                if self.board[x, y] is None:
                    full = False
            if full:
                print(f"row {y} is full")
                for x2 in range(self.board.width):
                    self.board[x2, y] = None
                for y2 in range(y - 1, -1, -1):
                    for x3 in range(self.board.width):
                        self.board[x3, y2 + 1] = self.board[x3, y2]
                self.rows += 1
            else:
                y -= 1
