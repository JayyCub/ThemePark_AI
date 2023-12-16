# This is a sample Python script.
import argparse
import math
import sys
import time
import tkinter as tk

import numpy
import numpy as np

from Park import Park
from Robot import Robot


class MapGUI:
    def __init__(self, root, map_data):
        self.root = root
        self.root.title("Map GUI")
        self.labels = []
        self.map_data = map_data

        for i, row in enumerate(map_data):
            label_row = []
            for j, cell in enumerate(row):
                cell_value = self.map_data[i][j]
                color = "green"
                text = cell_value
                if cell_value == '_':
                    color = "#363636"
                    text = ""
                elif cell_value == 'O':
                    color = "white"
                    text = ""
                elif cell_value == 'E':
                    color = "teal"
                label = tk.Label(root, width=2, height=1, text=text, bg=color, relief="solid", borderwidth=1)
                label.grid(row=i, column=j)
                label_row.append(label)
            self.labels.append(label_row)

    def change_cell_color(self, row, col, color):
        self.labels[row][col].config(bg=color)
        self.update_gui()

    def reset_cell(self, i, j):
        cell_value = self.map_data[i][j]
        text = cell_value
        if cell_value == '_':
            color = "black"
            text = ""
        elif cell_value == 'O':
            color = "white"
            text = ""
        elif cell_value == 'E':
            color = "teal"
        else:
            color = "green"
        self.labels[i][j].config(text=text, bg=color)
        self.update_gui()

    def val_gui_update(self, vals):
        np_array = numpy.array(vals)
        max_val = np.max(np_array)
        for i, row in enumerate(vals):
            for j, cell in enumerate(row):
                cell_value = round(int(vals[i][j]), 0)
                if cell_value != 0:
                    percent = cell_value / max_val
                    col = int(255 * percent)
                    color = '#%02x%02x%02x' % (255 - col, 255 - col, 255)
                    self.labels[i][j].config(text=cell_value, bg=color)
        self.update_gui()

    def update_gui(self):
        self.root.update()


def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Park Optimizer")
    parser.add_argument('park_file', metavar='FILENAME', type=str, help="File of park")
    parser.add_argument('ride_file', metavar='FILENAME', type=str, help="File of rides")
    parser.add_argument("-o", '--option',
                        help="Option type one",
                        default='default')
    options_return = parser.parse_args(args)
    return options_return


def mainFunc(gui, park, val_gui):
    # print("--\t--\tDAY START\t--\t--")
    # print("WELCOME TO " + my_park.name.upper() + '!')
    # my_park.display_info()

    # for i in range(10):
    #     my_park.increment_waits()
    #     print("--\t--\tTIME\t--\t--")
    #     my_park.display_times()
    #     time.sleep(1)

    # gui.change_cell_color(5, 5, "blue")
    # time.sleep(5)
    # input("Press a key")
    # gui.reset_cell(5, 5)
    # gui.change_cell_color(5, 4, "blue")
    # park.display_times()
    robo = Robot(gui, park, val_gui)


options = getOptions()

park_file = open(options.park_file, 'r')
my_park = Park(name=sys.argv[1].strip(".txt"), park_id=0, lod=8*60)
lines = park_file.readlines()

# Initialize the 2D array with empty values
width = len(lines[0])-1
height = len(lines)
park_array = [['' for _ in range(width)] for _ in range(height)]

# Fill in the 2D array with characters from the text
for i in range(height):
    for j in range(width):
        park_array[i][j] = lines[i][j]

# print(park_array)
my_park.add_map(park_array)
# print(my_park.map[21][9])

rides_file = open(options.ride_file, 'r')
rides = rides_file.readlines()

for ride in rides:
    my_park.add_ride(ride.strip())


root1 = tk.Tk()
root2 = tk.Tk()
root1.geometry('440x440')
root2.geometry('440x440+500+0')
map_gui = MapGUI(root1, park_array)
v_s_gui = MapGUI(root2, park_array)
root1.after(500, mainFunc, map_gui, my_park, v_s_gui)
root1.mainloop()
root2.mainloop()
