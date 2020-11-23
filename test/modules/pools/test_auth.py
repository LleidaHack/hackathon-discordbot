import unittest

from src.modules.pools.authentication import AuthenticationPool


class TestAuthPool(unittest.TestCase):

    def setUp(self):
        self.pool = AuthenticationPool()

    def test_finish_not_loggin(self):
        self.assertRaises(KeyError, lambda: self.pool.finish_login(432))

    def test_add_one_hacker(self):
        author = 1
        self.pool.add_newbie(author)
        self.assertTrue(self.pool.has(author))

    def test_add_two_hacker(self):
        authors = [1, 2]
        [self.pool.add_newbie(a) for a in authors]
        [self.assertTrue(self.pool.has(a)) for a in authors]

    def test_add_finish_hacker(self):
        author = 1
        self.pool.add_newbie(author)
        self.pool.finish_login(author)
        self.assertRaises(KeyError, lambda: self.pool.finish_login(author))

    def finish_asyncrhonous_hackers(self):
        authors = [1, 2]
        [self.pool.add_newbie(a) for a in authors]
        self.pool.finish_login(authors[1])
        self.assertTrue(self.pool.has(authors[1]))
        self.assertRaises(KeyError, lambda: self.pool.finish_login(authors[1]))
        self.assertTrue(self.pool.has(authors[0]))
        self.pool.finish_login(authors[0])
        self.assertTrue(self.pool.has(authors[0]))
        self.assertRaises(KeyError, lambda: self.pool.finish_login(authors[0]))


if __name__ == '__main__':
    unittest.main()
