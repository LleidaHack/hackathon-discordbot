import logging

from discord import User


class QuestionPool:

    def __init__(self):
        self.__questions = {}
        self.__question_num = 0

    def add_question(self, author):
        self.__questions[self.__question_num] = author
        self.__question_num += 1

    def get_last_question(self) -> int:
        if self.__question_num == 0:
            logging.warning(f"There are 0 questions in the pool.")
        return max(0, self.__question_num - 1)

    def get_author(self, question_id: int) -> User:
        return self.__questions[question_id]
