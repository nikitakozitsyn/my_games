import datetime as dt
import math
import numpy as np
import os
import random as rd
import sys
import tkinter as tk


class Matrix:
    def __init__(self, name: str, side: str):
        """Creates an object that stores name of user, side length, score,
        update- flag for inserting [2] or [4] cell, lose- or win- flag, cells style,
        grid for storing cells values, cells for visual display grid.
        Checks result file if exists to show best score in current side length mode"""
        self.name = name.title() if name.isalpha() and len(name) < 7 else 'guest'
        self.side = int(side) if side.isdigit() and 9 > int(side) > 1 else 4
        self.score = 0
        self.is_update = True
        self.is_lose = [False, {'text': 'LOSE', 'fg': 'Red'}]
        self.is_win = [False, {'text': 'WIN', 'fg': 'Green'}]
        self.style = {'width': 60 // self.side, 'height': 20 // self.side, 'font': 'Arial 16', 'relief': 'sunken'}
        self.grid = np.ones((self.side, self.side), dtype=int)
        self.cells = np.array([[tk.Label(**self.style) for _ in range(self.side + 1)] for _ in range(self.side + 1)])
        for i in range(self.side + 1):
            for j in range(self.side + 1):
                self.cells[i][j].config(bg='#333' if max(i, j) == 4 else '#000', fg='White')
                self.cells[i][j].grid(row=i, column=j)
        if os.path.exists('results.csv'):
            with open('results.csv') as file:
                results = [row for row in file.read().split('\n')[1:-1] if int(row.split(',')[1]) == self.side]
                self.record = max(results, key=lambda row: (int(row.split(',')[0]), -results.index(row))).split(',')
                self.cells[0][-1].config(text=f'Leader:\n{self.record[2]}', fg='#888')
                self.cells[1][-1].config(text=f'{self.record[0]}\n{self.record[3].split()[0]}', fg='#888')
        self.cells[-1][0].config(text=f'SCORE:\n{self.score}', fg='#888')

    def binds(self, event):
        """Binds events with methods"""
        eval(f'self.{event.keysym.lower()}()') if event.keysym in ('Left', 'Right', 'Up', 'Down') else None
        self.update_labels() if self.is_update else None
        self.save_and_exit() if event.keysym == 'Escape' else None

    def check(self):
        """Checks grid for lose- flag (if all cells are full)"""
        for row, column in zip(self.grid, self.grid.T):
            for i in range(self.side - 1):
                if row[i] == row[i + 1] or column[i] == column[i + 1]:
                    return
        self.is_lose[0] = True

    def change_labels(self):
        """Transfers grid values to cells values"""
        for i in range(self.side):
            for j in range(self.side):
                color = f'#0{int(math.log(self.grid[i][j], 2)) % 16:X}{int(math.log(self.grid[i][j], 2)) * 2 % 16:X}'
                self.cells[i][j].config(text=f'{self.grid[i][j]}' if self.grid[i][j] != 1 else '', bg=color)
        self.cells[-1][0].config(text=f'SCORE:\n{self.score}')
        self.cells[-1][-1].config(self.is_lose[1] if self.is_lose[0] else self.is_win[1] if self.is_win[0] else None)

    def move(self, array):
        """Moves all values in vector given the rules of game"""
        top, prev = 0, 1
        for i in range(len(array)):
            if array[i] != 1 and array[i] != prev:
                self.is_update = True if i != top else self.is_update
                array[top], array[i], top, prev = array[i], array[top], top + 1, array[i]
            elif array[i] != 1:
                array[top - 1], array[i], prev = array[i] * 2, 1, 1
                self.score += array[top - 1]
                self.is_update = True

    def insert(self):
        """Inserts [2] or [4] value in grid in random choice"""
        cell = rd.choice([(i, j) for i in range(self.side) for j in range(self.side) if self.grid[i][j] == 1])
        self.grid[cell[0]][cell[1]] = rd.choice([2] * 9 + [4])

    def update_labels(self):
        """Updates grid by inserting value, checking for lose- or win- flag and transferring cells from grid"""
        self.insert()
        self.check() if sum(sum(self.grid > 1)) == self.side ** 2 else None
        self.is_win[0] = True if sum(sum(self.grid == 2 ** (self.side ** 2 - 2 * self.side + 3))) else self.is_win[0]
        self.change_labels()
        self.is_update = False

    def save_and_exit(self):
        """Creates result file or update it if exists and exit"""
        with open('results.csv', 'a') as file:
            None if os.stat('results.csv').st_size else file.write('Score,Side,Name,Datetime\n')
            file.write(f'{self.score},{self.side},{self.name},{dt.datetime.now().strftime("%d-%m-%y %H:%M")}\n')
        sys.exit()

    def left(self):
        """Moves all values in grid given the rules of game left direction"""
        for row in self.grid:
            self.move(row)

    def right(self):
        """Moves all values in grid given the rules of game right direction"""
        for row in self.grid:
            self.move(row[::-1])

    def up(self):
        """Moves all values in grid given the rules of game up direction"""
        for column in self.grid.T:
            self.move(column)

    def down(self):
        """Moves all values in grid given the rules of game down direction"""
        for column in self.grid.T:
            self.move(column[::-1])


def create(name, side, prev: tk.Label, root: tk.Tk):
    """Destroys previous window, calls Matrix object passing name and side length"""
    prev.destroy()
    matrix = Matrix(name.get() if type(name) != str else name, side.get() if type(side) != str else side)
    root.title(f'Hello, {matrix.name}!')
    root.bind('<Key>', matrix.binds)


def start(root: tk.Tk):
    """Calls start window(if no command line arguments), which requests name and side length"""
    root.title('start')
    name, side = tk.StringVar(), tk.StringVar()
    style = {'font': 'Arial', 'bg': '#333', 'fg': '#FFF'}
    label = tk.Label(**style)
    label.pack()
    tk.Label(label, text='"←, →, ↑, ↓" to move\n"Esc" to save and exit', **style).grid(row=0, column=2, rowspan=2)
    tk.Label(label, text='name:', **style).grid(row=0, column=0, sticky='e')
    tk.Entry(label, textvariable=name, justify='center', **style).grid(row=0, column=1)
    tk.Label(label, text='side:', **style).grid(row=1, column=0, sticky='e')
    tk.Entry(label, textvariable=side, justify='center', **style).grid(row=1, column=1)
    tk.Button(label, text='create', **style, command=lambda: create(name, side, label, root)).grid(row=2, column=1)


def main():
    root = tk.Tk()
    create(sys.argv[1], sys.argv[2], tk.Label(), root) if len(sys.argv) > 1 else start(root)
    root.mainloop()


if __name__ == '__main__':
    main()
