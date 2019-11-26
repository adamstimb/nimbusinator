import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from .tools_pg import logo, message, pil_to_pygame_image
from .colour_table import colour_table
from PIL import Image, ImageDraw, ImageColor
import threading


class Nimbus:
    """Nimbus video display class.

    This class represents the Nimbus video display that will host the user
    interface for your application.  When created, the new Nimbus object 
    will not be visible until the boot() method has been called.

    Args:
        full_screen (bool), optional: Full screen mode
        title (str), optional: The title of the display window

    """


    def empty_paper(self):
        """Return empty paper filled with the current paper colour"""

        return Image.new(
            'RGB',
            self.SCREEN_MODES[self.screen_mode], 
            self.COLOUR_TABLE[self.paper_colour]
        )


    def __init__(self, full_screen=False, title='Nimbusinator', border_size=40):
        """Create a new Nimbus object

        When created, the new Nimbus object  will
        not be visible until the boot() method has been called.

        Args:
            full_screen (bool), optional: Full screen mode
            title (str), optional: The title of the display window

        """

        print(logo)

        # Constants
        self.SCREEN_MODES = {                       # The absolute screen resolution for
            'hi': (640, 250),                       # high (80 column) and low-res (40
            'lo': (320, 250)                        # column) modes
            }
        self.COLOUR_TABLE = colour_table            # This is the RGB colour table from the Nimbus
        self.NORMALIZED_PAPER_SIZE = (640, 500)     # After drawing graphics and chars the paper is normalized to this size
        # Background size is the normalized paper size plus 2x border size:
        background_width = self.NORMALIZED_PAPER_SIZE[0] + (2 * border_size)
        background_height = self.NORMALIZED_PAPER_SIZE[1] + (2 * border_size)
        self.BACKGROUND_SIZE = (background_width, background_height)

        # Settings
        self.full_screen = full_screen
        self.title = title
        self.border_size = border_size

        # Variables
        self.screen_mode = 'hi'
        self.paper_colour = 1
        self.border_colour = 2

        # Initialize with empty paper
        self.paper_image = self.empty_paper()

        # Status flags
        self.__running = False                      # Set to True to run the Nimbus and the display


    def __display_loop(self):
        """The display loop

        Normalize paper image.  Overlay normalized image on background
        image to make the video image.  If not in full screen mode
        just show the video image.  If in full screen mode scale the
        video image to the display height, overlay it on a background
        image that has the same dimensions as the display, and show.
        The loop breaks if self.__running becomes false.

        """

        while self.__running:
            normalized_paper_image = self.paper_image.resize(self.NORMALIZED_PAPER_SIZE, resample=Image.NEAREST)
            background_image = Image.new(
                'RGB',
                self.BACKGROUND_SIZE,
                self.COLOUR_TABLE[self.border_colour]
            )
            background_image.paste(normalized_paper_image, (self.border_size, self.border_size))
            # Handle full screen
            if self.full_screen:
                # Calculate new dimensions and resize
                scale = self.__full_screen_display_size[1] / self.BACKGROUND_SIZE[1]
                new_size = (int(self.BACKGROUND_SIZE[0] * scale), self.__full_screen_display_size[1])
                background_image = background_image.resize(new_size, resample=Image.BICUBIC)
                display_x_offset = int((self.__full_screen_display_size[0] - new_size[0]) / 2)
            else:
                display_x_offset = 0
            # Create the video image, blit it and flip it
            video_image = pil_to_pygame_image(background_image)
            self.__pygame_display.blit(video_image, (display_x_offset, 0))
            pygame.display.flip() 


    def boot(self):
        """Boot the Nimbus"""

        # Don't boot if already running
        if self.__running:
            message('The Nimbus is already running')
            return

        message('Booting up')

        # Initialize pygame and handle full screen
        pygame.init()
        pygame.display.set_caption(self.title)
        if self.full_screen:
            # Full screen - get full screen size as display size and set pygame flags
            self.__full_screen_display_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            display_size = self.__full_screen_display_size
            flags = pygame.FULLSCREEN
        else:
            # Run in window - use background size as display size and set pygame flags
            display_size = self.BACKGROUND_SIZE
            flags = 0
        self.__pygame_display = pygame.display.set_mode(display_size, flags=flags)

        # Set flags
        self.__running = True

        # Start display loop in a thread
        self.__display_thread = threading.Thread(target=self.__display_loop, args=())
        self.__display_thread.start()

    
    def shutdown(self):
        """Shut down the Nimbus"""

        # Don't shutdown if not running
        if not self.__running:
            message('The Nimbus is already shutdown')
            return

        message('Shutting down')

        # Set flags
        self.__running = False

        # Join threads
        self.__display_thread.join()

        # Quit pygame and exit
        pygame.quit()
        message('Finished')
        sys.exit(1)