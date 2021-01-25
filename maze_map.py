# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 23:12:05 2019

@author: PaulJ
"""

from math import ceil
from random import random, seed
import numpy as np
from rooms import room


class maze_map(object):
    def __init__(self,
                 no_rooms_wide=2,
                 no_rooms_long=2,
                 room_width=10,
                 room_length=10,
                 init_room_visibility=True,
                 ):
        self.no_rooms_wide = no_rooms_wide
        self.no_rooms_long = no_rooms_long
        self.room_width = room_width
        self.room_length = room_length

        temp_room = room()
        self.no_door = temp_room.no_door  # value used for no door

        self.rooms = []  # rooms is list of room objects
        for room_no in range(self.no_rooms_wide * self.no_rooms_long):
            self.rooms.append(room(size=(self.room_length, self.room_width),
                                   doors=(self.no_door,
                                          self.no_door,
                                          self.no_door,
                                          self.no_door),  # Doors, none
                                   windows=(0, 0, 0, 0),  # Windows, none
                                   visible=init_room_visibility,
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
                        ease_limit=0.5,   # Shortest path must be this ratio
                                           # between shortest possible path 
                                           # and longest possible path
                        diff_limit=0.95,   # Shortest path max ratio to max
                                           # for this maze size
                        min_length_limit=0.1,
                        max_length_limit=1,
                        max_tries=100
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

        self.entrance = the_entrance

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

        self.exit = the_exit

        self.tries = 0  # Use counter until validate so doors get gen. at least once

        while (not self.validate(ease_limit=ease_limit,
                                 difficulty_limit=diff_limit,
                                 min_length_limit=min_length_limit,
                                 max_length_limit=max_length_limit)
               and self.tries < max_tries):
            self.tries += 1
            # Top & Bottom Outside Horiz. Wall Windows
            for horiz_room in range(self.no_rooms_wide):
                if (random() <= window_freq  # Top Wall
                        and self.rooms[self.room_map[
                            0, horiz_room]].doors[0] == self.no_door):
                    self.rooms[self.room_map[0, horiz_room]].windows[0] = 1
                else:
                    self.rooms[self.room_map[0, horiz_room]].windows[0] = 0
                if (random() <= window_freq  # Bottom Wall
                        and self.rooms[
                            self.room_map[
                                self.no_rooms_long - 1,
                                horiz_room]].doors[2] == self.no_door):
                    self.rooms[self.room_map[self.no_rooms_long - 1,
                                             horiz_room]].windows[2] = 1
                else:
                    self.rooms[self.room_map[self.no_rooms_long - 1,
                                             horiz_room]].windows[2] = 0

            # Left & Right Outside Horiz. Wall Windows
            for vert_room in range(self.no_rooms_long):
                if (random() <= window_freq  # Left Wall
                        and self.rooms[
                        self.room_map[vert_room, 0]].doors[3] == self.no_door):
                    self.rooms[self.room_map[vert_room, 0]].windows[3] = 1
                else:
                    self.rooms[self.room_map[vert_room, 0]].windows[3] = 0
                if (random() <= window_freq  # Right Wall
                        and self.rooms[self.room_map[
                        vert_room, self.no_rooms_wide - 1]].doors[1] == (
                            self.no_door)):
                    self.rooms[self.room_map[
                        vert_room, self.no_rooms_wide - 1]].windows[1] = 1
                else:
                    self.rooms[self.room_map[
                        vert_room, self.no_rooms_wide - 1]].windows[1] = 0

            # Inside Doors
            for vert_room in range(self.no_rooms_long - 1):
                for horiz_room in range(self.no_rooms_wide):
                    # Horiz. Doors
                    if random() <= door_freq:
                        self.rooms[
                            self.room_map[vert_room][horiz_room]].doors[2] = (
                            self.room_map[vert_room + 1][horiz_room])
                        self.rooms[
                            self.room_map[vert_room + 1][
                                    horiz_room]].doors[0] = (
                                    self.room_map[vert_room][horiz_room])
                    else:
                        self.rooms[
                            self.room_map[vert_room][horiz_room]].doors[2] = (
                                self.no_door)
                        self.rooms[self.room_map[vert_room + 1][
                            horiz_room]].doors[0] = self.no_door
                    # Vert. Doors
                    if horiz_room < (self.no_rooms_wide - 1):
                        if random() <= door_freq:
                            self.rooms[
                                self.room_map[vert_room][
                                    horiz_room]].doors[1] = (
                                self.room_map[vert_room][horiz_room + 1])
                            self.rooms[
                                self.room_map[vert_room][
                                    horiz_room + 1]].doors[3] = (
                                    self.room_map[vert_room][horiz_room])
                        else:
                            self.rooms[
                                self.room_map[vert_room][
                                    horiz_room]].doors[1] = self.no_door
                            self.rooms[
                                self.room_map[vert_room][
                                    horiz_room + 1]].doors[3] = self.no_door
        if self.tries < max_tries:
            print('It took', self.tries, 'tries to try to get a good maze')
        else:
            print(self.tries, 'tries were made but no solution was found that met'
                  + ' the criteria')

    def validate(self,
                 ease_limit=0,
                 difficulty_limit=1,
                 min_length_limit=0,
                 max_length_limit=1):
        shortest_path_length = None
        dead_ends = 0
        solution_paths = []
        # print('self.entrance:', self.entrance)
        # print('self.entrance[0]:', self.entrance[0], type(self.entrance[0]))
        active_paths = [[self.room_map[self.entrance[0], self.entrance[1]]]]

        while active_paths:
            new_active_paths = []
            # print('active_paths:', active_paths)
            for a_path in active_paths:
                curr_room = a_path[-1]
                try:
                    prev_room = a_path[-2]
                except IndexError:
                    prev_room = None
                new_directions = [x for x in self.rooms[curr_room].doors
                                  if (x not in a_path
                                      and x not in [self.no_door, -1]
                                      and x != prev_room)]
                if not new_directions:
                    dead_ends += 1
                for new_dir in new_directions:
                    if new_dir == -2:  # Found an exit
                        solution_paths.append(a_path)
                        break  # Ignore remainder of doors, if any
                    if new_dir in a_path:  # Yea, we made a loop
                        continue
                    new_path = a_path + [new_dir]
                    new_active_paths.append(new_path)
            active_paths = new_active_paths.copy()
        # print('Solution Paths:', solution_paths)

        shortest_possible_path_length = (
            abs(self.entrance[0] - self.exit[0])
            + abs(self.entrance[1] - self.exit[1]))
        longest_possible_path_length = (self.no_rooms_wide
                                        * self.no_rooms_long - 1)

        min_path_length_allowed = ceil(ease_limit * (
            longest_possible_path_length - shortest_possible_path_length)
            + shortest_possible_path_length)
        # print('min_path_length_allowed:', min_path_length_allowed)

        # solution_paths = [x for x in solution_paths
        #                   if len(x) >= min_path_length_allowed]
        # print('Solution Paths:\n', solution_paths)

        path_lengths = [len(x) for x in solution_paths]
        # print('path_lengths:', path_lengths)
        if not path_lengths:
            return False
        shortest_path_number = path_lengths.index(min(path_lengths))
        solution_path = solution_paths[shortest_path_number]
        shortest_path_length = len(solution_path)

        length_rating = (
            (shortest_path_length - shortest_possible_path_length)
            / (longest_possible_path_length - shortest_possible_path_length))

        difficulty_rating = dead_ends / shortest_path_length

        # print('shortest_path_length:', shortest_path_length,
        #       '\nshortest_possible_path_length:', shortest_possible_path_length,
        #       '\nlongest_possible_path_length:', longest_possible_path_length)
        # print('ease_limit:', ease_limit, '\ndifficulty_rating:',
        #       difficulty_rating, '\ndifficulty_limit:', difficulty_limit)

        return ((ease_limit <= difficulty_rating <= difficulty_limit)
                and (min_length_limit <= length_rating <= max_length_limit))

    def maze_map(self):
        temp_map = []
        for v_room in range(self.no_rooms_long):
            temp_room_map = [None] * self.no_rooms_wide
            for h_room in range(self.no_rooms_wide):
                    temp_room_map[h_room] = (
                        self.rooms[self.room_map[v_room, h_room]].room_map())

            for v_block in range(len(temp_room_map[0])):
                if (v_room != self.no_rooms_long - 1
                        and v_block == len(temp_room_map[0]) - 1):
                    continue
                row_str = ''
                for h_room in range(self.no_rooms_wide):
                    if h_room != self.no_rooms_wide -1:
                        row_str += temp_room_map[h_room][v_block][:-1]
                    else:
                        row_str += temp_room_map[h_room][v_block]
                temp_map.append(row_str)
        return temp_map

    def __str__(self):
        return('\n'.join(self.maze_map()))



if __name__ == '__main__':
    from time import time
    start_time = time()
    seed(155)
    NO_ROOMS_WIDE = 9
    NO_ROOMS_LONG = 9
    ROOM_WIDTH = 5
    ROOM_LENGTH = 5

    # new_maze_map1 = maze_map()

    new_maze_map2 = maze_map(no_rooms_wide=NO_ROOMS_WIDE,
                             no_rooms_long=NO_ROOMS_LONG,
                             room_width=ROOM_WIDTH,
                             room_length=ROOM_LENGTH,
                             )

    """
    new_maze_map3 = maze_map(no_rooms_wide=NO_ROOMS_WIDE,
                             no_rooms_long=NO_ROOMS_LONG,
                             room_width=ROOM_WIDTH,
                             room_length=ROOM_LENGTH,
                             init_room_visibility=False)
    """

    # print("new_maze_map1:\n", new_maze_map1)

    # print("new_maze_map2:\n", new_maze_map2)

    new_maze_map2.generate_random(# the_entrance=None,
                                  # the_exit=None,
                                  door_freq=0.45,
                                  window_freq=0.25,
                                  ease_limit=0.6,
                                  diff_limit=1,
                                  min_length_limit=.25,
                                  max_length_limit=1,
                                  max_tries=100000)
    print("new_maze_map2:\n", new_maze_map2)

    # new_maze_map3.generate_random()
    # print("new_maze_map3:\n", new_maze_map3)

    elapsed_time = time() - start_time
    time_per_map = elapsed_time / new_maze_map2.tries * 1000
    time_per_map_per_room = (time_per_map /
                             (NO_ROOMS_WIDE * NO_ROOMS_LONG) * 1000)
    print('Elapsed Time:', round(elapsed_time, 2), 's')
    print('Tries:', new_maze_map2.tries)
    print('Time per map:', round(time_per_map, 2), 'ms')
    print('Time per map per room:', round(time_per_map_per_room, 2), 'µs')
