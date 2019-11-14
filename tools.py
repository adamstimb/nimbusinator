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

    Let's face it, OpenCV2 is a clusterfuck for getting things the
    wrong way round, and the drawing functions are no exception.  Pass
    you're coordinates into this function to "fix" them for use in any
    drawing functions.

    Args:
        screen_size (tuple): The screen size (width, height)
        coord (tuple): The x, y coordinate to fix (x, y)

    Returns:
        (tuple): I can't even put this in words...

    """
    
    return (coord[0], screen_size[1] - coord[1])
