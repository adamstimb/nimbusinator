import time
from nimbusinator import Nimbus, Command

if __name__ == '__main__': 
    nim = Nimbus()
    cmd = Command(nim)
    nim.boot()          # Boot the Nimbus
    cmd.set_mode(40)    # Low resolution mode
    cmd.set_border(1)   # Dark blue border
    cmd.set_paper(9)    # Light blue paper
    cmd.cls()           # Clear screen
    cmd.plonk_logo((10, 110))    # Show Nimbus logo
    # Display a message in cyan with shadowing
    cmd.plot('Greetings from', (40, 155), size=2, brush=0)
    cmd.plot('Greetings from', (41, 156), size=2, brush=13)
    cmd.plot('(well, sort of)', (100, 80), brush=14)
    # Wait 5 seconds then shutdown
    time.sleep(5)
    nim.shutdown()