import unittest

from src.modules.pools.questions import QuestionPool

AUTHOR1, AUTHOR2 = "AUTHOR1", "AUTHOR2"


class TestQuestionPool(unittest.TestCase):

    def setUp(self):
        self.pool = QuestionPool()

    def test_has_questions(self):
        self.pool.add_question(AUTHOR1)
        self.assertEqual(0, self.pool.get_last_question())

    def test_has_no_questions(self):
        self.assertEqual(0, self.pool.get_last_question())

    def test_get_author(self):
        self.pool.add_question(AUTHOR1)
        question1 = self.pool.get_last_question()
        self.assertEqual(AUTHOR1, self.pool.get_author(question1))

    def test_get_author2(self):
        authors = [AUTHOR1, AUTHOR2, AUTHOR1]
        questions = []
        for a in authors:
            self.pool.add_question(a)
            questions.append(self.pool.get_last_question())
        [self.assertEqual(a, self.pool.get_author(q), msg=f"{a}: {q}") for a, q in zip(authors, questions)]


if __name__ == '__main__':
    unittest.main()
