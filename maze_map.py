# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 23:12:05 2019

@author: PaulJ
"""

from random import random
import numpy as np
from rooms import room


class maze_map(object):
    def __init__(self,
                 no_rooms_wide=2,
                 no_rooms_long=2,
                 room_width=10,
                 room_length=10,
                 ):
        self.no_rooms_wide = no_rooms_wide
        self.no_rooms_long = no_rooms_long
        self.room_width = room_width
        self.room_length = room_length

        self.rooms = []  # rooms is list of room objects
        for room_no in range(self.no_rooms_wide * self.no_rooms_long):
            self.rooms.append(room((self.room_length, self.room_width),
                                   (0, 0, 0, 0),  # Doors, none
                                   (0, 0, 0, 0),  # Windows, none
                                   ))

        self.room_map = np.empty((self.no_rooms_long, self.no_rooms_wide),
                                 dtype=int)
        for vert_room in range(self.no_rooms_long):
            for horiz_room in range(self.no_rooms_wide):
                self.room_map[vert_room, horiz_room] = (
                    vert_room * self.no_rooms_wide + horiz_room)

    def validate_outside_doors(self, outside_door):  # (row, col, direction)
        try:
            outside_door = list(outside_door)
            if len(outside_door) != 3:
                raise TypeError
            row, col, direction = [int(x) for x in outside_door]
        except (TypeError, IndexError):
            raise

        return ((row == 0 and direction == 0)
                or (col == (self.no_rooms_wide - 1) and direction == 1)
                or (row == (self.no_rooms_long - 1) and direction == 2)
                or (col == 0 and direction == 3))

    def generate_random(self,
                        the_entrance=None,
                        the_exit=None,
                        door_freq=0.33,    # 33% of internal walls have doors
                        window_freq=0.25,  # 25% of external walls windows
                        ease_limit=1.25,   # Shortest path must be this ratio
                                           # of shortest possible path for this
                                           # maze size
                        diff_limit=0.95,   # Shortest path max ratio to max
                                           # for this maze size
                        ):

        # Verify good Entrance Set
        try:
            if not self.validate_outside_doors(the_entrance):
                the_entrance = [self.no_rooms_long - 1, 0, 2]  # (y, x, dir.)
        except (TypeError, IndexError):
            the_entrance = [self.no_rooms_long - 1, 0, 2]  # (y, x, dir.)

        # Identify Entrance Door in Room
        try:
            self.rooms[
                self.room_map[the_entrance[0],
                              the_entrance[1]]].doors[the_entrance[2]] = -1
        except IndexError:
            raise TypeError('Entrance Direction not valid: ' + the_entrance[2])

        # Verify good Exit Set
        try:
            if not self.validate_outside_doors(the_exit):
                the_exit = [0, self.no_rooms_wide - 1, 0]  # (y, x, direction)
        except (TypeError, IndexError):
            the_exit = [0, self.no_rooms_wide - 1, 0]  # (y, x, direction)

        # Identify Exit Door in Room
        try:
            self.rooms[
                self.room_map[the_exit[0],
                              the_exit[1]]].doors[the_exit[2]] = -2
        except IndexError:
            raise TypeError('Exit Direction not valid: ' + the_exit[2])


        n = 1  # Use counter until validate so doors get gen. at least once


        while (not self.validate(ease_limit=ease_limit, diff_limit=diff_limit)
               or n == 1):
            n += 1
            # Top & Bottom Outside Horiz. Wall Windows
            for horiz_room in range(self.no_rooms_wide):
                if (random() >= window_freq  # Top Wall
                        and self.rooms[self.room_map[
                            0, horiz_room]].doors[0] == 0):
                    self.rooms[self.room_map[0, horiz_room]].windows[0] = 1
                else:
                    self.rooms[self.room_map[0, horiz_room]].windows[0] = 0
                if (random() >= window_freq  # Bottom Wall
                        and self.rooms[
                            self.room_map[self.no_rooms_long - 1,
                                          horiz_room]].doors[2] == 0):
                    self.rooms[self.room_map[self.no_rooms_long - 1,
                                             horiz_room]].windows[2] = 1
                else:
                    self.rooms[self.room_map[self.no_rooms_long - 1,
                                             horiz_room]].windows[2] = 0

            # Left & Right Outside Horiz. Wall Windows
            for vert_room in range(self.no_rooms_long):
                if (random() >= window_freq  # Left Wall
                        and self.rooms[
                        self.room_map[vert_room, 0]].doors[3] == 0):
                    self.rooms[self.room_map[vert_room, 0]].windows[3] = 1
                else:
                    self.rooms[self.room_map[vert_room, 0]].windows[3] = 0
                if (random() >= window_freq  # Right Wall
                        and self.rooms[self.room_map[
                        vert_room, self.no_rooms_wide - 1]].doors[1] == 0):
                    self.rooms[self.room_map[
                        vert_room, self.no_rooms_wide - 1]].windows[1] = 1
                else:
                    self.rooms[self.room_map[
                        vert_room, self.no_rooms_wide - 1]].windows[1] = 0

            # Inside Doors
            for vert_room in range(self.no_rooms_long - 1):
                for horiz_room in range(self.no_rooms_wide):
                    # Horiz. Doors
                    if random() >= door_freq:
                        self.rooms[
                            self.room_map[vert_room][horiz_room]].doors[2] = (
                            self.room_map[vert_room + 1][horiz_room])
                        self.rooms[
                            self.room_map[vert_room + 1][
                                    horiz_room]].doors[0] = (
                                    self.room_map[vert_room][horiz_room])
                    else:
                        self.rooms[
                            self.room_map[vert_room][horiz_room]].doors[2] = 0
                        self.rooms[self.room_map[vert_room + 1][
                            horiz_room]].doors[0] = 0
                    # Vert. Doors
                    if horiz_room < (self.no_rooms_wide - 1):
                        if random() >= door_freq:
                            self.rooms[
                                self.room_map[vert_room][
                                    horiz_room]].doors[1] = (
                                self.room_map[vert_room][horiz_room + 1])
                            self.rooms[
                                self.room_map[vert_room][
                                    horiz_room + 1]].doors[2] = (
                                    self.room_map[vert_room][horiz_room])
                        else:
                            self.rooms[
                                self.room_map[vert_room][
                                    horiz_room]].doors[1] = 0
                            self.rooms[
                                self.room_map[vert_room][
                                    horiz_room + 1]].doors[2] = 0

    def validate(self,
                 ease_limit=0,
                 diff_limit=1):
        return True

    def maze_map(self):
        temp_map = []
        for v_room in range(self.no_rooms_long):
            temp_room_map = [None] * self.no_rooms_wide
            for h_room in range(self.no_rooms_wide):
                temp_room_map[h_room] = (
                    self.rooms[self.room_map[v_room, h_room]].room_map())

            for v_block in range(len(temp_room_map[0])):
                row_str = ''
                for h_room in range(self.no_rooms_wide):
                    row_str += temp_room_map[h_room][v_block]
                temp_map.append(row_str)
        return temp_map

    def __str__(self):
        return('\n'.join(self.maze_map()))



if __name__ == '__main__':
    NO_ROOMS_WIDE = 5
    NO_ROOMS_LONG = 5
    ROOM_WIDTH = 20
    ROOM_LENGTH = 20

    new_maze_map1 = maze_map()

    new_maze_map2 = maze_map(no_rooms_wide=NO_ROOMS_WIDE,
                             no_rooms_long=NO_ROOMS_LONG,
                             room_width=ROOM_WIDTH,
                             room_length=ROOM_LENGTH,
                             )

    print("new_maze_map1:\n", new_maze_map1)

    print("new_maze_map2:\n", new_maze_map2)

    new_maze_map2.generate_random()
    print("new_maze_map2:\n", new_maze_map2)

    # print(new_room)
