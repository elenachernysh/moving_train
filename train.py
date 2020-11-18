import time
import os
import re


class Train:
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

    def __init__(self, speed: float):
        self.speed = speed

    @property
    def distance(self) -> int:
        width, _ = os.get_terminal_size()
        return width

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

    def replace_all_symbols(self, string_to_search: str) -> str:
        list_index_left_lines = self.find_indexes_of_symbols_in_string(symbol="/", string_to_search=string_to_search)
        list_index_right_lines = self.find_indexes_of_symbols_in_string(symbol=r"\\", string_to_search=string_to_search)
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
        for i in range(1, self.distance):
            if self.distance-self.the_most_long_part <= i < self.distance-1:
                end = self.the_most_long_part-abs(self.distance-(i+self.the_most_long_part))
                print('\n'.join((i * " ") + t[:end] for t in self.train))
            elif i == self.distance-1:
                self.moving_left(i)
            else:
                print('\n'.join((i * " ") + t for t in self.train))
            # print(*self.train, sep=i * " " + "\n")
            time.sleep(self.speed)
            os.system('clear')

    def moving_left(self, i):
        for i in range(self.distance, 1, -1):
            end = self.distance - i
            print('\n'.join((i * " ") + t[:end] for t in self.reverse_train()))
            time.sleep(self.speed)
            os.system('clear')


train = Train(speed=0.05)
train.moving_right()
