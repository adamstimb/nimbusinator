import inspect
import sys


# Let there be ASCII art
logo = """

     _  ___       __            _           __          
    / |/ (_)_ _  / /  __ _____ (_)__  ___ _/ /____  ____
   /    / /  ' \/ _ \/ // (_-</ / _ \/ _ `/ __/ _ \/ __/
  /_/|_/_/_/_/_/_.__/\_,_/___/_/_//_/\_,_/\__/\___/_/   
                                                      
  RM Nimbus SUB-BIOS Emulator for Python
                                            
"""


def message(text):
    """Debug message

    Prints a message in the console including the name of the function
    that sent the message.

    Args:
        text (str): The text of the message

    """

    # Get name of function that sent the message
    caller = inspect.stack()[1][3]
    # Print the debug message
    print('[nimbusinator] {}: {}'.format(caller, text))


def fatal(nimbus):
    """Handle a fatal error

    If a fatal error is encountered shutdown the Nimbus :(

    Args:
        nimbus (Nimbus): The Nimbus object to shutdown
    
    """

    message('Fatal error')
    nimbus.shutdown()
    sys.exit()


def is_valid_colour(nimbus, colour):
    """Validate colour number

    If the colour number is out of range for the current screen
    mode a fatal error is yielded

    Args:
        nimbus (Nimbus): The Nimbus object
        colour (int): The colour number
    
    Returns:
        (int): The validated colour number

    """

    # validate low-res colour
    if nimbus.screen_size == (320, 250):
        if colour >= 0 and colour <= 15:
            # it's fine
            return colour
        else:
            # it's fatal
            message('{} is not a valid choice since in low-resolution mode only values between 0 and 15 are accepted'.format(colour))
            fatal(nimbus)
    
    # validate high-res colour
    if nimbus.screen_size == (640, 250):
        if colour >= 0 and colour <= 3:
            # it's fine
            return colour
        else:
            # it's fatal
            message('{} is not a valid choice since in high-resolution mode only values between 0 and 3 are accepted'.format(colour))
            fatal(nimbus)


def colour_to_bgr(nimbus, colour):
    """Convert a validated colour number to BGR composition

    Recommended to use is_valid_colour function first!

    Args:
        nimbus (Nimbus): The Nimbus object
        colour (int): The colour number
    
    Returns:
        (array): The BGR composition in an array, i.e. [B, G, R]
    
    """

    # low-res colour
    if nimbus.screen_size == (320, 250):
        return nimbus.colour_table[colour]
    
    # high-res colour
    if nimbus.screen_size == (640, 250):
        return nimbus.colour_table[nimbus.high_res_colour_table[colour]]


def fix_coord(screen_size, coord):
    """Fix coordinates for use in OpenCV's drawing functions

    PIL images have upside-down co-ordinates and it shafts me
    every goddamn time, so this function "deals with it"

    Args:
        screen_size (tuple): The screen size (width, height)
        coord (tuple): The x, y coordinate to fix (x, y)

    Returns:
        (tuple): The coordinates flipped upside-down

    """
    
    return (coord[0], screen_size[1] - coord[1])


def colrows_to_xy(screen_size, cursor_position):
    """Convert cursor position to x, y pixel position

    Args:
        screen_size (tuple): The screen size (width, height)
        cursor_position (tuple): The cursor position (row, col)

    Returns:
        (tuple): The screen position in pixels (x, y)
    
    """

    x = (8 * (cursor_position[0] - 1))
    y = screen_size[1] - (cursor_position[1] * 10)
    return (x, y)


def font_image_selecta(font_img, ascii_code):
    """Get the image of a character from a PNG

    Enter an ASCII code and a transparent PNG image of the char is returned.
    Codes < 33 and delete char (127) just return a space.

    Args:
        ascii_code (int): The ASCII code (extended) of the character

    Returns:
        (PIL image): The transparent image of the character
    
    """

    # On our Nimbus char map PNGs delete (127) is just a blank space, so if we
    # receive any < 33 control chars, set the ascii value to 127 so a space is
    # also returned in those cases.
    if ascii_code < 33:
        ascii_code = 127
    # Calculate the row and column position of the char on the character map PNG
    map_number = ascii_code - 32    # codes < 33 are not on the map (unprintable)
    row = (map_number // 31) + 1
    column = map_number - (30 * (row - 1))
    print('map_number={} column={}, row{}'.format(map_number, column, row))
    # Calculate corners of box around the char
    x1 = (column - 1) * 10
    y1 = (row - 1) * 10
    x2 = x1 + 10
    y2 = y1 + 10
    # Chop out the char and return as PIL
    char_img = font_img[x1:x2, y1:y2]
    print('x1, y1 = {}, {}; x2, y2 = {}, {}'.format(x1, y1, x2, y2))
    return char_img





if __name__ == '__main__':
    font_image_selecta(34)