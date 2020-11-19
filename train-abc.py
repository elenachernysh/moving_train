import sys
import time
import os
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
        "|______: ///|\\\\\\",
        "|      | \-----/",
        "|      |  \   /",
        "|      |___,_._,--",
        "|          |:| |  |",
        "|   .--.   |:| |  c",
        "|  /    \  |:| |  |",
        "|_ : || :     ,-, |\\",
        "' -\ '==/=====o|--|\\\\"
    )

    def __init__(self, speed: float) -> None:
        self.speed = speed

    @property
    def the_most_long_part(self) -> int:
        return len(max(self.train, key=len))

    @staticmethod
    def find_indexes_of_symbols_in_string(symbol: str, string_to_search: list) -> list:
        return [i for i, x in enumerate(string_to_search) if x == symbol]

    @staticmethod
    def replace_symbols_by_index(string_to_search: list, new_symbol: str, index_list: list) -> str:
        for i in index_list:
            string_to_search[i] = new_symbol
        return ''.join(chr(int(i)) for i in string_to_search)

    @staticmethod
    def string_to_ascii(string: str):
        return [str(ord(i)) for i in string]

    def train_str_to_ascii(self):
        return [self.string_to_ascii(i) for i in self.train]

    @staticmethod
    def ascii_to_string(string_list: list) -> str:
        return ''.join(chr(int(i)) for i in string_list)

    def train_ascii_to_str(self):
        return [self.ascii_to_string(i) for i in self.train_str_to_ascii()]

    def replace_all_symbols(self, string_to_search: str) -> str:
        ascii_string = self.string_to_ascii(string_to_search)
        list_index_left_lines = self.find_indexes_of_symbols_in_string(symbol='47', string_to_search=ascii_string)
        list_index_right_lines = self.find_indexes_of_symbols_in_string(symbol='92', string_to_search=ascii_string)
        string_to_search = self.replace_symbols_by_index(string_to_search=ascii_string, new_symbol='92',
                                                         index_list=list_index_left_lines)
        string_to_search = self.replace_symbols_by_index(string_to_search=ascii_string, new_symbol='47',
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
