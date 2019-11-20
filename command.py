from tools import message, fatal, is_valid_colour, colour_to_bgr, fix_coord, colrows_to_xy
from tools import plonk_image, plonk_transparent_image, colour_char
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
        screen_data = np.zeros((self.nimbus.screen_size[1]+1, self.nimbus.screen_size[0]+1, 3), dtype=np.uint8)
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
            self.nimbus.high_res_colours = self.nimbus.high_res_default_colours.copy()
            self.set_paper(0)
            self.set_border(0)
            self.set_brush(3)
            self.set_pen(3)
            self.set_curpos((1, 1))
            self.cls()
            return
        if columns == 40:
            self.nimbus.screen_size = (320, 250)
            self.nimbus.low_res_colours = self.nimbus.low_res_default_colours.copy()
            self.set_paper(0)
            self.set_border(0)
            self.set_brush(15)
            self.set_pen(15)
            self.set_curpos((1, 1))
            self.cls()
            return
        # Invalid choice (RM Basic wasn't fussy about this but I am)
        message('{} is not a valid choice for columns since set_mode only accepts 40 or 80'.format(columns))
        fatal(self.nimbus)


    def set_cursor(self, flag):
        """Show or hide cursor

        Args:
            flag (boolean): True to show cursor, False to hide

        """
        if self.nimbus.debug:
            message('set cursor {}'.format(flag))
        self.nimbus.show_cursor = flag


    def plonk_logo(self, coord):
        """Plonk the RM Nimbus logo on screen

        Args:
            coord (tuple): The (x, y) position to plonk the logo

        """

        if self.nimbus.debug:
            message('plonk logo {}'.format(coord))
        screen_data = self.nimbus.get_screen()
        screen_data = plonk_image(self.nimbus, screen_data, self.nimbus.logo, coord)
        self.nimbus.update_screen(screen_data)


    def set_paper(self, colour):
        """Set the paper colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """

        if self.nimbus.debug:
            message('set paper {}'.format(colour))
        self.nimbus.paper_colour = is_valid_colour(self.nimbus, colour)
        
    
    def set_colour(self, colour1, colour2):
        """Set a colour to a new colour

        Args:
            colour1 (int): The colour code to be changed
            colour2 (int): The new colour to be assigned to colour1
        
        """

        if self.nimbus.debug:
            message('set colour {} to {}'.format(colour1, colour2))
        if self.nimbus.screen_size == (320, 250):
            self.nimbus.low_res_colours[is_valid_colour(self.nimbus, colour1)] = colour2
        if self.nimbus.screen_size == (640, 250):
            self.nimbus.high_res_colours[is_valid_colour(self.nimbus, colour1)] = colour2


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


    def set_pen(self, colour):
        """Set the pen colour

        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """

        if self.nimbus.debug:
            message('set pen {}'.format(colour))
        self.nimbus.pen_colour = is_valid_colour(self.nimbus, colour)


    def set_charset(self, charset):
        """Set the charset for text

        Args:
            charset (int): 0 is the standard font, 1 is the other font!

        """

        if self.nimbus.debug:
            message('set charset {}'.format(charset))
        self.nimbus.charset = charset


    def ask_charset(self):
        """Return the current charset for text

        Returns:
            charset (int): 0 is the standard font, 1 is the other font

        """

        return self.nimbus.charset


    def set_curpos(self, cursor_position):
        """Set the cursor position

        Args:
            cursor_position (tuple): The new cursor position (column, row)

        """

        if self.nimbus.debug:
            message('set curpos {}'.format(cursor_position))
        # Validate that cursor will still be on screen
        # Column
        if colrows_to_xy(self.nimbus.screen_size, (cursor_position[0], 1))[0] >= self.nimbus.screen_size[0]:
            message('Column {} is not on the screen'.format(cursor_position[0]))
            fatal(self.nimbus)
        # Row
        if colrows_to_xy(self.nimbus.screen_size, (1, cursor_position[1]))[1] < 0:
            message('Column {} is not on the screen'.format(cursor_position[1]))
            fatal(self.nimbus)
        # Now update the cursor position
        self.nimbus.update_cursor_position(cursor_position)


    def ask_curpos(self):
        """Gets the current cursor position

        Returns:
            cursor_position (tuple): The current cursor position (column, row)

        """

        if self.nimbus.debug:
            message('ask curpos')
        # Return cursor position
        return self.nimbus.get_cursor_position()


    def plot(self, text, coords, size=1, brush=None, direction=0, font=None):
        """Plot text on the screen

        Args:
            text (str): The text to be plotted
            coords (tuple): The (x, y) position of the text
            size (int): Font size. To elongate pass a tuple (x_size, y_size)
            brush (int): Brush colour
            direction (int): 0=normal, 1=-90deg, 2=180deg, 3=-270deg
            font (int): 0 is the standard font, 1 is the other font

        """

        # Handle is_black workaround
        if colour_to_bgr(self.nimbus, brush) == [0, 0, 0]:
            is_black = True
        else:
            is_black = False

        # Handle brush colour
        if brush is None:
            brush = self.nimbus.brush_colour

        # Handle font
        if font is None:
            font = self.nimbus.plot_font

        # Create a temporary image of the plotted text
        plot_img_width = len(text) * 9
        plot_img = np.zeros((10, plot_img_width, 3), dtype=np.uint8)
        x = 0
        for char in text:
            if is_black:
                char_img = cv2.bitwise_not(self.nimbus.font_images[font][ord(char)])
            else:
                char_img = colour_char(self.nimbus, brush, cv2.bitwise_not(self.nimbus.font_images[font][ord(char)]))
            plot_img = plonk_image(self.nimbus, plot_img, char_img, (x, 0), custom_size=(plot_img_width, 10))
            x += 8
        
        # resize
        if isinstance(size, tuple):
            # tuple: extract x_size, y_size
            x_size, y_size = size
        else:
            x_size = size
            y_size = size
        resized = cv2.resize(plot_img, (plot_img.shape[1]*x_size, plot_img.shape[0]*y_size), interpolation=0)
        
        # rotate
        for i in range(0, direction):
            resized = cv2.rotate(resized, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        # rebuild screen and done
        screen_data = self.nimbus.get_screen()
        screen_data = plonk_transparent_image(self.nimbus, screen_data, resized, coords, is_black=is_black)
        self.nimbus.update_screen(screen_data)


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

        # Handle is_black workaround
        if colour_to_bgr(self.nimbus, self.nimbus.pen_colour) == [0, 0, 0]:
            is_black = True
        else:
            is_black = False

        # Handle integer
        if isinstance(ascii_data, int):
            ascii_list = [ascii_data]
        if isinstance(ascii_data, str):
            ascii_list = ascii_data
        for ascii in ascii_list:
            # Get char img
            char_img = self.nimbus.font_images[self.nimbus.charset][ord(ascii)]
            # Get screen position in pixels from cursor position
            curpos_xy = colrows_to_xy(self.nimbus.screen_size, self.nimbus.get_cursor_position())
            if self.nimbus.debug:
                message('curpos {} resolved to screen position {}'.format(self.nimbus.get_cursor_position(), curpos_xy))
            # Plot char and apply paper colour underneath char
            screen_data = self.nimbus.get_screen()
            # Paper colour
            cv2.rectangle(
                screen_data, 
                fix_coord(self.nimbus.screen_size, (curpos_xy[0], curpos_xy[1])), 
                fix_coord(self.nimbus.screen_size, (curpos_xy[0] + 8, curpos_xy[1] + 10)), 
                colour_to_bgr(self.nimbus, self.nimbus.paper_colour), 
                -1
            )
            # Overlay char, colourise and preserve paper colour
            if is_black:
                char_img = cv2.bitwise_not(char_img)
            else:
                char_img = colour_char(self.nimbus, self.nimbus.pen_colour, cv2.bitwise_not(char_img))
            screen_data = plonk_transparent_image(self.nimbus, screen_data, char_img, (curpos_xy[0], curpos_xy[1]), is_black=is_black)
            # calculate new curpos, if over the right-hand side do carriage return
            self.nimbus.update_screen(screen_data)
            new_column = self.nimbus.get_cursor_position()[0] + 1
            if colrows_to_xy(self.nimbus.screen_size, (new_column, 1))[0] >= self.nimbus.screen_size[0]:
                if self.nimbus.debug:
                    message('carriage return')
                # do carriage return
                new_column = 1  # return to left-hand side
                new_row = self.nimbus.get_cursor_position()[1] + 1  # move down
                # if we're below, then screen, move screen data up 10 pixels and set
                # cursor to bottom of screen
                if colrows_to_xy(self.nimbus.screen_size, (1, new_row))[1] < 0:
                    new_row = self.nimbus.get_cursor_position()[1]
                    # Shove screen up.  First crop the top line:
                    old_screen_data = self.nimbus.get_screen()[10:, :]
                    # Make a blank screen and apply paper colour (same as Nimbus did it)
                    screen_data = np.zeros((self.nimbus.screen_size[1]+1, self.nimbus.screen_size[0]+1, 3), dtype=np.uint8)
                    cv2.rectangle(screen_data, (0,0), (self.nimbus.screen_size[0], self.nimbus.screen_size[1]), colour_to_bgr(self.nimbus, self.nimbus.paper_colour),-1)
                    # And overlay the old_screen_data
                    screen_data[:-10, :] = old_screen_data
                    # Update screen
                    self.nimbus.update_screen(screen_data)
            else:
                # don't move cursor down
                new_row = self.nimbus.get_cursor_position()[1]
            # move cursor
            self.set_curpos((new_column, new_row))
            
    def print(self, text):
        """Print a string with carriage return at end

        Args:
            text (str): The text to be printed

        """

        self.put(text)
        # Carriage return?
        col, row = self.ask_curpos()
        if col > 1:
            # Yep - smash the cursor off the screen and use put to force CR
            self.nimbus.cursor_position = (255, row)
            self.put('X')


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
    

    def area(self, coord_list, brush=None):
        """Draw a filled polygon

        Args:
            coord_list (list): A list of (x, y) tuples
            brush (int), optional: Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """

        if self.nimbus.debug:
            message('area {} brush={}'.format(coord_list, brush))
        # if default brush value then get current brush colour
        if brush is None:
            brush = self.nimbus.brush_colour
            if self.nimbus.debug:
                message('using current brush colour {}'.format(brush))
        # validate brush
        brush = is_valid_colour(self.nimbus, brush)
        # convert coord_list into array
        poly_list = []
        for coord in coord_list:
            coord = fix_coord(self.nimbus.screen_size, coord)
            poly_list.append([coord[0], coord[1]])
        # draw filled polygon on screen
        screen_data = self.nimbus.get_screen()
        cv2.fillPoly(screen_data, np.array([poly_list]), colour_to_bgr(self.nimbus, brush))
        self.nimbus.update_screen(screen_data)