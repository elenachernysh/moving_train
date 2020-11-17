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
        "|_ : () :     ,-, |\\",
        "' -\ '==/=====o)--|\\\\"
    )

    def __init__(self, speed: float):
        self.speed = speed

    @property
    def distance(self):
        (width, height) = os.get_terminal_size()
        return width

    @property
    def the_most_long_part(self):
        return len(max(self.train, key=len))

    def staying(self):
        print('\n'.join(self.train))

    @staticmethod
    def replace_all_left_lines(string_to_search: str):
        list_index_line = [m.start() for m in re.finditer("/", string_to_search)]
        return [string_to_search[:r] + r"\\" + string_to_search[r+1:] for r in list_index_line]

    @staticmethod
    def replace_all_right_lines(string_to_search: str):
        list_index_line = [m.start() for m in re.finditer(r"\\", string_to_search)]
        return [string_to_search[:r] + "/" + string_to_search[r + 1:] for r in list_index_line]

    def reverse_train(self):
        # print([self.replace_all_left_lines(d) for d in self.train])
        # print([self.replace_all_right_lines(d) for d in self.train])
        return [" " * (self.the_most_long_part+1-len(i)) + i[::-1] for i in self.train]

    def moving_right(self):
        for i in range(1, self.distance):
            if i >= self.distance-self.the_most_long_part:
                end = self.the_most_long_part-abs(self.distance-(i+self.the_most_long_part))
                print('\n'.join((i * " ") + t[:end] for t in self.train))
            else:
                print('\n'.join((i * " ") + t for t in self.train))
            time.sleep(self.speed)
            os.system('clear')

    def moving_left(self, i):
        for i in range(self.distance, 1, -1):
            print('\n'.join((i * " ") + t for t in self.reverse_train()))
            time.sleep(self.speed)
            os.system('clear')


train = Train(speed=0.05)
train.moving_right()
# train.reverse_train()

