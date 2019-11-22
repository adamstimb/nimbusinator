import time
from nimbusinator import Nimbus, Command

if __name__ == '__main__': 
    nim = Nimbus(full_screen=False)
    cmd = Command(nim)
    nim.boot(skip_welcome_screen=False)
    cmd.set_mode(40)
    cmd.set_cursor(True)
    quest = cmd.input('What is your quest? ')
    print(quest)
    time.sleep(5)
    nim.shutdown()