import time
from nimbusinator import Nimbus, Command

if __name__ == '__main__': 
    nim = Nimbus(zoom=3, full_screen=True)
    cmd = Command(nim)
    nim.boot(skip_loading_screen=True)
    cmd.set_mode(80)
    cmd.set_paper(15)
    time.sleep(2)
    cmd.cls()
    cmd.set_mode(40)
    time.sleep(3)
    cmd.set_border(15)
    time.sleep(3)
    nim.shutdown()