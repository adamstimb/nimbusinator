from tools import message, fatal
import numpy as np
import cv2


class Command:

    def __init__(self, nimbus):
        # Initialize commands and global parameters
        if nimbus.debug:
            message('Initializing Nimbus commands')
        self.nimbus = nimbus

    def cls(self):
        # cls
        if self.nimbus.debug:
            message('cls')
        self.nimbus.update(np.zeros((self.nimbus.screen_size[1], self.nimbus.screen_size[0], 3), dtype=np.uint8))
        cv2.rectangle(self.nimbus.vs.screen_data, (0,0), (self.nimbus.screen_size[0], self.nimbus.screen_size[1]), self.nimbus.paper_colour,-1)

    def set_mode(self, columns):
        # set mode
        if self.nimbus.debug:
            message('set mode {}'.format(columns))
        # change screen size according to columns parameter
        if columns == 80:
            self.nimbus.screen_size = (640, 250)
            self.cls()
        if columns == 40:
            self.nimbus.screen_size = (320,250)
            self.set_paper(0)
            self.cls()

    def set_paper(self, colour):
        # set_paper
        if self.nimbus.debug:
            message('set paper {}'.format(colour))
        self.nimbus.paper_colour = self.nimbus.colour_table[colour]
    
    def set_border(self, colour):
        # set_border
        if self.nimbus.debug:
            message('set border {}'.format(colour))
        self.nimbus.border_colour = colour
        