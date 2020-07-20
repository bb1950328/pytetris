import unittest

from model.base import Color
from model.base import MatrixObject


class TestBase(unittest.TestCase):
    def test_matrix_object1(self):
        mo = MatrixObject(2, 3)
        mo[0, 1] = Color.RED
        mo[1, 2] = Color.BLUE
        self.assertEqual("  \nr \n b", repr(mo))
        self.assertEqual(Color.RED, mo[0, 1])
        self.assertEqual(Color.BLUE, mo[1, 2])
        self.assertEqual(None, mo[0, 0])

    def test_matrix_object2(self):
        mo = MatrixObject(2, 3)
        self.assertEqual(2, mo.width)
        self.assertEqual(3, mo.height)
        mo[0, 1] = Color.RED
        mo[0, 0] = Color.YELLOW
        mo[1, 2] = Color.BLUE
        before = repr(mo)
        mo.rotate_clockwise()
        self.assertEqual(" ry\nb  ", repr(mo))
        mo.rotate_counterclockwise()
        self.assertEqual(before, repr(mo))
        for _ in range(4):
            mo.rotate_clockwise()
        self.assertEqual(before, repr(mo))
        for _ in range(4):
            mo.rotate_counterclockwise()
        self.assertEqual(before, repr(mo))

    def test_matrix_object3(self):
        mo = MatrixObject(2, 3)

        def assign_x_too_big():
            mo[2, 2] = Color.RED

        def assign_y_too_big():
            mo[2, 3] = Color.RED

        self.assertRaises(ValueError, assign_x_too_big)
        self.assertRaises(ValueError, assign_y_too_big)

    def test_matrix_object_4(self):
        mo = MatrixObject(2, 3)
        mo[1, 1] = Color.RED
        mo[0, 2] = Color.BLUE
        self.assertEqual({(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)}, set(mo.all_coords()))
        self.assertEqual({(1, 1), (0, 2)}, set(mo.all_colored_coords()))


if __name__ == '__main__':
    unittest.main()
