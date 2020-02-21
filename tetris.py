import random as rd
import sys
import tkinter as tk


class Figure:
    FIGURES = [[None, (0, 0), (20, 0), (20, 20), (0, 20), (0, 0), 'White'],  # O
               [(False, True), (0, 0), (0, 20), (0, 40), (0, 60), (0, 40), 'Grey'],  # I
               [(False, True), (0, 20), (20, 20), (20, 0), (40, 0), (20, 20), 'Green'],  # S
               [(False, True), (0, 0), (20, 0), (20, 20), (40, 20), (20, 20), 'Yellow'],  # Z
               [(True, True), (0, 0), (0, 20), (0, 40), (20, 40), (0, 20), 'Red'],  # L
               [(True, True), (20, 0), (20, 20), (20, 40), (0, 40), (20, 20), 'Blue'],  # J
               [(True, True), (0, 0), (20, 0), (20, 20), (40, 0), (20, 0), 'Pink']]  # T

    POINTS = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def __init__(self):
        self.score = 0, 0
        self.pause = False
        self.table = []
        self.figure = rd.choice(self.FIGURES)
        self.figure = [self.figure[0]] + [(x + 80, y) for x, y in self.figure[1:-1]] + [self.figure[-1]]
        self.next = rd.choice(self.FIGURES)
        self.obj = [window.create_rectangle(x + 200, y + 200, x + 220, y + 220, fill=self.next[-1]) for x, y in
                    self.next[1:-2]]
        self.heap = {(i, j) for i in range(0, 198, 20) for j in range(0, 398, 20)}
        self.center = self.figure[-2]
        self.color = self.figure[-1]
        self.object = [window.create_rectangle(x, y, x + 20, y + 20, fill=self.color) for x, y in self.figure[1:-2]]
        self.speed = 400
        self.motion()

    def shift(self):
        count = 0
        for k in range(0, 398, 20):
            if all((i, k) not in self.heap for i in range(0, 198, 20)):
                [window.delete(cell) for cell in self.table if window.coords(cell) and window.coords(cell)[1] == k]
                [window.move(cell, 0, 20) for cell in self.table if window.coords(cell) and window.coords(cell)[1] < k]
                tmp = {(i[0], i[1] + 20 * (i[1] < k)) for i in self.heap} | {(i, 0) for i in range(0, 198, 20)}
                self.heap, count, self.speed = tmp, count + 1, self.speed - 4 if self.speed > 300 else self.speed - 2
        self.score = self.score[0] + self.POINTS[count], self.score[1] + count
        score.config(text=f'SCORE:\n{self.score[0]}\n\nLINES:\n{self.score[1]}')

    def binds(self, event):
        tmp = eval(f'self.{event.keysym.lower()}()') if event.keysym in ('Left', 'Right', 'Up', 'Down') else None
        if tmp:
            self.center, self.figure = (tmp[-2], tmp) if set(tmp[1:-2]) <= self.heap else (self.center, self.figure)
            self.draw()
        if event.keysym == 'Return':
            if self.pause:
                self.pause = False
                self.motion()
            else:
                self.pause = True

    def draw(self):
        for o in self.object:
            window.delete(o)
        self.object = [window.create_rectangle(x, y, x + 20, y + 20, fill=self.color) for x, y in self.figure[1:-2]]
        for o in self.obj:
            window.delete(o)
        self.obj = [window.create_rectangle(x + 220, y + 60, x + 240, y + 80, fill=self.next[-1]) for x, y in
                    self.next[1:-2]]

    def renew(self):
        self.figure = self.next
        self.next = rd.choice(self.FIGURES)[:]
        self.center = self.figure[-2]
        self.color = self.figure[-1]
        None if set(self.figure[1:-2]) <= self.heap else sys.exit()

    def left(self):
        tmp_figure = self.figure[:]
        for i in range(len(self.object)):
            tmp_figure[i + 1] = tmp_figure[i + 1][0] - 20, tmp_figure[i + 1][1]
        tmp_figure[-2] = tmp_figure[-2][0] - 20, tmp_figure[-2][1]
        return tmp_figure

    def right(self):
        tmp_figure = self.figure[:]
        for i in range(len(self.object)):
            tmp_figure[i + 1] = tmp_figure[i + 1][0] + 20, tmp_figure[i + 1][1]
        tmp_figure[-2] = tmp_figure[-2][0] + 20, tmp_figure[-2][1]
        return tmp_figure

    def down(self):
        tmp_figure = self.figure[:]
        for i in range(len(self.object)):
            tmp_figure[i + 1] = tmp_figure[i + 1][0], tmp_figure[i + 1][1] + 20
        tmp_figure[-2] = tmp_figure[-2][0], tmp_figure[-2][1] + 20
        return tmp_figure

    def up(self):
        if self.figure[0]:
            tmp_figure = self.figure[:]
            center = tmp_figure[-2]
            for i in range(len(self.object)):
                if tmp_figure[0][0] or tmp_figure[0][1]:
                    tmp_figure[i + 1] = center[0] - tmp_figure[i + 1][1] + center[1], center[1] - center[0] + \
                                        tmp_figure[i + 1][0]
                else:
                    tmp_figure[i + 1] = center[0] + tmp_figure[i + 1][1] - center[1], center[1] + center[0] - \
                                        tmp_figure[i + 1][0]
            tmp_figure[0] = tmp_figure[0][0], not (tmp_figure[0][0] ^ tmp_figure[0][1])
            return tmp_figure

    def motion(self):
        tmp = self.down()
        if set(tmp[1:-2]) <= self.heap:
            self.center, self.figure = tmp[-2], tmp
        else:
            self.heap -= set(self.figure[1:-2])
            self.table += [window.create_rectangle(x, y, x + 20, y + 20, fill=self.color) for x, y in self.figure[1:-2]]
            self.shift()
            self.renew()
        self.draw()
        None if self.pause else root.after(self.speed, self.motion)


root = tk.Tk()
s=tk.Label(bg='#333')
s.pack()
window = tk.Canvas(s, width=298, height=398, bg='#333')
window.grid(row=0, column=0)
window.create_line(200, 0, 200, 400, fill='#FFF')
score = tk.Label(s, height=20, width=8, bg='#333', font='Arial 12 bold')
score.grid(row=0, column=1)
f = Figure()
root.bind('<Key>', f.binds)

root.bind('<Escape>', lambda event: sys.exit())
root.mainloop()
