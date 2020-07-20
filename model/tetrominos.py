from typing import Optional

from model.base import Color
from model.base import MatrixObject


class Tetromino(object):
    I = None
    J = None
    L = None
    O = None
    S = None
    T = None
    Z = None
    ALL = None

    def __init__(self, shape: MatrixObject):
        self._shape = shape

    @property
    def shape(self) -> MatrixObject:
        return self._shape


Tetromino.I = Tetromino(MatrixObject.single_colored_from_string("#\n#\n#\n#", Color.LIGHT_BLUE))
Tetromino.J = Tetromino(MatrixObject.single_colored_from_string("#  \n###", Color.BLUE))
Tetromino.L = Tetromino(MatrixObject.single_colored_from_string("  #\n###", Color.ORANGE))
Tetromino.O = Tetromino(MatrixObject.single_colored_from_string("##\n##", Color.YELLOW))
Tetromino.S = Tetromino(MatrixObject.single_colored_from_string(" ##\n## ", Color.GREEN))
Tetromino.T = Tetromino(MatrixObject.single_colored_from_string(" # \n###", Color.PURPLE))
Tetromino.Z = Tetromino(MatrixObject.single_colored_from_string("## \n ##", Color.RED))

Tetromino.ALL = [Tetromino.I, Tetromino.J, Tetromino.L, Tetromino.O, Tetromino.S, Tetromino.T, Tetromino.Z]
