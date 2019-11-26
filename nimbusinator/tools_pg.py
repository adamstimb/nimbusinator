import inspect
from pygame import image


# Let there be ASCII art
logo = """                                        
 _____ _       _           _         _           
|   | |_|_____| |_ _ _ ___|_|___ ___| |_ ___ ___ 
| | | | |     | . | | |_ -| |   | .'|  _| . |  _|
|_|___|_|_|_|_|___|___|___|_|_|_|__,|_| |___|_|  
                                                  
                                               
RM Nimbus GUI for Python
                                            
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


def pil_to_pygame_image(PIL_image):
    """Convert PIL image to pygame surface

    Args:
        PIL_image (PIL.Image): The PIL image to be converted

    Returns:
        (pygame.image): The pygame image
    
    """

    return image.fromstring(PIL_image.tobytes(), PIL_image.size, PIL_image.mode)