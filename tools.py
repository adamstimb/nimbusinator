import inspect
import sys

logo = """

     _  ___       __            _           __          
    / |/ (_)_ _  / /  __ _____ (_)__  ___ _/ /____  ____
   /    / /  ' \/ _ \/ // (_-</ / _ \/ _ `/ __/ _ \/ __/
  /_/|_/_/_/_/_/_.__/\_,_/___/_/_//_/\_,_/\__/\___/_/   
                                                      
  RM Nimbus SUB-BIOS Emulator for Python
                                            
"""

def message(text):
    caller = inspect.stack()[1][3]
    print('[nimbusinator] {}: {}'.format(caller, text))

def fatal(nim):
    message('Fatal error')
    nim.shutdown()
    sys.exit()

def is_valid_colour(nimbus, colour):
    # validate low-res colour
    if nimbus.screen_size == (320, 250):
        if colour >= 0 and colour <= 15:
            return colour
        else:
            message('{} is not a valid choice since in low-resolution mode only values between 0 and 15 are accepted'.format(colour))
            fatal(nimbus)
    # validate high-res colour
    if nimbus.screen_size == (640, 250):
        if colour >= 0 and colour <= 3:
            return colour
        else:
            message('{} is not a valid choice since in high-resolution mode only values between 0 and 3 are accepted'.format(colour))
            fatal(nimbus)

def colour_to_bgr(nimbus, colour):
    # low-res colour
    if nimbus.screen_size == (320, 250):
        return nimbus.colour_table[colour]
    # high-res colour
    if nimbus.screen_size == (640, 250):
        return nimbus.colour_table[nimbus.high_res_colour_table[colour]]

def fix_coord(screen_size, coord):
    return (coord[0], screen_size[1] - coord[1])
