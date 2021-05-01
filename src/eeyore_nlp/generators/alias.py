import random
from typing import Set


class Alias():
    def __init__(self, starter_phrase: str = '', size: int = 100):
        self.__min = 0
        self.__max = 25
        self.__cache: Set[str] = set()

        self.__size = size
        self.__starter_phrase = starter_phrase
        self.__mapper = dict(enumerate('abcdefghijklmnopqrstuvwxyz'))

    def get_alias(self) -> str:
        keep_generating = True
        while keep_generating:
            random_string = self.generate_random_string()
            keep_generating = random_string in self.__cache

        self.__cache.add(random_string)

        return f'{self.__starter_phrase}{random_string}'

    def reset_cache(self):
        self.__cache.clear()

    def generate_random_string(self) -> str:
        random_int_array = (
            random.randint(self.__min, self.__max)
            for _
            in range(self.__size + 1)
        )

        random_generated_string = (
            self.__mapper[i]
            for i
            in random_int_array
        )

        return ''.join(random_generated_string)
