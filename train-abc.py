import sys
import time
import os
import re
from abc import ABC
from typing import Optional


class MovableObject(ABC):
    _space_left = None

    @property
    def distance(self) -> int:
        width, _ = os.get_terminal_size()
        return width

    @property
    def space_left(self) -> Optional[int]:
        return self._space_left

    @space_left.setter
    def space_left(self, some_value: int) -> None:
        self.space_left = some_value

    def moving_distance(self, current_position: int, the_most_long_part: int) -> Optional[int]:
        if self.distance - the_most_long_part <= current_position < self.distance - 1:
            self._space_left = the_most_long_part - abs(self.distance - (current_position + the_most_long_part))
        return self.space_left


class Train(MovableObject):
    train = (
        ",------,  _____",
        "|______: \57\57\57|\134\134\134",
        "|      | \-----/",
        "|      |  \   /",
        "|      |___,_._,--",
        "|          |:| |  |",
        "|   .--.   |:| |  c",
        "|  /    \  |:| |  |",
        "|_ : || :     ,-, |\134",
        "' -\ '==/=====o|--|\134\134"
    )

    def __init__(self, speed: float) -> None:
        self.speed = speed

    @property
    def the_most_long_part(self) -> int:
        return len(max(self.train, key=len))

    @staticmethod
    def find_indexes_of_symbols_in_string(symbol: str, string_to_search: str) -> list:
        return [m.start() for m in re.finditer(symbol, string_to_search)]

    @staticmethod
    def replace_symbols_by_index(string_to_search: str, new_symbol: str, index_list: list) -> str:
        for i in index_list:
            string_to_search = string_to_search[:i] + new_symbol + string_to_search[i+1:]
        return string_to_search

    @staticmethod
    def clear():
        return os.system('clear')

    def replace_all_symbols(self, string_to_search: str) -> str:
        list_index_left_lines = self.find_indexes_of_symbols_in_string(symbol=chr(ord('/')), string_to_search=string_to_search)
        list_index_right_lines = self.find_indexes_of_symbols_in_string(symbol=r'\\', string_to_search=string_to_search)

        string_to_search = self.replace_symbols_by_index(string_to_search=string_to_search, new_symbol="\\",
                                                         index_list=list_index_left_lines)
        string_to_search = self.replace_symbols_by_index(string_to_search=string_to_search, new_symbol="/",
                                                         index_list=list_index_right_lines)
        return string_to_search

    def staying(self):
        print('\n'.join(self.train))

    def reverse_train(self) -> list:
        return [" " * (self.the_most_long_part+1-len(i)) + self.replace_all_symbols(i[::-1]) for i in self.train]

    def moving_right(self):
        try:
            for i in range(1, self.distance):
                super(Train, self).moving_distance(current_position=i, the_most_long_part=self.the_most_long_part)
                end = self.space_left if self.space_left else self.distance
                if i == self.distance - 1:
                    self.moving_left(i)
                else:
                    print('\033[93m\n'.join((i * " ") + t[:end] for t in self.train))
                time.sleep(self.speed)
                os.system('clear')
        except KeyboardInterrupt:
            sys.exit(0)

    def moving_left(self, i):
        for i in range(self.distance, 1, -1):
            end = self.distance - i
            print('\033[93m\n'.join((i * " ") + t[:end] for t in self.reverse_train()))
            time.sleep(self.speed)
            os.system('clear')


train = Train(speed=0.05)
train.moving_right()

