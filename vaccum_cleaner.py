import numpy as np
from time import sleep
import random

class VacuumCleaner:
    def __init__(self):
        self.position = [2,2]
        self.environ = np.random.choice([True,False],size=(8,8))
        self.performance = 0

    # SENSOR
    def scan_dirty_regions(self):
        curr_pos = self.position
        environment = self.environ

        dirty = [
                [False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False]
                ]

        for i in range(-3, 3):
            for j in range(-3, 3):
                x = curr_pos[0] + i
                y = curr_pos[1] + j

                if x >= 0 and x < 8 and y >= 0 and y < 8:
                    dirty[i+3][j+3] = environment[x][y]

        return dirty

    # ACTUATOR
    def move(self,dir_vec):
        new_x = self.position[0] + dir_vec[0]
        new_y = self.position[1] + dir_vec[1]

        if new_x < 0 or new_x > 7 or new_y > 7 or new_y < 0:
            print("At edge")
            return

        self.position = [ new_x, new_y ]

        if dir_vec == [0,0]:
            print("Staying")
        else:
            print("Moving to", self.position)

    def clean(self):
        # SENSOR
        locations = self.scan_dirty_regions()
        self.performance += len(locations) / 25

        # AGENT - Chose dirty locations
        dirty = []
        for i in range(len(locations)):
            for j in range(7):
                if self.environ[i][j] == True:
                    dirty.append([i,j])

        if len(dirty) == 0:
            print("No dirt found near cleaner")
            return [0,0]

        loc = random.choice(dirty)

        move = [ loc[0] - 2, loc[1] - 2 ]

        self.move(move)

        new_pos = self.position
        if self.environ[ new_pos[0] ][ new_pos[1] ]:
            print("Cleaning: ", new_pos)
            self.environ[ new_pos[0] ][ new_pos[1] ] = False
            self.performance += len(locations)*0.4;  # TODO: perf += dirt_found/total_boxes

            for i in range(8):
                for j in range(8):
                    if self.environ[i][j]:
                        print("+", end=" ")
                    else:
                        print(" ", end=" ")
                print()
        else:
            print("Already Clean")

vacuum_cleaner = VacuumCleaner()
while True:
    vacuum_cleaner.clean()
    sleep(1)

