import unittest

from geometry.vec2 import vec2

class TestVec2Methods(unittest.TestCase):

    def test_setting_length_prop(self):
        v = vec2(20, 0)
        v.length = 10
        self.assertEqual(v.length, 10)
        self.assertEqual(v.x, 10)
        self.assertEqual(v.y, 0)

    def test_getting_normal(self):
        v = vec2(0, 1)
        normal = v.normal()
        self.assertEqual(normal.length, v.length)
        self.assertEqual(normal.x, -1)


if __name__ == "__main__":
    unittest.main()


