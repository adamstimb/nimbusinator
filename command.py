from tools import message, fatal, is_valid_colour, colour_to_bgr, fix_coord, colrows_to_xy
import numpy as np
import cv2

import time

class Command:
    """Nimbus commands

    This class contains the commands to control the Nimbus display.  The commands
    mimick the syntax found in RM Basic but re-written Pythonically.  For example
    in RM Basic we could write a command to plot a greeting in yellow at position 
    20, 30 with font size 2 like this:

    PLOT "Hello Nimbus!", 20, 20 SIZE 2 BRUSH 14

    And with the Command class we can write the same instruction like this:

    .plot("Hello Nimbus!", (20, 20), size=2, brush=14)

    Notice that x, y coordinates are written in tuples.  For drawing commands we
    use a list of tuples instead of the semicolon notation used by RM Basic. For 
    example this:

    AREA 0, 0; 50, 50; 100, 0 BRUSH 13

    Becomes this:

    .area([(0, 0), (50, 50), (100, 0)], brush=13)

    """

    def __init__(self, nimbus):
        """Create a new Command object

        In creating an object of this class it must be bound to
        a pre-existing Nimbus object.

        Args:
            nimbus (Nimbus): The Nimbus object to bind to
        
        """
        if nimbus.debug:
            message('Binding Nimbus commands')
        self.nimbus = nimbus


    def cls(self):
        """Clear the screen of all text and graphics and reset cursor position

        """
        if self.nimbus.debug:
            message('cls')
        # Wipe screen data in the Nimbus and fill screen with paper colour. First
        # define a new PIL image to make sure it matches the current screen mode, 
        # e.g. if set_mode was just called
        screen_data = np.zeros((self.nimbus.screen_size[1], self.nimbus.screen_size[0], 3), dtype=np.uint8)
        cv2.rectangle(screen_data, (0,0), (self.nimbus.screen_size[0], self.nimbus.screen_size[1]), colour_to_bgr(self.nimbus, self.nimbus.paper_colour),-1)
        self.nimbus.update_screen(screen_data)

    def set_mode(self, columns):
        """Select either high-resolution or low-resolution screen mode

        In RM Basic the screen resolution was set by the number of columns: 
        40 for low-resolution and 80 for high-resolution.  Any other values
        has no effect.  Nimbusinator is more strict and will yield an error
        if any other values are entered.  Check the original RM Basic manual
        for a description of how screen resolutions worked on the Nimbus.
        High-resolution mode is particularly odd.

        Args:
            columns (int): The number of colums (40 or 80)

        """
        if self.nimbus.debug:
            message('set mode {}'.format(columns))
        # change screen size and set default colours accordingly
        if columns == 80:
            self.nimbus.screen_size = (640, 250)
            self.set_paper(0)
            self.set_border(0)
            self.set_brush(3)
            self.cls()
            return
        if columns == 40:
            self.nimbus.screen_size = (320, 250)
            self.set_paper(0)
            self.set_border(0)
            self.set_brush(15)
            self.cls()
            return
        # Invalid choice (RM Basic wasn't fussy about this but I am)
        message('{} is not a valid choice for columns since set_mode only accepts 40 or 80'.format(columns))
        fatal(self.nimbus)
        

    def set_paper(self, colour):
        """Set the paper colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """
        if self.nimbus.debug:
            message('set paper {}'.format(colour))
        self.nimbus.paper_colour = is_valid_colour(self.nimbus, colour)
        
    
    def set_border(self, colour):
        """Set the border colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """
        if self.nimbus.debug:
            message('set border {}'.format(colour))
        self.nimbus.border_colour = is_valid_colour(self.nimbus, colour)
    

    def set_brush(self, colour):
        """Set the brush colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """
        if self.nimbus.debug:
            message('set brush {}'.format(colour))
        self.nimbus.brush_colour = is_valid_colour(self.nimbus, colour)


    def set_curpos(self, cursor_position):
        """Set the cursor position

        Args:
            cursor_position (tuple): The new cursor position (column, row)

        """

        if self.nimbus.debug:
            message('set curpos {}'.format(cursor_position))
        # Validate that cursor will still be on screen
        # Column
        if cursor_position[0] < 1 or cursor_position[0] * 8 >= self.nimbus.screen_size[0]:
            message('Column {} is not on the screen'.format(cursor_position[0]))
            fatal(self.nimbus)
        # Row
        if cursor_position[1] < 1 or cursor_position[1] * 10 >= self.nimbus.screen_size[1]:
            message('Column {} is not on the screen'.format(cursor_position[1]))
            fatal(self.nimbus)
        # Now update the cursor position
        self.nimbus.update_cursor_position(cursor_position)


    def put(self, ascii_data):
        """Put a single character or string at the current cursor position

        Args:
            ascii_data (int/str): If an int is passed the corresponding ASCII character
                                    will be plotted.  If a string is passed then the 
                                    string will be printed without a terminating carriage
                                    return.

        """
        if self.nimbus.debug:
            message('put {}'.format(ascii_data))
        # Handle integer
        if isinstance(ascii_data, int):
            ascii_list = [ascii_data]
        if isinstance(ascii_data, str):
            ascii_list = ascii_data
        for ascii in ascii_list:
            # Get screen position in pixels from cursor position
            curpos_xy = colrows_to_xy(self.nimbus.screen_size, self.nimbus.get_cursor_position())
            if self.nimbus.debug:
                message('curpos {} resolved to screen position {}'.format(self.nimbus.get_cursor_position(), curpos_xy))
            # Plot char
            screen_data = self.nimbus.get_screen()
            cv2.rectangle(
                screen_data, 
                fix_coord(self.nimbus.screen_size, (curpos_xy[0], curpos_xy[1])), 
                fix_coord(self.nimbus.screen_size, (curpos_xy[0] + 8, curpos_xy[1] + 10)), 
                colour_to_bgr(self.nimbus, self.nimbus.pen_colour), 
                1
            )
            # calculate new curpos, if over the right-hand side do carriage return
            new_column = self.nimbus.get_cursor_position()[0] + 1
            if new_column * 8 >= self.nimbus.screen_size[0]:
                if self.nimbus.debug:
                    message('carriage return')
                # do carriage return
                new_column = 1  # return to left-hand side
                new_row = self.nimbus.get_cursor_position()[1] + 1  # move down
                # if we're below, then screen, move screen data up 10 pixels and set
                # cursor to bottom of screen
                if new_row * 10 >= self.nimbus.screen_size[1]:
                    new_row -= 1
                    message('Shove screen up')
                    # Shove screen up.  First crop the top line:
                    old_screen_data = self.nimbus.get_screen()[:, :-10]
                    message('{}'.format(old_screen_data.shape))
                    # Make a blank screen
                    screen_data = np.zeros((self.nimbus.screen_size[1], self.nimbus.screen_size[0], 3), dtype=np.uint8)
                    # And overlay the old_screen_data
                    screen_data[:, :-10] = old_screen_data
                    # Update screen
                    self.nimbus.update_screen(screen_data)
                    time.sleep(5)
            else:
                # don't move cursor down
                new_row = self.nimbus.get_cursor_position()[1]
            # move cursor
            self.set_curpos((new_column, new_row))


    def line(self, coord_list, brush=None):
        """Draw one or more connected straight lines

        Args:
            coord_list (list): A list of (x, y) tuples
            brush (int), optional: Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """
        if self.nimbus.debug:
            message('line {} brush={}'.format(coord_list, brush))
        # if default brush value then get current brush colour
        if brush is None:
            brush = self.nimbus.brush_colour
            if self.nimbus.debug:
                message('using current brush colour {}'.format(brush))
        # validate brush
        brush = is_valid_colour(self.nimbus, brush)
        # draw lines on screen
        screen_data = self.nimbus.get_screen()
        for i in range(0, len(coord_list) - 1):
            cv2.line(screen_data, fix_coord(self.nimbus.screen_size, coord_list[i]), fix_coord(self.nimbus.screen_size, coord_list[i+1]), colour_to_bgr(self.nimbus, brush), 1)
        self.nimbus.update_screen(screen_data)