from tools import logo, message, fatal, colour_to_bgr, font_image_selecta, colrows_to_xy, plonk_image
import cv2
import numpy as np
import time
import threading
import random
import simpleaudio as sa
from pynput import keyboard
from videostream import VideoStream
from colour_table import colour_table, low_res_default_colours, high_res_default_colours
from command import Command
from welcome import welcome


# Floppy drive sounds: https://freesound.org/people/MrAuralization/packs/15891/

default_cursor_image = np.ones((2, 10, 3), dtype=np.uint8) * 255


class Nimbus:
    """Nimbus video display class.

    This class represents the Nimbus video display that will host the user
    interface for your application.  

    """

    def __onMouse(self, event, x, y, flags, param):
        """Handle mouse event

        """


        return


    def __init__(self, full_screen=False, debug=False, title='Nimbusinator', border_size=40):
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
        self.font_images = self.__load_fonts()
        self.logo = cv2.imread('data/rm-nimbus-logo.png')
        self.screen_size = (640, 250)                       # Screen size (initializes in high-res mode)
        self.border_size = border_size
        self.border_colour = 0                              # High-res initial border colour is blue
        self.paper_colour = 0                               # High-res initial paper colour is blue
        self.brush_colour = 3                               # High-res initial brush colour is white
        self.pen_colour = 3                                 # High-res initial pen colour is white
        self.cursor_position = (1, 1)                       # Initial cursor position is top-left
        self.plot_font = 0                                  # Initial plot font (charset for plot)
        self.charset = 0                                    # Initial charset (font for text)
        self.colour_table = colour_table                    # Dict to to convert Nimbus colour numbers to BGR
        self.low_res_default_colours = low_res_default_colours.copy()
        self.high_res_default_colours = high_res_default_colours.copy()
        self.low_res_colours = low_res_default_colours.copy()
        self.high_res_colours = high_res_default_colours.copy()
        self.cursor_image = default_cursor_image.copy()
        self.cursor_flash = False
        self.show_cursor = False
        self.floppy_is_running = False
        self.keyboard_buffer = []
        self.ctrl_pressed = False
        self.enter_was_pressed = False
        self.backspace_was_pressed = False
        self.vs = VideoStream(self.screen_size, queue_size=16).start()  # VideoStream object to display the Nimbus


    def __load_fonts(self):
        if self.debug:
            message('Loading fonts')
        fonts = {}
        for font in range(0, 2):
            font_img = cv2.imread('data/font{}.png'.format(font))
            fonts[font] = []
            for ascii_code in range(0, 256):
                fonts[font].append(font_image_selecta(font_img, ascii_code, font))
        return fonts

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


    def __cycle_cursor_flash(self):
        """Cycle the cursor flash

        This needs to run in it's own thread

        """
        while self.running:
            # When the Nimbus is boot flip cursor flash every 0.5 secs
            time.sleep(0.5)
            cursor_flash = self.cursor_flash
            self.cursor_flash = not cursor_flash


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

        # Calculate the actual display dimensions with border:
        horizontal_display_length = 640+(self.border_size*2)
        vertical_display_length = 500+(self.border_size*2)
        # Make the display image as an empty array then add the border colour
        display_data = np.zeros((vertical_display_length, horizontal_display_length, 3), dtype=np.uint8)
        cv2.rectangle(display_data, (0,0), (horizontal_display_length, vertical_display_length), colour_to_bgr(self, self.border_colour), -1)
        # Add cursor if showing cursor
        final_screen_data = screen_data.copy()
        if self.show_cursor:
            coord = colrows_to_xy(self.screen_size, self.cursor_position)
            # Only overlay cursor if on screen and cursor flash is true
            if coord[0] < self.screen_size[0] and self.cursor_flash:
                final_screen_data = plonk_image(self, screen_data, self.cursor_image, coord)
        # resize the combined screen_data and add it to display
        resized = cv2.resize(final_screen_data, (640, 500), interpolation=cv2.INTER_LINEAR_EXACT)
        display_data[self.border_size:self.border_size+resized.shape[0], self.border_size:self.border_size+resized.shape[1]] = resized
        return display_data


    def __screen_runner(self):
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
        cv2.namedWindow(self.title)
        # Nimbus's mouse feature won't be implemented until later
        cv2.setMouseCallback(self.title, self.__onMouse)
        # Display loop
        while self.running:
            frame = self.__render_display(self.vs.get_screen())
            cv2.imshow(self.title, frame)
            time.sleep(0.05)
            cv2.waitKey(5)
        if self.debug:
            message('Display loop stopped')


    def __floppy_drive_effects(self):
        """Simulate floppy drive grinding

        This has to be run a thread.  Two drive sounds are supplied: a
        short 'dot' sounds, and a long 'dash' sound, with 4 variations
        of each.  Semi-random patterns of dashes and dots are generated 
        with randomly-selected variations while the floppy_is_running
        flag is True.

        """
        while self.running:
            # Load sound effects
            dash = []
            dot = []
            for i in range(1, 5):
                dash.append(sa.WaveObject.from_wave_file('data/floppy-dash{}.wav'.format(i)))
                dot.append(sa.WaveObject.from_wave_file('data/floppy-dot{}.wav'.format(i)))
            # If flag is True play a bunch of grinding floppy drive sounds
            if self.floppy_is_running:
                # play dash (pick one at random)
                play_obj = dash[random.randint(0, 3)].play()
                play_obj.wait_done()
                # play random number of dots
                for i in range(0, random.randint(1, 5)):
                    # break out if drive is stopped
                    if not self.floppy_is_running:
                        return
                    else:
                        # pick one at random
                        play_obj = dot[random.randint(0, 3)].play()
                        play_obj.wait_done()


    def run_floppy(self, flag):
        """Run or stop the floppy drive sound effects

        Augment your user experience with the industrial melodies of a 
        1980s PC floppy drive

        Args:
            flag (boolean): True to run the drive, False to stop

        """

        if self.debug:
            message('run floppy {}'.format(flag))
        self.floppy_is_running = flag


    def __on_key_press(self, key):
        """Handle control key presses

        """
        
        # Printable chars go straight into the buffer
        try:
            self.keyboard_buffer.append(key.char)
            # BUT - if CTRL-C situation then shutdown!
            if self.ctrl_pressed and key.char.lower() == 'c':
                message('CTRL-C detected - shutting down')
                self.shutdown()
        except AttributeError:
            # Handle CTRL released
            if key == keyboard.Key.ctrl_l or keyboard.Key.ctrl_r:
                self.ctrl_pressed = True
            # Handle ENTER hit
            if key == keyboard.Key.enter:
                self.enter_was_pressed = True
            # Handle BACKSPACE hit
            if key == keyboard.Key.backspace:
                self.backspace_was_pressed = True
            # Also add spaces to buffer
            if key == keyboard.Key.space:
                self.keyboard_buffer.append(' ')


    def __on_key_release(self, key):
        """Handle control key releases

        """
        # Handle CTRL released
        if key == keyboard.Key.ctrl_l or keyboard.Key.ctrl_r:
            self.ctrl_pressed = False
        if key == keyboard.Key.esc:
            # Stop listener
            return False


    def boot(self, skip_welcome_screen=False):
        """Boot the Nimbus

        Reveal the Nimbus in all its glory, with or without a cheeky
        simulation of the famous Nimbus welcome screen.

        Args:
            skip_welcome_screen (bool), optional: Go straight to the application

        """

        # otherwise go ahead
        message('Booting up')
        if self.debug:
            message('Dropping runner into a thread')
        # Fire up screen runner in a thread
        t_screen = threading.Thread(target=self.__screen_runner, args=())
        t_screen.start()
        # Fire up cursor in another thread
        t_cursor = threading.Thread(target=self.__cycle_cursor_flash, args=())
        t_cursor.start()
        # Fire up the floppy disk effects in another
        t_floppy = threading.Thread(target=self.__floppy_drive_effects, args=())
        t_floppy.start()
        # Fire up the keyboard listener
        listener = keyboard.Listener(
            on_press=self.__on_key_press,
            on_release=self.__on_key_release)
        listener.start()
        if skip_welcome_screen:
            # don't bother with loading screen
            message('Running')
            Command(self).set_mode(80)
            return
        else:
            if self.debug:
                message('Running Welcome Screen')
            welcome(Command(self), self)
            Command(self).set_mode(80)
            if self.debug:
                message('Welcome Screen finished')
            message('Running')

  
    def shutdown(self):
        """Shutdown the Nimbus

        Stop everything and close the display Window.  This must be called to exit
        the application cleanly.

        """

        message('Shutting down')
        if self.debug:
            message('Stopping display loop and destroying cv2 windows')
        self.running = False
        cv2.destroyAllWindows()