from typing import List
from typing import Optional
from typing import Tuple


class Color(object):
    RED = None
    BLUE = None
    GREEN = None
    name: str

    def __init__(self, name: str):
        self.name = name

    @property
    def onechar(self) -> str:
        return self.name[0]


# todo make this more elegant
Color.RED = Color("red")
Color.BLUE = Color("blue")
Color.GREEN = Color("green")


class MatrixObject(object):
    _matrix: List[List[Optional[Color]]]

    def __init__(self, width=0, height=0):
        self._matrix = [[None] * width for _ in range(height)]

    def __repr__(self):
        return "\n".join("".join(b.onechar if b is not None else " " for b in row) for row in self._matrix)

    @staticmethod
    def single_colored_from_string(string: str, color: Color):
        rows: List[str] = string.splitlines(keepends=False)
        width = max(len(r) for r in rows)
        mo = MatrixObject(width, len(rows))
        # todo parse string with .isspace() and write to matrix
        for y, ro in enumerate(rows):
            for x, bl in enumerate(ro):
                mo[x, y] = None if bl.isspace() else color

    @property
    def width(self):
        return len(self._matrix[0]) if self._matrix else 0

    @property
    def height(self):
        return len(self._matrix)

    def _check_xy_bounds(self, x, y):
        if x < 0:
            raise ValueError(f"x (={x}) must not be negative")
        elif x >= self.width:
            raise ValueError(f"x (={x}) must be smaller than width (={self.width})")
        elif y < 0:
            raise ValueError(f"y (={y}) must not be negative")
        elif x >= self.height:
            raise ValueError(f"y (={y}) must be smaller than height (={self.height})")

    def __setitem__(self, key: Tuple[int, int], value: Color):
        x, y = key
        self._check_xy_bounds(x, y)
        self._matrix[y][x] = value

    def __getitem__(self, key: Tuple[int, int]) -> Color:
        x, y = key
        self._check_xy_bounds(x, y)
        return self._matrix[y][x]
