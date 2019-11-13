# Nimbusinator

Didn't you dream of writing your own applications for the RM Nimbus back in the day?  Maybe you've got a Nimbus but it's so hopelessly obsolete you can't connect it to the internet or do anything more interesting than run Trains?  Did you get fed up with RM Basic and yet the mythical C compiler is nowhere to be found?  No chance of finding RM Pascal with it's super-sexy blue IDE is there?  Well, stuff the Nimbus!  And stuff Pascal, stuff C and stuff Basic!  This is the 21st century for crying out loud.  All you need is Nimbusinator.

Nimbusinator is a graphical user interface package for Python, accurately emulating the graphics and console drivers found in the fabled RM Nimbus PC186 SUB-BIOS and providing Pythonic controls that mimick the vocabulary of RM Basic.  It is _not_ an emulation of the RM Nimbus machine itself, nor does it contain any proprietary software or firmware naughtiness.  This means you can use all the computing power at your disposal beneath a user interface that predates the world-wide-web, acid house and even _Back to the Future Part 1_.  

## Installation

None as yet

## Quick-start

```python
import time
from nimbus import Nimbus
from command import Command

# Create a Nimbus object then create a Command object
# and bind it to the Nimbus object
nim = Nimbus()  
cmd = Command(nim)

nim.boot()          # Boot the Nimbus
cmd.set_mode(40)    # Low resolution mode
cmd.set_paper(1)    # Dark blue background
cmd.cls()           # Clear screen
# Display the Nimbus logo at the top
cmd.plonk_logo((80, 80))
# Display a message in cyan with shadowing
cmd.plot('Greetings from the', (25, 45), size=2, brush=0)
cmd.plot('Greetings from the', (26, 46), size=2, brush=13)
time.sleep(3)
nim.shutdown()      # Shut down the Nimbus 
```