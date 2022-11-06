import unittest

from pattern_cutting.geometry.Vector import Vector


class TestVectorMethods(unittest.TestCase):
    def test_setting_length_prop(self):
        v = Vector(20, 0)
        v.length = 10
        self.assertEqual(v.length, 10)
        self.assertEqual(v.x, 10)
        self.assertEqual(v.y, 0)

    def test_getting_normal(self):
        v = Vector(0, 1)
        normal = v.normal()
        self.assertEqual(normal.length, v.length)
        self.assertEqual(normal.x, -1)


if __name__ == "__main__":
    unittest.main()
