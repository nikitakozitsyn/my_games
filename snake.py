import random
import sys
import tkinter as tk


class Matrix:
    DIRECTIONS = {'Left': (-10, 0), 'Right': (10, 0), 'Up': (0, -10), 'Down': (0, 10)}

    def __init__(self):
        self.state = None
        self.pause = False
        self.grid = [(i, j) for i in range(2, 400, 10) for j in range(2, 500, 10)]
        self.snake_grid = [(2, 2)]
        self.direction = (10, 0)
        self.snake = [window.create_rectangle(i, j, i + 10, j + 10, fill='#0F0') for i, j in self.snake_grid]
        self.food_grid = random.choice(list(set(self.grid) - set(self.snake_grid)))
        self.food = [window.create_rectangle(i, j, i + 10, j + 10, fill='#F00') for i, j in [self.food_grid]]
        self.speed = 200
        self.score = 0

    def motion(self):
        self.snake_grid.append((self.snake_grid[-1][0] + self.direction[0], self.snake_grid[-1][1] + self.direction[1]))
        if self.snake_grid[-1] not in self.grid or self.snake_grid[-1] in self.snake_grid[:-1]:
            sys.exit()
        if self.snake_grid[-1] != self.food_grid:
            self.snake_grid = self.snake_grid[1:]
            window.delete(self.snake[0])
        else:
            self.score += 1
            count.config(text=f'SCORE:\n{self.score}')
            self.speed -= 4 if self.speed > 100 else 2 if self.speed > 50 else 1
            window.delete(self.food[0])
            self.food_grid = random.choice(list(set(self.grid) - set(self.snake_grid)))
            self.food = [window.create_rectangle(i, j, i + 10, j + 10, fill='#F00') for i, j in [self.food_grid]]
        [window.delete(i) for i in self.snake]
        self.snake = [window.create_rectangle(i, j, i + 10, j + 10, fill='#0F0') for i, j in self.snake_grid]
        self.state = root.after(self.speed, self.motion)

    def binds(self, event):
        if self.DIRECTIONS.get(event.keysym) in set(self.DIRECTIONS.values()) - {self.direction} and not self.pause:
            root.after_cancel(self.state)
            self.direction = self.DIRECTIONS[event.keysym]
            self.motion()
        if event.keysym == 'Return':
            if self.pause:
                self.motion()
                self.pause = False
            else:
                root.after_cancel(self.state)
                self.pause = True
        sys.exit() if event.keysym == 'Escape' else None


root = tk.Tk()
s = tk.Label(bg='#333')
s.pack()
window = tk.Canvas(s, width=401, height=501, bg='#333')
window.grid(row=0, column=0)
count = tk.Label(s, height=26, width=8, bg='#333', font='Arial 12 bold', text='SCORE:\n0')
count.grid(row=0, column=1)
matrix = Matrix()
matrix.motion()
root.bind('<Key>', matrix.binds)
root.mainloop()
