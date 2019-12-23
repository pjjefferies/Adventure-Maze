# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 21:26:21 2019

@author: PaulJ
"""


class room(object):
    def __init__(self,
                 location,
                 size,
                 doors,  # of next room, 0 = no room, -1 = start, -2 = exit
                 windows,  # 1 if window, 0 if no window
                 # wall_decoration,
                 # light_level=1,
                 ):
        self.location = location
        self.size = size
        self.width = size[0]
        self.wall_width = int(self.width * 0.4)
        self.door_window_width = self.width - (self.wall_width * 2)
        self.length = size[1]
        self.wall_length = int(self.length * 0.4)
        self.door_window_length = self.length - (self.wall_length * 2)
        self.map = []
        self.doors = doors
        self.windows = windows
        # self.wall_decoration = wall_decoration
        # self.light_level = light_level
        self.door_char = ' '
        self.window_char = '░'

        mid_wall_char = (self.door_char if self.doors[0] else
                         (self.window_char if self.windows[0] else '-'))
        self.map.append('┌' + '-' * (self.wall_width - 1)
                        + mid_wall_char * self.door_window_width
                        + '-' * (self.wall_width - 1) + '┐')
        for wall_piece in range(self.wall_length - 1):
            self.map.append('|' + ' ' * (self.wall_width * 2
                                         + self.door_window_width - 2) + '|')

        for wall_piece in range(self.door_window_length):
            self.map.append((self.door_char if self.doors[3] else
                             self.window_char if self.windows[3] else '|')
                            + ' ' * (self.wall_width * 2
                                     + self.door_window_width - 2)
                            + (self.door_char if self.doors[1] else
                               self.window_char if self.windows[1] else '|'))
        for wall_piece in range(self.wall_length - 1):
            self.map.append('|' + ' ' * (self.wall_width * 2
                                         + self.door_window_width - 2) + '|')

        mid_wall_char = (self.door_char if self.doors[2] else
                         (self.window_char if self.windows[2] else '-'))
        self.map.append('└' + '-' * (self.wall_width - 1)
                        + mid_wall_char * self.door_window_width
                        + '-' * (self.wall_width - 1) + '┘')

    def __str__(self):
        return('\n'.join(self.map))





if __name__ == '__main__':
    LOCATION = (0, 0)
    SIZE = (10, 10)
    DOORS = (1, 0, 0, 1)
    WINDOWS = (0, 1, 1, 0)

    new_room = room(LOCATION,
                    SIZE,
                    DOORS,
                    WINDOWS)

    print(new_room)

