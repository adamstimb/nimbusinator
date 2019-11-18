import inspect
import sys
import numpy as np
import cv2


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


def ceildiv(a, b):
    return -(-a // b)

def font_image_selecta(font_img, ascii_code):
    """Get the image of a character from a PNG

    Enter an ASCII code and a transparent PNG image of the char is returned.
    Codes < 33 and delete char (127) just return a space.

    Args:
        ascii_code (int): The ASCII code (extended) of the character

    Returns:
        (PIL image): The transparent image of the character
    
    """

    x_pos_table = {
        #col, #x
        1: 0,
        2: 10,
        3: 21,
        4: 32,
        5: 43,
        6: 54,
        7: 65,
        8: 76,
        9: 86,
        10: 97,
        11: 108,
        12: 120,
        13: 131,
        14: 142,
        15: 152,
        16: 163,
        17: 174,
        18: 186,
        19: 196,
        20: 207,
        21: 218,
        22: 229,
        23: 240,
        24: 251,
        25: 261,
        26: 272,
        27: 283,
        28: 294,
        29: 305,
        30: 316
    }

    y_pos_table = {
        #row, y
        1: 0,
        2: 11,
        3: 21,
        4: 32,
        5: 42,
        6: 52,
        7: 62,
        8: 74
    }

    # On our Nimbus char map PNGs delete (127) is just a blank space, so if we
    # receive any < 33 control chars, set the ascii value to 127 so a space is
    # also returned in those cases.
    if ascii_code < 33:
        ascii_code = 127
    # Calculate the row and column position of the char on the character map PNG
    map_number = ascii_code - 32    # codes < 33 are not on the map (unprintable)
    row = ceildiv(map_number, 30)
    column = map_number - (30 * (row - 1))
    print('ascii_code={} map_number={} column={}, row{}'.format(ascii_code, map_number, column, row))
    # Calculate corners of box around the char
    x1 = x_pos_table[column] + 1
    y1 = y_pos_table[row]
    x2 = x1 + 9
    y2 = y1 + 9
    # Chop out the char and return as PIL
    char_img = font_img[y1:y2, x1:x2]
    #print('x1, y1 = {}, {}; x2, y2 = {}, {}'.format(x1, y1, x2, y2))
    return char_img


def plonk_image(nimbus, background, smaller, coord, custom_size=None):
    """Overlay a smaller image on a background image

    This function also handles cases where the smaller image will overhang
    the screen margins.

    Args:
        background (PIL image): The background image
        smaller (PIL image): The smaller image to overlay on the background
        coord (tuple): The (x, y) position of the bottom left corner of the smaller image
        custom_size (tuple): Override actual screen size

    Returns:
        (PIL image): The modified background image

    """

    # Handle screen width or max width:
    if custom_size is None:
        screen_size = nimbus.screen_size
    else:
        screen_size = custom_size

    # Convert coordinates to PIL offsets
    x_offset = coord[0]
    y_offset = screen_size[1] - coord[1]
    bkg_img = background.copy()
    # Will part of the image be off screen?  Crop it and update offsets if so.
    x = coord[0]
    y = coord[1]
    if x < 0:
        # Image overhangs left-hand side so crop left-hand side of image and set x_offset to 0
        smaller = smaller[:, (-1 * x):, :]
        x_offset = 0
    if y < 0:
        # Image overhangs bottom so crop bottom of image
        # (because PIL has y upside down)
        smaller = smaller[:-((-1*y)), :, :]
        y_offset = screen_size[1]
    if x + smaller.shape[1] > screen_size[0]:
        # right-hand side of image overhangs left-hand side of screen so
        # crop right-hand side of image
        overhanging_length = (x + smaller.shape[1]) - screen_size[0]
        smaller = smaller[:, :-overhanging_length, :]
    if y + smaller.shape[0] > screen_size[1]:
        # top of image overhangs top of screen so crop top of image
        overhanging_length = (y + smaller.shape[0]) - screen_size[1]
        smaller = smaller[overhanging_length:, :, :]
    if x > screen_size[0] or y > screen_size[1]:
        # Image is beyond right-hand side or top so is invisble --> plot nothing
        return bkg_img
    # Overlay the smaller image and return
    bkg_img[y_offset-smaller.shape[0]:y_offset, x_offset:x_offset+smaller.shape[1]] = smaller
    return bkg_img


def colour_char(nimbus, colour, char_img):
    """Colourise a char image (black background, white char)

    Args:
        colour (int): Nimbus colour code

    Returns:
        (PIL image): Colourised char image

    """

    char_img_colourised = char_img.copy()
    white = np.array([255, 255, 255])
    mask = cv2.inRange(char_img, white, white)
    colour_bgr = colour_to_bgr(nimbus, colour)
    b = colour_bgr[0]
    g = colour_bgr[1]
    r = colour_bgr[2]
    char_img_colourised[mask>0] = (b, g, r)
    return char_img_colourised

def plonk_transparent_image(nimbus, background, smaller, coords, is_black=False):
    """Overlay a smaller image on a background with black as transparent

    Args:
        background (PIL image): The background image
        smaller (PIL image): The smaller image to overlay on the background (black=transparent)
        coord (tuple): The (x, y) position of the bottom left corner of the smaller image
        is_black (bool): Temporary workaround
    
    Returns:
        (PIL image): The modified background
    
    """

    # Make an overlay    
    overlay = np.zeros((nimbus.screen_size[1]+1, nimbus.screen_size[0]+1, 3), dtype=np.uint8)
    overlay = plonk_image(nimbus, overlay, smaller, coords)
    
    # Create mask
    gray = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY).astype(np.int32)
    gray = np.multiply(gray, 255).clip(max=255).astype(np.uint8)
    mask = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Cast images to signed int32 so we can go negative
    background = background.astype(np.int32)

    # Subtract the mask  from background
    subtracted = np.subtract(background, mask)

    # Set negatives to zero and recast back to uint8
    subtracted = np.clip(subtracted, 0, 255).astype(np.uint8)

    if is_black:
        message('return subtracted')
        return subtracted
    else:
        return np.add(subtracted, overlay)