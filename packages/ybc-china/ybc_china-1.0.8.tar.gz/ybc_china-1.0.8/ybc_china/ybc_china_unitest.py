import unittest


class MyTestCase(unittest.TestCase):
    def test_what(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()