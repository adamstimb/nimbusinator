import time
from nimbus import Nimbus
from command import Command

nim = Nimbus(zoom=3, full_screen=True)
cmd = Command(nim)
nim.boot(skip_loading_screen=True)
cmd.set_mode(40)
cmd.set_paper(15)
time.sleep(2)
cmd.cls()
time.sleep(3)
nim.shutdown()