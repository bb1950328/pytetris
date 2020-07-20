from typing import List
from typing import Optional
from typing import Tuple


class Color(object):
    PURPLE = None
    YELLOW = None
    ORANGE = None
    LIGHT_BLUE = None
    RED = None
    BLUE = None
    GREEN = None
    name: str

    def __init__(self, name: str, hexcode: str):
        self.name = name
        self._hexcode = hexcode

    @property
    def onechar(self) -> str:
        return self.name[0]

    @property
    def hexcode(self):
        return self._hexcode

    @property
    def rgb(self):
        stripped = self._hexcode.lstrip('#')
        return tuple(int(stripped[i:i + 2], 16) for i in (0, 2, 4))


Color.PURPLE = Color("purple", "##FF00FF")
Color.YELLOW = Color("yellow", "##FFFF00")
Color.ORANGE = Color("orange", "##FF6300")
Color.LIGHT_BLUE = Color("lightblue", "#00FFFF")
Color.RED = Color("red", "#FF0000")
Color.BLUE = Color("blue", "#0000FF")
Color.GREEN = Color("green", "#00FF00")


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
        for y, ro in enumerate(rows):
            for x, bl in enumerate(ro):
                mo[x, y] = None if bl.isspace() else color
        return mo

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
        elif y >= self.height:
            raise ValueError(f"y (={y}) must be smaller than height (={self.height})")

    def are_xy_valid(self, x: int, y: int) -> bool:
        try:
            self._check_xy_bounds(x, y)
            return True
        except ValueError:
            return False

    def __setitem__(self, key: Tuple[int, int], value: Color):
        x, y = key
        self._check_xy_bounds(x, y)
        self._matrix[y][x] = value

    def __getitem__(self, key: Tuple[int, int]) -> Color:
        x, y = key
        self._check_xy_bounds(x, y)
        return self._matrix[y][x]

    def rotate_clockwise(self):
        self._matrix = [list(row) for row in zip(*self._matrix[::-1])]

    def rotate_counterclockwise(self):
        self._matrix = [list(row) for row in zip(*self._matrix)][::-1]

    def all_coords(self):
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

    def all_colored_coords(self):
        return filter(lambda xy: self[xy] is not None, self.all_coords())
