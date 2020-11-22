import unittest


class TestWebUser(unittest.TestCase):

    def setUp(self):
        self.foo = 123

    def test_default_widget_size(self):
        self.assertEqual(123, self.foo)


if __name__ == '__main__':
    unittest.main()
