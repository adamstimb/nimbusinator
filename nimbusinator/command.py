from .tools import is_valid_colour, colrows_to_xy, recolour, fix_coord
from PIL import Image, ImageDraw
import copy


class Command:
    """Nimbus commands

    This class contains the commands to control the Nimbus display.  The commands
    mimick the syntax found in RM Basic but re-written Pythonically.  In creating an 
    object of this class it must be bound to a pre-existing Nimbus object.  It is
    highly recommended to read the original Nimbus manuals (particularly RM Basic)
    to get a deeper understanding of how these commands originally worked.

    Args:
        nimbus (Nimbus): The Nimbus object to bind to

    """


    def __init__(self, nimbus):
        """Create a new Command object

        In creating an object of this class it must be bound to
        a pre-existing Nimbus object.

        Args:
            nimbus (Nimbus): The Nimbus object to bind to
        
        """

        # Validate params
        # To avoid circular import we can't put Nimbus in isintance but we can
        # assert that the object contains a string called title.
        #assert isinstance(nimbus.title, str), "Command object needs to be bound to a Nimbus object"
        self.nimbus = nimbus


    def set_paper(self, colour):
        """Set the paper colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(colour, int), "The value of colour must be an integer, not {}".format(type(colour))
        assert is_valid_colour(self.nimbus, colour), "Colour {} is out-of-range for this screen mode".format(colour)

        self.nimbus.paper_colour = colour
        
    
    def set_colour(self, colour1, colour2):
        """Set a colour to a new colour

        Args:
            colour1 (int): The colour code to be changed
            colour2 (int): The new colour to be assigned to colour1
        
        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(colour1, int), "The value of colour1 must be an integer, not {}".format(type(colour1))
        assert isinstance(colour2, int), "The value of colour2 must be an integer, not {}".format(type(colour2))
        assert (colour2 >= 0 and colour2 <= 15), "The value of colour 2 must be >= 0 and <= 15, not {}".format(colour2)
        assert is_valid_colour(self.nimbus, colour1), "Colour1 {} is out-of-range for this screen mode".format(colour1)

        self.nimbus.runtime_colours[self.nimbus.screen_mode][colour1] = self.nimbus.DEFAULT_COLOURS['lo'][colour2]


    def set_border(self, colour):
        """Set the border colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """
 
        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(colour, int), "The value of colour must be an integer, not {}".format(type(colour))
        assert is_valid_colour(self.nimbus, colour), "Colour {} is out-of-range for this screen mode".format(colour)

        self.nimbus.border_colour = colour
    

    def set_brush(self, colour):
        """Set the brush colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(colour, int), "The value of colour must be an integer, not {}".format(type(colour))
        assert is_valid_colour(self.nimbus, colour), "Colour {} is out-of-range for this screen mode".format(colour)

        self.nimbus.brush_colour = colour


    def set_pen(self, colour):
        """Set the pen colour

        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(colour, int), "The value of colour must be an integer, not {}".format(type(colour))
        assert is_valid_colour(self.nimbus, colour), "Colour {} is out-of-range for this screen mode".format(colour)

        self.nimbus.pen_colour = colour


    def set_charset(self, charset):
        """Set the charset for text

        Args:
            charset (int): 0 is the standard font, 1 is the other font!

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(charset, int), "The value of charset must be an integer, not {}".format(type(charset))
        assert (charset == 0 or charset == 1), "The value of charset can be either 0 or 1, not {}".format(charset)

        self.nimbus.charset = charset


    def set_plot_font(self, plot_font):
        """Set the plot font

        Args:
            plot_font (int): 0 is the standard font, 1 is the other font!

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(plot_font, int), "The value of plot_font must be an integer, not {}".format(type(plot_font))
        assert (plot_font == 0 or plot_font == 1), "The value of plot_font can be either 0 or 1, not {}".format(plot_font)

        self.nimbus.plot_font = plot_font


    def ask_charset(self):
        """Return the current charset for text

        0 is the standard font, 1 is the other font

        Returns:
            int

        """

        return self.nimbus.charset


    def ask_plot_font(self):
        """Return the current plot_font

        0 is the standard font, 1 is the other font

        Returns:
            int

        """

        return self.nimbus.plot_font
        

    def ask_pen(self):
        """Return the current pen colour

        Returns:
            int

        """

        return self.nimbus.pen_colour


    def ask_paper(self):
        """Return the current paper colour

        Returns:
            int

        """

        return self.nimbus.paper_colour


    def ask_brush(self):
        """Return the current brush colour

        Returns:
            int
        """

        return self.nimbus.brush_colour


    def set_curpos(self, cursor_position):
        """Set the cursor position

        Args:
            cursor_position (tuple): The new cursor position (column, row)

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # Validate params
        assert isinstance(cursor_position, tuple), "The value of cursor_position must be a tuple, not {}".format(type(cursor_position))
        assert len(cursor_position) == 2, "The cursor_position tuple must have 2 values, not {}".format(len(cursor_position))
        for i in range(0, 2):
            assert isinstance(cursor_position[i], int), "This value in cursor_position must be an integer, not{}".format(type(cursor_position[i]))
        # Validate that cursor will still be on screen
        assert cursor_position[0] >= 0, "Negative column value in {} is not permitted".format(cursor_position)
        assert cursor_position[1] >= 0, "Negative row value in {} is not permitted".format(cursor_position)
        assert cursor_position[1] <= 25, "There are only 25 rows, not {}".format(cursor_position[1])
        if self.nimbus.screen_mode == 'hi':
            assert cursor_position[0] <= 80, "There are only 80 columns in this mode, not {}".format(cursor_position[0])
        if self.nimbus.screen_mode == 'lo':
            assert cursor_position[0] <= 40, "There are only 40 columns in this mode, not {}".format(cursor_position[0])

        # Now update the cursor position
        self.nimbus.cursor_position = cursor_position


    def ask_curpos(self):
        """Gets the current cursor position as column index, row index

        Returns:
            (int, int)

        """

        # Return cursor position
        return self.nimbus.cursor_position


    def cls(self):
        """Clear the screen of all text and graphics and reset cursor position

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # Wipe paper image in the Nimbus and reset cursor position
        self.nimbus.paper_image = self.nimbus.empty_paper()
        self.set_curpos((1, 1))


    def set_mode(self, columns):
        """Select either high-resolution or low-resolution screen mode

        In RM Basic the screen resolution was set by the number of columns:  40 for low-resolution and 80 for 
        high-resolution.  Any other values had no effect.  Nimbusinator is more strict and will yield an error
        if any other values are entered.  Check the original RM Basic manual for a description of how screen 
        resolutions worked on the Nimbus.

        MODE 40: 40 columns, 25 rows; 320 pixels wide, 250 pixels high; 16 colours

        MODE 80: 80 columns, 25 rows; 640 pixels wide, 250 pixels high (but doubled along vertical axis); 4 colours

        Args:
            columns (int): The number of colums (40 or 80)

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(columns, int), "The value of columns must be integer, not {}".format(columns)
        assert (columns == 80 or columns == 40), "The value of columns can be 80 or 40, not {}".format(columns)

        # restore default colors
        self.nimbus.runtime_colours = copy.deepcopy(self.nimbus.DEFAULT_COLOURS)

        # change screen size and set default colours accordingly
        if columns == 80:
            self.nimbus.screen_mode = 'hi'
            self.set_paper(0)
            self.set_border(0)
            self.set_brush(3)
            self.set_pen(3)
            self.set_curpos((1, 1))
            self.cls()
            return
        if columns == 40:
            self.nimbus.screen_mode = 'lo'
            self.set_paper(0)
            self.set_border(0)
            self.set_brush(15)
            self.set_pen(15)
            self.set_curpos((1, 1))
            self.cls()
            return


    def plonk_logo(self, coord):
        """Plonk the RM Nimbus logo on screen

        Args:
            coord (tuple): The (x, y) position to plonk the logo

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(coord, tuple), "The value of coord must be a tuple, not {}".format(coord)
        assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
        for i in range(0, 2):
            assert isinstance(coord[i], int), "This value in coord must be an integer, not{}".format(coord[i])

        self.nimbus.plonk_image_on_paper(self.nimbus.NIMBUS_LOGO, coord)


    def put(self, ascii_data):
        """Put a single character or string at the current cursor position

        Args:
            ascii_data (int/str): If an int is passed the corresponding ASCII character
                                    will be plotted.  If a string is passed then the 
                                    string will be printed without a terminating carriage
                                    return.

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # Validate params
        assert isinstance(ascii_data, (str, int)), "The value of ascii_data must be an integer or string, not {}".format(type(ascii_data))

        # Handle integer
        if isinstance(ascii_data, int):
            # validate in extended ASCII range
            assert (ascii_data >= 0 and ascii_data <= 255), "The value {} of ascii_data is outside the range of Extended ASCII (0-255)".format(ascii_data)
            # convert to char
            ascii_list = [chr(ascii_data)]
        # Handle string
        if isinstance(ascii_data, str):
            ascii_list = ascii_data
        
        # Put char or chars
        for ascii in ascii_list:

            # return if shutdown detected
            if not self.nimbus.running:
                return

            # If out of extended ASCII range replace with space
            if ord(ascii) > 255:
                # It's out of range
                ascii = ' '
            # Get char img
            char_img = self.nimbus.FONT_IMAGES[self.nimbus.charset][ord(ascii)]
            # Get screen position in pixels from cursor position
            curpos_xy = colrows_to_xy(self.nimbus.SCREEN_MODES[self.nimbus.screen_mode], self.nimbus.cursor_position)
            # Plot char and apply paper colour underneath char
            empty_char_image = recolour(self.nimbus, self.nimbus.EMPTY_CHAR_IMAGE, (0, 0, 0), self.nimbus.COLOUR_TABLE[self.nimbus.runtime_colours[self.nimbus.screen_mode][self.nimbus.paper_colour]], has_alpha=True)
            self.nimbus.plonk_image_on_paper(empty_char_image, curpos_xy, transparent=True)
            # Overlay char, colourise and preserve paper colour
            char_img = recolour(self.nimbus, char_img, (0, 0, 0), self.nimbus.COLOUR_TABLE[self.nimbus.runtime_colours[self.nimbus.screen_mode][self.nimbus.pen_colour]], has_alpha=True)
            self.nimbus.plonk_image_on_paper(char_img, curpos_xy, transparent=True)
            # calculate new curpos, if over the right-hand side do carriage return
            new_column = self.nimbus.cursor_position[0] + 1
            if (self.nimbus.screen_mode == 'lo' and new_column > 40) or (self.nimbus.screen_mode == 'hi' and new_column > 80):
                # do carriage return
                new_column = 1  # return to left-hand side
                new_row = self.nimbus.cursor_position[1] + 1  # move down
                # if we're below, then screen, move screen data up 10 pixels and set
                # cursor to bottom of screen
                if new_row > 25:
                    new_row = 25
                    # Make a blank paper image and paste the old paper image 10 pixels higher 
                    # than the top and update actual paper image
                    new_paper_image = self.nimbus.empty_paper()
                    new_paper_image.paste(self.nimbus.paper_image, (0, -10))
                    self.nimbus.paper_image = new_paper_image
            else:
                # don't move cursor down
                new_row = self.nimbus.cursor_position[1]
            # move cursor
            self.set_curpos((new_column, new_row))


    def set_cursor(self, flag):
        """Show or hide cursor

        Args:
            flag (boolean): True to show cursor, False to hide

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(flag, bool), "The value of flag must be boolean, not {}".format(flag)

        self.nimbus.cursor_enabled = flag


    def print(self, text):
        """Print a string with carriage return at end

        Args:
            text (str): The text to be printed

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # Validate params
        assert isinstance(text, str), "The value of text must be a string, not {}".format(type(text))

        # Put the string and then maybe CR
        self.put(text)
        # Carriage return?
        col, row = self.ask_curpos()
        if col > 1:
            # Yep - smash the cursor off the screen and use put to force CR
            self.nimbus.cursor_position = (255, row)
            self.put('X')


    def flush(self):
        """Clears the keyboard buffer

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        self.nimbus.keyboard_buffer = []


    def gets(self):
        """Get the oldest char in the keyboard buffer

        Equivalent to GET$ in RM Basic

        Returns:
            str
        
        """

        # If the buffer isn't empty pop the last char
        # and return it, otherwise return empty str
        if len(self.nimbus.keyboard_buffer) > 0:
            return self.nimbus.keyboard_buffer.pop(0)
        else:
            return ''        


    def input(self, prompt):
        """Collects keyboard input until user presses ENTER then returns the input as a string

        Args:
            prompt (str): Message to be printed

        Returns:
            str
        
        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # Validata params
        assert isinstance(prompt, str), "The value of prompt must be a string, not {}".format(type(prompt))

        # Get max columns for this screen mode
        if self.nimbus.screen_mode == 'lo':
            max_columns = 40
        if self.nimbus.screen_mode == 'hi':
            max_columns = 80
        # Flush buffer, reset enter + delete flag
        self.flush()
        self.nimbus.enter_was_pressed = False
        self.nimbus.backspace_was_pressed = False
        # Print the prompt and get start cursor position
        self.put(prompt)
        # Collect response in this string:
        response = ''
        # Collect and echo chars from buffer until enter was pressed
        while not self.nimbus.enter_was_pressed and self.nimbus.running:
            new_char = self.gets()
            response += new_char
            self.put(new_char)
            # Handle delete
            if self.nimbus.backspace_was_pressed and len(response) == 0:
                self.nimbus.backspace_was_pressed = False
            if self.nimbus.backspace_was_pressed and len(response) > 0:
                now_col, now_row = self.ask_curpos()
                response = response[:-1]
                # Move cursor left
                # If we're about to move off the left-hand side of the screen
                # it must be because we're on a line below where the input
                # started.  So, we need to move up one row and locate cursor
                # at right-hand side, wipe whatever char is there, then re-
                # position
                next_col = now_col - 1
                if next_col == 0:
                    # Go up one row
                    next_col = max_columns
                    next_row = now_row - 1
                else:
                    # Go back one column
                    next_row = now_row
                # Wipe char in this location, reposition, and reset flag
                self.set_curpos((next_col, next_row))
                self.put(' ')
                self.set_curpos((next_col, next_row))
                self.nimbus.backspace_was_pressed = False
        # Enter was pressed, flush buffer and reset enter flag
        self.nimbus.enter_was_pressed = False
        self.flush()
        # Force carriage return by smashing the cursor off the screen
        col, row = self.ask_curpos()
        self.nimbus.cursor_position = (255, row)
        self.put('X')
        # Return string
        return response


    def plot(self, text, coord, size=1, brush=None, direction=0, font=None):
        """Plot text on the screen

        Args:
            text (str): The text to be plotted
            coord (tuple): The (x, y) position of the text
            size (int), optional: Font size. To elongate pass a tuple (x_size, y_size)
            brush (int), optional: Brush colour
            direction (int), optional: 0=normal, 1=-90deg, 2=180deg, 3=-270deg
            font (int), optional: 0 is the standard font, 1 is the other font

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # Validate params
        assert isinstance(text, str), "The value of text must be a string, not {}".format(type(str))
        assert isinstance(coord, tuple), "The value of coord must be a tuple, not {}".format(type(coord))
        assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
        for i in range(0, 2):
            assert isinstance(coord[i], int), "The values in coord {} must be integer, not {}".format(coord, type(coords[i]))      
        assert isinstance(size, (int, tuple)), "The value of size must be an integer or tuple, not {}".format(type(size))
        if isinstance(size, tuple):
            for i in range(0, 2):
                assert isinstance(size[i], int), "The values in size {} must be integer, not {}".format(size, type(size[i]))  
        assert isinstance(brush, (type(None), int)), "The value of brush must be None or an integer, not {}".format(type(brush))
        if brush is not None:
            assert is_valid_colour(self.nimbus, brush), "Brush colour {} is out-of-range for this screen mode".format(brush)
        assert isinstance(direction, int), "The value of direction must be an integer, not {}".format(type(direction))
        assert isinstance(font, (type(None), int)), "The value of font must be an integer, not {}".format(type(font))
        assert (font == 0 or font == 1 or font is None), "The value of font can be 0 or 1, not {}".format(font)

        # Handle brush colour
        if brush is None:
            brush = self.nimbus.brush_colour

        # Handle font
        if font is None:
            font = self.nimbus.plot_font

        # Create a temporary image of the plotted text
        plot_img_width = len(text) * 10
        plot_img = Image.new(
            'RGBA',
            (plot_img_width, 10), 
            (0, 0, 0, 1)
        )

        # Plot chars on plot_img
        x = 0
        for char in text:

            # return if shutdown detected
            if not self.nimbus.running:
                return

            # If out of extended ASCII range replace with space
            if ord(char) > 255:
                # It's out of range
                char = ' '
            # Get char image and recolour it
            char_img = self.nimbus.FONT_IMAGES[font][ord(char)]
            char_img = recolour(self.nimbus, char_img, (0, 0, 0), self.nimbus.COLOUR_TABLE[self.nimbus.runtime_colours[self.nimbus.screen_mode][brush]], has_alpha=True)
            # Plot char and increment x
            plot_img.paste(char_img, (x, 0), mask=char_img)
            x += 8
        
        # resize
        if isinstance(size, tuple):
            # tuple: extract x_size, y_size
            x_size, y_size = size
        else:
            x_size = size
            y_size = size
        new_size = (plot_img.size[0] * x_size, plot_img.size[1] * y_size)
        plot_img = plot_img.resize(new_size, resample=Image.NEAREST)
        
        # rotate
        for i in range(0, direction):
            plot_img = plot_img.transpose(Image.ROTATE_90)
        
        # rebuild screen and done
        self.nimbus.plonk_image_on_paper(plot_img, coord, transparent=True)


    def area(self, coord_list, brush=None):
        """Draw a filled polygon

        Args:
            coord_list (list): A list of (x, y) tuples
            brush (int), optional: Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(coord_list, list), "coord_list should contain a list, not {}".format(type(coord_list))
        assert isinstance(brush, (type(None), int)), "The value of brush must be None or an integer, not {}".format(type(brush))
        assert is_valid_colour(self.nimbus, brush), "Brush colour {} is out-of-range for this screen mode".format(brush)
        for coord in coord_list:
            assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
            for i in range(0, 2):
                assert isinstance(coord[i], int), "The values in coord {} must be integer, not {}".format(coord, type(coord[i]))

        # if default brush value then get current brush colour
        if brush is None:
            brush = self.nimbus.brush_colour

        # correct coords
        for i in range(0, len(coord_list)):
            coord_list[i] = fix_coord(self.nimbus.SCREEN_MODES[self.nimbus.screen_mode], coord_list[i])

        # draw area
        draw = ImageDraw.Draw(self.nimbus.paper_image)
        rgb = self.nimbus.COLOUR_TABLE[self.nimbus.runtime_colours[self.nimbus.screen_mode][brush]]
        draw.polygon(coord_list, outline=rgb, fill=rgb)


    def line(self, coord_list, brush=None):
        """Draw one or more connected straight lines

        Args:
            coord_list (list): A list of (x, y) tuples
            brush (int), optional: Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(coord_list, list), "coord_list should contain a list, not {}".format(type(coord_list))
        assert isinstance(brush, (type(None), int)), "The value of brush must be None or an integer, not {}".format(type(brush))
        assert is_valid_colour(self.nimbus, brush), "Brush colour {} is out-of-range for this screen mode".format(brush)
        for coord in coord_list:
            assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
            for i in range(0, 2):
                assert isinstance(coord[i], int), "The values in coord {} must be integer, not {}".format(coord, type(coord[i])) 

        # if default brush value then get current brush colour
        if brush is None:
            brush = self.nimbus.brush_colour

        # correct coords
        for i in range(0, len(coord_list)):
            coord_list[i] = fix_coord(self.nimbus.SCREEN_MODES[self.nimbus.screen_mode], coord_list[i])

        # draw lines
        draw = ImageDraw.Draw(self.nimbus.paper_image)
        rgb = self.nimbus.COLOUR_TABLE[self.nimbus.runtime_colours[self.nimbus.screen_mode][brush]]
        draw.line(coord_list, fill=rgb)


    def circle(self, radius, coord_list, brush=None):
        """Draw one or more circles

        Args:
            radius (int): The radius of the circle
            coord_list (list): A list of (x, y) tuples
            brush (int), optional: Colour value (High-resolution: 0-3, low-resolution: 0-15)
        
        """

        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(radius, int), "radius must be an integer, not {}".format(type(radius))
        assert radius > 0, "radius must be greater than zero, not {}".format(radius)
        assert isinstance(coord_list, list), "coord_list should contain a list, not {}".format(type(coord_list))
        assert isinstance(brush, (type(None), int)), "The value of brush must be None or an integer, not {}".format(type(brush))
        assert is_valid_colour(self.nimbus, brush), "Brush colour {} is out-of-range for this screen mode".format(brush)
        for coord in coord_list:
            assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
            for i in range(0, 2):
                assert isinstance(coord[i], int), "The values in coord {} must be integer, not {}".format(coord, type(coord[i]))

        # if default brush value then get current brush colour
        if brush is None:
            brush = self.nimbus.brush_colour

        # draw cirtles
        draw = ImageDraw.Draw(self.nimbus.paper_image)
        rgb = self.nimbus.COLOUR_TABLE[self.nimbus.runtime_colours[self.nimbus.screen_mode][brush]]
        for coord in coord_list:

            # return if shutdown detected
            if not self.nimbus.running:
                return

            # define 'bounding box'
            r = radius
            x, y = coord
            box = [(x-r, y-r), (x+r, y+r)]
            draw.ellipse(box, outline=rgb, fill=rgb)


    def slice(self, radius, from_angle, to_angle, coord_list, brush=None):
        """Draw one or more pie slices

        Args:
            radius (int): The radius of the slice
            from_angle (int): The starting angle (degrees)
            to_angle (int): The finishing angle (degrees)
        
        """
        
        # return if shutdown detected
        if not self.nimbus.running:
            return

        # validate params
        assert isinstance(radius, int), "radius must be an integer, not {}".format(type(radius))
        assert radius > 0, "radius must be greater than zero, not {}".format(radius)
        assert isinstance(from_angle, int), "from_angle must be an integer, not {}".format(type(from_angle))
        assert isinstance(to_angle, int), "to_angle must be an integer, not {}".format(type(to_angle))
        assert from_angle >= 0 and from_angle <= 360, "from_angle must be between 0 and 360 degrees, not {}".format(from_angle)
        assert to_angle >=0 and to_angle <= 360, "to_angle must be between 0 and 360 degrees, not {}".format(to_angle)
        assert isinstance(coord_list, list), "coord_list should contain a list, not {}".format(type(coord_list))
        assert isinstance(brush, (type(None), int)), "The value of brush must be None or an integer, not {}".format(type(brush))
        assert is_valid_colour(self.nimbus, brush), "Brush colour {} is out-of-range for this screen mode".format(brush)
        for coord in coord_list:
            assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
            for i in range(0, 2):
                assert isinstance(coord[i], int), "The values in coord {} must be integer, not {}".format(coord, type(coord[i]))

        # if default brush value then get current brush colour
        if brush is None:
            brush = self.nimbus.brush_colour

        # draw slices      
        draw = ImageDraw.Draw(self.nimbus.paper_image)
        rgb = self.nimbus.COLOUR_TABLE[self.nimbus.runtime_colours[self.nimbus.screen_mode][brush]]
        for coord in coord_list:

            # return if shutdown detected
            if not self.nimbus.running:
                return

            # define 'bounding box'
            r = radius
            x, y = coord
            box = [(x-r, y-r), (x+r, y+r)]
            draw.pieslice(box, from_angle, to_angle, outline=rgb, fill=rgb)      