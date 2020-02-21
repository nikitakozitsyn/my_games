import random
import sys
import tkinter as tk


class Matrix:
    DIRECTIONS = {'Left': (-10, 0), 'Right': (10, 0), 'Up': (0, -10), 'Down': (0, 10)}

    def __init__(self):
        self.grid = [(i, j) for i in range(0, 400, 10) for j in range(0, 500, 10)]
        self.snake_grid = [random.choice(self.grid)]
        self.direction = random.choice(list(self.DIRECTIONS.values()))
        self.snake = [window.create_rectangle(i, j, i + 10, j + 10, fill='#0F0') for i, j in self.snake_grid]
        self.food_grid = random.choice(list(set(self.grid) - set(self.snake_grid)))
        self.food = [window.create_rectangle(i, j, i + 10, j + 10, fill='#F00') for i, j in [self.food_grid]]
        self.speed = 200

    def motion(self):
        self.snake_grid.append((self.snake_grid[-1][0] + self.direction[0], self.snake_grid[-1][1] + self.direction[1]))
        if self.snake_grid[-1] not in self.grid or self.snake_grid[-1] in self.snake_grid[:-1]:
            sys.exit()
        if self.snake_grid[-1] != self.food_grid:
            self.snake_grid = self.snake_grid[1:]
            window.delete(self.snake[0])
        else:
            self.speed -= 4 if self.speed > 100 else 2 if self.speed > 50 else 1
            window.delete(self.food[0])
            self.food_grid = random.choice(list(set(self.grid) - set(self.snake_grid)))
            self.food = [window.create_rectangle(i, j, i + 10, j + 10, fill='#F00') for i, j in [self.food_grid]]
        [window.delete(i) for i in self.snake]
        self.snake = [window.create_rectangle(i, j, i + 10, j + 10, fill='#0F0') for i, j in self.snake_grid]
        root.after(self.speed, self.motion)

    def binds(self, event):
        self.direction = self.DIRECTIONS[event.keysym] if event.keysym in (
            'Left', 'Right', 'Up', 'Down') else self.direction
        sys.exit() if event.keysym == 'Escape' else None


root = tk.Tk()
window = tk.Canvas(width=398, height=498, bg='#333')
window.pack()
matrix = Matrix()
matrix.motion()
root.bind('<Key>', matrix.binds)
root.mainloop()
