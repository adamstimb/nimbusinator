from tools import message, fatal, is_valid_colour, colour_to_bgr, fix_coord
import numpy as np
import cv2



class Command:


    def __init__(self, nimbus):
        """Create a new Command object

        In creating an object of this class it must be bound to
        a pre-existing Nimbus object.

        Args:
            nimbus (Nimbus): The Nimbus object to bind to
        
        """
        if nimbus.debug:
            message('Initializing Nimbus commands')
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