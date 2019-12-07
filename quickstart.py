from nimbusinator.nimbus import Nimbus
from nimbusinator.command import Command

if __name__ == '__main__': 
    # Create and bind nimbusinator objects:
    nim = Nimbus()
    cmd = Command(nim)
    nim.boot()          # Boot the Nimbus
    cmd.set_mode(40)    # Low resolution mode
    cmd.set_border(1)   # Dark blue border
    cmd.set_paper(9)    # Light blue paper
    cmd.cls()           # Clear screen
    cmd.plonk_logo((8, 110))    # Show Nimbus logo
    # Display a message in cyan with shadowing
    cmd.plot('Greetings!!!', (65, 155), size=2, brush=0)
    cmd.plot('Greetings!!!', (66, 156), size=2, brush=13)
    # Wait 5 seconds then shutdown
    nim.sleep(5)
    nim.shutdown()