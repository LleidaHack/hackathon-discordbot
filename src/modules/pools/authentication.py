class AuthenticationPool:

    def __init__(self):
        self.__middle_people = set()
        self.LIMIT_PEOPLE = 500
        self.MAX_RECOVER = 20
        self.last_people = list()

    def add_newbie(self, author):
        if len(self.__middle_people) > self.LIMIT_PEOPLE:
            self.__middle_people = set(self.last_people)
        self.__middle_people.add(author)
        if len(self.last_people) >= self.MAX_RECOVER:
            self.last_people = self.last_people[1:]
            self.last_people.append(author)

    def finish_login(self, author):
        self.__middle_people.remove(author)

    def has(self, author) -> bool:
        return author in self.__middle_people
