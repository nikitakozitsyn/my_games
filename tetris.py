import random as rd
import sys
import tkinter as tk


class Figure:
    FIGURES = [[None, (2, 2), (22, 2), (22, 22), (2, 22), (2, 2), '#800000'],  # O
               [(False, True), (2, 2), (2, 22), (2, 42), (2, 62), (2, 42), '#800080'],  # I
               [(False, True), (2, 22), (22, 22), (22, 2), (42, 2), (22, 22), '#006400'],  # S
               [(False, True), (2, 2), (22, 2), (22, 22), (42, 22), (22, 22), '#7CFC00'],  # Z
               [(True, True), (2, 2), (2, 22), (2, 42), (22, 42), (2, 22), '#0FF'],  # L
               [(True, True), (22, 2), (22, 22), (22, 42), (2, 42), (22, 22), '#00008B'],  # J
               [(True, True), (2, 2), (22, 2), (22, 22), (42, 2), (22, 2), '#FF4500']]  # T

    POINTS = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def __init__(self):
        self.state = None
        self.counter = 0
        self.x = None
        self.flags = {'Left': True, 'Right': True, 'Down': True}
        self.score = 0, 0
        self.pause = False
        self.table = []
        self.figure = rd.choice(self.FIGURES)
        self.figure = [self.figure[0]] + [(x + 80, y) for x, y in self.figure[1:-1]] + [self.figure[-1]]
        self.next = rd.choice(self.FIGURES)
        self.obj = [window.create_rectangle(x + 200, y + 200, x + 220, y + 220, fill=self.next[-1]) for x, y in
                    self.next[1:-2]]
        self.heap = {(i, j) for i in range(2, 198, 20) for j in range(2, 398, 20)}
        self.center = self.figure[-2]
        self.color = self.figure[-1]
        self.object = [window.create_rectangle(x, y, x + 20, y + 20, fill=self.color) for x, y in self.figure[1:-2]]
        self.speed = 400
        self.motion()

    def shift(self):
        count = 0
        for k in range(2, 398, 20):
            if all((i, k) not in self.heap for i in range(2, 198, 20)):
                [window.delete(cell) for cell in self.table if window.coords(cell) and window.coords(cell)[1] == k]
                [window.move(cell, 0, 20) for cell in self.table if window.coords(cell) and window.coords(cell)[1] < k]
                tmp = {(i[0], i[1] + 20 * (i[1] < k)) for i in self.heap} | {(i, 2) for i in range(2, 198, 20)}
                self.heap, count, self.speed = tmp, count + 1, self.speed - 4 if self.speed > 300 else self.speed - 2
        self.score = self.score[0] + self.POINTS[count], self.score[1] + count
        score.config(text=f'SCORE:\n{self.score[0]}\n\nLINES:\n{self.score[1]}')

    def binds(self, event):
        if event.keysym in ('Left', 'Right', 'Down') and self.flags[event.keysym] and not self.pause:
            self.counter = 0
            self.move(event.keysym.lower())
        elif event.keysym == 'Up' and not self.pause:
            tmp = self.up()
            if tmp:
                self.center, self.figure = (tmp[-2], tmp) if set(tmp[1:-2]) <= self.heap else (self.center, self.figure)
                self.draw()
        elif event.keysym == 'Return':
            if self.pause:
                self.pause = False
                self.motion()
            else:
                root.after_cancel(self.state)
                self.pause = True

    def move(self, string):
        tmp = eval(f'self.{string}()')
        if tmp:
            self.center, self.figure = (tmp[-2], tmp) if set(tmp[1:-2]) <= self.heap else (self.center, self.figure)
            self.draw()
            self.flags[string.title()] = False
            self.counter += 1
            self.x = root.after(150 if self.counter == 1 else 30, lambda: self.move(string))

    def stop(self, event):
        if event.keysym in ('Left', 'Right', 'Down') and not self.pause:
            self.flags[event.keysym] = True
            root.after_cancel(self.x) if self.x else None

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
        self.state = root.after(self.speed, self.motion)


root = tk.Tk()
s = tk.Label(bg='#333')
s.pack()
window = tk.Canvas(s, width=301, height=401, bg='#333')
window.grid(row=0, column=0)
window.create_line(203, 0, 203, 404, fill='#FFF')
score = tk.Label(s, height=20, width=8, bg='#333', font='Arial 12 bold', text='SCORE:\n0\n\nLINES:\n0')
score.grid(row=0, column=1)
f = Figure()
root.bind('<KeyPress>', f.binds)
root.bind('<KeyRelease>', f.stop)

root.bind('<Escape>', lambda event: sys.exit())
root.mainloop()
