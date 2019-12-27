# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 21:26:21 2019

@author: PaulJ
"""


class room(object):
    def __init__(self,
                 # location,  # [y, x] where [0, 0] is upper left square
                 size=None,
                 doors=None,  # [N,E,S,W] list of doors with values
                              # of next room, 0=no room, -1=start, -2 = exit
                 windows=None,  # [N,E,S,W] list of 1 if window, 0 if no window
                 # wall_decoration,
                 # light_level=1,
                 visible=True,
                 ):
        # self.location = location
        self.size = size
        self.size = (list(self.size) if isinstance(self.size, tuple)
                     else self.size)
        if (self.size is None or (not isinstance(self.size, list))
            or len(self.size) != 2
                or (not all(isinstance(x, int) for x in self.size))):
            self.size = [10, 10]
        self.width = self.size[0]
        self.wall_width = int(self.width * 0.4)
        self.door_window_width = self.width - (self.wall_width * 2)
        self.length = self.size[1]
        self.wall_length = int(self.length * 0.4)
        self.door_window_length = self.length - (self.wall_length * 2)
        # self.map = []
        self.doors = doors
        self.windows = windows
        # self.wall_decoration = wall_decoration
        # self.light_level = light_level
        self.visible = visible
        self.door_char = ' '
        self.window_char = '░'

        self.doors = (list(self.doors) if isinstance(self.doors, tuple)
                      else self.doors)
        self.windows = (list(self.windows) if isinstance(self.windows, tuple)
                        else self.windows)

        if (self.doors is None or (not isinstance(self.doors, list))
            or len(self.doors) != 4
            or (not all(isinstance(x, int) for x in self.doors))
                or (not all((x >= 0 and x <= 3) for x in self.doors))):
            self.doors = [0, 0, 0, 0]

        if (self.windows is None or (not isinstance(self.windows, list))
            or len(self.windows) != 4
            or (not all(isinstance(x, int) for x in self.windows))
                or (not all((x >= 0 and x <= 3) for x in self.windows))):
            self.windows = [0, 0, 0, 0]

    def room_map(self):
        temp_map = []

        if not self.visible:
            for a_v_block in range(self.length):
                temp_map.append(' ' * self.width)
            return temp_map

        # Top/North Wall
        mid_wall_char = (self.door_char if self.doors[0] else
                         (self.window_char if self.windows[0] else '-'))
        temp_map.append('┌' + '-' * (self.wall_width - 1)
                        + mid_wall_char * self.door_window_width
                        + '-' * (self.wall_width - 1) + '┐')

        # Side Walls above Door or Window
        for wall_piece in range(self.wall_length - 1):
            temp_map.append('|' + ' ' * (self.wall_width * 2
                                         + self.door_window_width - 2) + '|')

        # Side Wall where door or window may be
        for wall_piece in range(self.door_window_length):
            temp_map.append((self.door_char if self.doors[3] else
                             self.window_char if self.windows[3] else '|')
                            + ' ' * (self.wall_width * 2
                                     + self.door_window_width - 2)
                            + (self.door_char if self.doors[1] else
                               self.window_char if self.windows[1] else '|'))

        # Side Wall below Door or Window
        for wall_piece in range(self.wall_length - 1):
            temp_map.append('|' + ' ' * (self.wall_width * 2
                                         + self.door_window_width - 2) + '|')

        # Bottom/South Wall
        mid_wall_char = (self.door_char if self.doors[2] else
                         (self.window_char if self.windows[2] else '-'))
        temp_map.append('└' + '-' * (self.wall_width - 1)
                        + mid_wall_char * self.door_window_width
                        + '-' * (self.wall_width - 1) + '┘')
        return temp_map

    def __str__(self):
        return('\n'.join(self.room_map()))


if __name__ == '__main__':
    # LOCATION = (0, 0)
    SIZE = (10, 10)
    DOORS = (1, 0, 0, 1)
    WINDOWS = (0, 1, 1, 0)
    # VISIBLE1 = True
    VISIBLE2 = True
    VISIBLE3 = False

    new_room1 = room(  # LOCATION,
                     SIZE,
                     DOORS,
                     WINDOWS)

    new_room2 = room()
    new_room3 = room(visible=VISIBLE3)

    print(new_room1)
    print('------')
    print(new_room2)
    print('------')
    print(new_room3)
