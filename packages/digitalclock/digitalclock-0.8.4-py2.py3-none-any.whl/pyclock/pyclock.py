""" PyClock class """
# Copyright 2018 @johncharlie
#
# Licensed under the GNU General Public License v3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import Tkinter as tk
import datetime

# 7 segments are ordered clockwise from top left, with crossbar last.
# The coordinates of each segment are (x_0, y_0, x_1, y_1)
SEGMENT_OFFSET = (
    (0, 0, 1, 0),  # top
    (1, 0, 1, 1),  # upper right
    (1, 1, 1, 2),  # lower right
    (0, 2, 1, 2),  # bottom
    (0, 1, 0, 2),  # lower left
    (0, 0, 0, 1),  # upper left
    (0, 1, 1, 1),  # middle
)

# The 7 segments according to each number representation
SEGMENT_DIGITS = (
    (1, 1, 1, 1, 1, 1, 0),  # 0
    (0, 1, 1, 0, 0, 0, 0),  # 1
    (1, 1, 0, 1, 1, 0, 1),  # 2
    (1, 1, 1, 1, 0, 0, 1),  # 3
    (0, 1, 1, 0, 0, 1, 1),  # 4
    (1, 0, 1, 1, 0, 1, 1),  # 5
    (1, 0, 1, 1, 1, 1, 1),  # 6
    (1, 1, 1, 0, 0, 0, 0),  # 7
    (1, 1, 1, 1, 1, 1, 1),  # 8
    (1, 1, 1, 1, 0, 1, 1),  # 9
)


class Digit():
    ''' Class to represent each seven segment display digit '''

    def __init__(self, canvas, x_offset=10, y_offset=10, length=70, width=12):
        self.canvas = canvas
        self.segs = []
        for x_0, y_0, x_1, y_1 in SEGMENT_OFFSET:
            self.segs.append(canvas.create_line(
                x_offset + x_0*length, y_offset + y_0*length,
                x_offset + x_1*length, y_offset + y_1*length,
                width=width, state='hidden', fill="#1f1"))
        circle_size = 10

        self.canvas.create_oval(length*3 - length/10, length,
                                length*3+circle_size - length/10,
                                length+circle_size, outline="#1f1",
                                fill="#000", width=2)
        self.canvas.create_oval(length*6 - length/10, length,
                                length*6+circle_size - length/10,
                                length+circle_size, outline="#1f1",
                                fill="#000", width=2)

    def show(self, num):
        ''' Show seven segment number in canvas '''
        for iid, is_on in zip(self.segs, SEGMENT_DIGITS[num]):
            self.canvas.itemconfigure(
                iid, state='normal' if is_on else 'hidden')

class PyClock():
    """ Main class """
    def __init__(self):
        self.root = tk.Tk()
        self.offset = 70
        screen = tk.Canvas(self.root, width=self.offset*9,
                           height=self.offset*2+self.offset/5,
                           background="#000")
        screen.grid()
        self.hour_tens = Digit(screen)
        self.hour_unit = Digit(screen, self.offset + 40)

        self.min_tens = Digit(screen, self.offset*3 + 20)
        self.min_unit = Digit(screen, self.offset*4 + 40)

        self.sec_tens = Digit(screen, self.offset*6 + 20)
        self.sec_unit = Digit(screen, self.offset*7 + 40)

        self.prev_time = None
        self.run()

    def update(self):
        """ Update the time in the clock """
        time_now = datetime.datetime.now()

        if self.prev_time != time_now:
            self.hour_tens.show(time_now.hour/10)
            self.hour_unit.show(time_now.hour%10)
            self.min_tens.show(time_now.minute/10)
            self.min_unit.show(time_now.minute%10)
            self.sec_tens.show(time_now.second/10)
            self.sec_unit.show(time_now.second%10)
            self.prev_time = time_now
            self.root.after(100, self.update)

    def run(self):
        """ Execute the clock update every x time"""
        self.root.after(100, self.update)
        self.root.mainloop()
