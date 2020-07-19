import unittest

from model.base import Color
from model.base import MatrixObject


class TestBase(unittest.TestCase):
    def test_matrix_object1(self):
        mo = MatrixObject(2, 3)
        mo[0, 1] = Color.RED
        mo[1, 2] = Color.BLUE
        self.assertEqual("  \nr \n b", repr(mo))

    def test_matrix_object2(self):
        mo = MatrixObject(2, 3)

        def assign_x_too_big():
            mo[2, 2] = Color.RED

        def assign_y_too_big():
            mo[2, 3] = Color.RED

        self.assertRaises(ValueError, assign_x_too_big)
        self.assertRaises(ValueError, assign_y_too_big)


if __name__ == '__main__':
    unittest.main()
