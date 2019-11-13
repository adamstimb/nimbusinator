from tools import logo, message, fatal
import cv2
import numpy as np
import time
import threading
from videostream import VideoStream
from colour_table import colour_table


class Nimbus:

    def __init__(self, zoom=1, full_screen=False, debug=True, title='Nimbusinator'):
        # Create a new Nimbus object
        print(logo)
        if debug:
            message('Creating a new Nimbus')
        self.zoom = zoom
        self.full_screen = full_screen
        self.debug = debug
        self.running = True
        self.title = title
        self.screen_size = (640, 250)
        self.border_colour = 1
        self.colour_table = colour_table
        self.vs = VideoStream(self.screen_size, queue_size=16).start()

    def update(self, new_screen_data):
        # Update screen data
        if self.debug:
            message('Updating screen data')
        self.vs.update_screen(new_screen_data)

    def render_display(self, screen_data):
        # generate actual size display data including border
        border_size = 20
        vertical_display_length = 640+(border_size*2)
        horizontal_display_length = 500+(border_size*2)
        display_data = np.zeros(shape=[vertical_display_length, horizontal_display_length, 3], dtype=np.uint8)
        # add the background
        cv2.rectangle(display_data, (0,0), (vertical_display_length, horizontal_display_length), self.colour_table[self.border_colour], -1)
        # resize the screen_data and add it to display
        resized = cv2.resize(screen_data, (500, 640))
        x_offset=y_offset=20
        display_data[y_offset:y_offset+resized.shape[0], x_offset:x_offset+resized.shape[1]] = resized
        return display_data

    def runner(self):
        # Display loop
        if self.debug:
            message('Running display loop')
        while self.running:
            frame = self.render_display(self.vs.read())
            cv2.imshow(self.title, frame)
            key_pressed = cv2.waitKey(5)
        if self.debug:
            message('Display loop stopped')
    
    def boot(self, skip_loading_screen=False):
        # Boot the Nimbus
        if self.debug:
            message('Dropping runner into a thread')
        t = threading.Thread(target=self.runner, args=())
        t.start()
        if skip_loading_screen:
            # don't bother with loading screen
            return
        else:
            message('Loading screen started')
            message('Please insert an operating system')
            time.sleep(1.5)
            message('Loading operating system')
            time.sleep(3)
            message('End of loading screen')
    
    def shutdown(self):
        # Stop the Nimbus
        if self.debug:
            message('Stopping display loop and destroying cv2 windows')
        self.running = False
        cv2.destroyAllWindows()