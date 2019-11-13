from tools import message, fatal
import numpy as np
import cv2
from colour_table import colour_table

class Command:

    def __init__(self, nimbus):
        # Initialize commands and global parameters
        if nimbus.debug:
            message('Initializing Nimbus commands')
        self.nimbus = nimbus
        self.screen_size = (640, 250)
        self.border_colour = 15
        self.paper_colour = 0
        self.brush_colour = 15
        self.colour_table = colour_table

    def cls(self):
        # cls
        if self.nimbus.debug:
            message('cls')
        self.nimbus.update(np.zeros(shape=[self.screen_size[1], self.screen_size[0], 3], dtype=np.uint8))
        cv2.rectangle(self.nimbus.vs.screen_data, (0,0), self.screen_size, self.paper_colour,-1)

    def set_mode(self, columns):
        # set mode
        if self.nimbus.debug:
            message('set mode {}'.format(columns))
        # change screen size according to columns parameter
        if columns == 80:
            self.screen_size = (640, 250)
            self.cls()
        if columns == 40:
            self.screen_size = (320,250)
            self.set_paper(0)
            self.cls()

    def set_paper(self, colour):
        # set_paper
        if self.nimbus.debug:
            message('set_paper {}'.format(colour))
        self.paper_colour = self.colour_table[colour]
        