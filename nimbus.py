from tools import logo, message, fatal, colour_to_bgr
import cv2
import numpy as np
import time
import threading
from videostream import VideoStream
from colour_table import colour_table, high_res_colour_table


class Nimbus:
    """Nimbus video display class.

    This class represents the Nimbus video display that will host the user
    interface for your application.  

    """

    def __init__(self, full_screen=False, debug=False, title='Nimbusinator'):
        """Create a new Nimbus object

        When created, the new Nimbus object is in a default state but will
        not be visible until the boot() method has been called.

        Args:
            full_screen (bool), optional: Full screen mode
            debug (bool), optional: Log debugging messages in the console if set to True
            title (str), optional: The title of the display window

        """

        print(logo)
        if debug:
            message('Running in debug mode.  Performance will be severely impeded, but still faster than a real Nimbus :D')
        self.full_screen = full_screen                      # Full screen flag
        self.debug = debug                                  # Debug flag
        self.running = True                                 # Flag to run or stop the Nimbus
        self.title = title                                  # Display window title
        self.screen_size = (640, 250)                       # Screen size (initializes in high-res mode)
        self.border_colour = 0                              # High-res initial border colour is blue
        self.paper_colour = 0                               # High-res initial paper colour is blue
        self.brush_colour = 3                               # High-res initial brush colour is white
        self.pen_colour = 3                                 # High-res initial pen colour is white
        self.cursor_position = (1, 1)                       # Initial cursor position is top-left
        self.colour_table = colour_table                    # Dict to to convert Nimbus colour numbers to BGR
        self.high_res_colour_table = high_res_colour_table  # Dict to map high-res colour numbers to all Nimbus colours
        self.vs = VideoStream(self.screen_size, queue_size=16).start()  # VideoStream object to display the Nimbus


    def get_cursor_position(self):
        """Get current cursor position

        Returns:
            (tuple): The current cursor position (col, row)

        """

        if self.debug:
            message('Get cursor position')
        return self.cursor_position

    def update_cursor_position(self, new_cursor_position):
        """Update cursor position

        Args:
            new_cursor_position (tuple): The new cursor position (col, row)

        """

        if self.debug:
            message('Update cursor position to {}'.format(new_cursor_position))
        self.cursor_position = new_cursor_position

    def update_screen(self, new_screen_data):
        """Update screen data

        Change the screen data to be displayed in VideoStream

        Args:
            new_screen_data (PIL image): The new screen data to be displayed

        """

        if self.debug:
            message('Updating screen data')
        self.vs.update_screen(new_screen_data)

    def get_screen(self):
        """Get screen data

        Get the screen data to be displayed from VideoStream

        Returns:
            (PIL image): The screen data to be displayed
        
        """

        if self.debug:
            message('Getting screen data')
        return self.vs.get_screen()
        
    def __render_display(self, screen_data):
        """Generate final display data including border

        In low-resolution mode the screen size is doubled and maintanes the same
        aspect ratio. It is then centrally overlayed on a larger image that acts
        as a border.  In high-resolution mode the original Nimbus would stretch
        the screen vertically to match the aspect ratio of low-resolution mode,
        making everything appear elongated.  It is then overlayed on the border as
        before.

        Args:
            screen_data (PIL image): The screen data to be displayed

        Returns:
            display_data (PIL image): The finished display data
        """

        border_size = 80        # Border size (really a constant)
        # Calculate the actual display dimensions with border:
        horizontal_display_length = 640+(border_size*2)
        vertical_display_length = 500+(border_size*2)
        # Make the display image as an empty array then add the border colour
        display_data = np.zeros((vertical_display_length, horizontal_display_length, 3), dtype=np.uint8)
        cv2.rectangle(display_data, (0,0), (horizontal_display_length, vertical_display_length), colour_to_bgr(self, self.border_colour), -1)
        # resize the screen_data and add it to display
        resized = cv2.resize(screen_data, (640, 500), interpolation=cv2.INTER_LINEAR_EXACT)
        display_data[border_size:border_size+resized.shape[0], border_size:border_size+resized.shape[1]] = resized
        return display_data

    def __runner(self):
        """Display the Nimbus in a window

        This function contains a loop which can be broken by setting
        the running flag to False.  It must be run within its own thread.

        """
        if self.debug:
            message('Running display loop')
        # Set full screen mode in OpenCV
        if self.full_screen:
            if self.debug:
                message('Full screen mode')
            cv2.namedWindow(self.title, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while self.running:
            frame = self.__render_display(self.vs.get_screen())
            cv2.imshow(self.title, frame)
            key_pressed = cv2.waitKey(5)
        if self.debug:
            message('Display loop stopped')
    
    def boot(self, skip_loading_screen=False):
        """Boot the Nimbus

        Reveal the Nimbus in all its glory, with or without a cheeky
        simulation of the famous Nimbus loading screen.

        Args:
            skip_loading_screen (bool), optional: Go straight to the application

        """

        if self.debug:
            message('Dropping runner into a thread')
        # Fire up runner in a thread
        t = threading.Thread(target=self.__runner, args=())
        t.start()
        if skip_loading_screen:
            # don't bother with loading screen
            return
        else:
            message('Please insert an operating system')
            time.sleep(1.5)
            message('Loading operating system')
            time.sleep(3)
            message('End of loading screen')
    
    def shutdown(self):
        """Shutdown the Nimbus

        Stop everything and close the display Window.  This must be called to exit
        the application cleanly.

        """

        if self.debug:
            message('Stopping display loop and destroying cv2 windows')
        self.running = False
        cv2.destroyAllWindows()