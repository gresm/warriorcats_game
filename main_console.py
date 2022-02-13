from __future__ import annotations

import os
import data_structure as ds


def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


class Console:
    def __init__(self):
        self.text: list[str] = []
        self.header = ""

    def print(self, text: str):
        for el in text.split("\n"):
            self.text.append(el)

    def input(self, text: str = ""):
        ret = input(text)
        self.print(text + ret)
        self.update()
        return ret

    def clear(self):
        self.text = []

    def update(self):
        clear()
        if self.header:
            print(self.header)
        for el in self.text:
            print(el)


console = Console()


def main():
    while True:
        console.input("test: ")
        console.clear()
        console.update()


if __name__ == '__main__':
    main()
