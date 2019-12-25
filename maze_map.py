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

    """
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
        if (the_entrance is None or (not isinstance(the_entrance, list))
            or len(the_entrance) != 3
            or (not all(isinstance(x, int) for x in the_entrance))
            or the_entrance[0] < 0 or the_entrance[0] >= self.no_rooms_wide
            or the_entrance[1] < 0 or the_entrance[1] >= self.no_rooms_long
            or (the_entrance[2] == 0 and the_entrance[1] != 0)
            or (the_entrance[2] == 1 and
                the_entrance[0] != (self.no_room_wide-1))
            or (the_entrance[2] == 2 and
                the_entrance[1] != (self.no_room_long-1))
                or (the_entrance[2] == 3 and the_entrance[0] != 0)):
            the_entrance = (self.no_rooms_long - 1, 0, 0)  # (y, x, z)
            self.rooms[the_entrace[0], the_entrance[1].]
        if (the_exit is None or (not isinstance(the_exit, list))
            or len(the_exit) != 3
            or (not all(isinstance(x, int) for x in the_exit))
            or the_exit[0] < 0 or the_exit[0] >= self.no_rooms_wide
            or the_exit[1] < 0 or the_exit[1] >= self.no_rooms_long
            or (the_exit[2] == 0 and the_exit[1] != 0)
            or (the_exit[2] == 1 and the_exit[0] != (self.no_room_wide-1))
            or (the_exit[2] == 2 and the_exit[1] != (self.no_room_long-1))
                or (the_exit[2] == 3 and the_exit[0] != 0)):
            the_exit = (self.no_rooms_width - 1, 0, 0)

        # Top & Bottom Outside Horiz. Wall
        for horiz_room in range(self.no_rooms_wide):
            

        for vert_room in range(self.no_rooms_long):
            for horiz_room in range(self.no_rooms_wide):
                # Inside horiz. walls
                if (random() >= door_freq
                        and vert_room <= (self.no_rooms_long - 1)):
                    self.rooms[vert_room][horiz_room].door[2] = (
                        (vert_room + 1, horiz_room))
                    self.rooms[vert_room + 1][horiz_room].door[0] = (
                        (vert_room, horiz_room))
                # Inside vert. walls
                if (random() >= door_freq
                        and horiz_room <= (self.no_rooms_wide - 1)):
                    self.rooms[vert_room][horiz_room].door[1] = (
                        (vert_room, horiz_room + 1))
                    self.rooms[vert_room][horiz_room + 1].door[2] = (
                        (vert_room, horiz_room))
            # Left/West Wall
            # if (random() >= window_freq
            #     and self.rooms[vert_room][0].
    """


if __name__ == '__main__':
    NO_ROOMS_WIDE = 5
    NO_ROOMS_LONG = 5
    ROOM_WIDTH=20
    ROOM_LENGTH=15

    new_maze_map1 = maze_map()

    new_maze_map2 = maze_map(no_rooms_wide=NO_ROOMS_WIDE,
                             no_rooms_long=NO_ROOMS_LONG,
                             room_width=ROOM_WIDTH,
                             room_length=ROOM_LENGTH,
                             )

    # print(new_room)
