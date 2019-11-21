import time
from nimbus import Nimbus
from command import Command

if __name__ == '__main__': 
    nim = Nimbus(full_screen=False)
    cmd = Command(nim)
    nim.boot(skip_welcome_screen=True)
    cmd.set_cursor(True)
    quest = cmd.input('What is your quest? ')
    print(quest)
    time.sleep(5)
    nim.shutdown()