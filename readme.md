# Nimbusinator

RM Nimbus SUB-BIOS Emulator for Python

Did you ever dream of writing your own applications for the RM Nimbus?  Maybe you're lucky enough to own a working Nimbus but it's so hopelessly obsolete you can't connect it to the internet or do anything more interesting than run Trains?  Been there and done that with RM Basic?  Wanted to try the mythical C compiler but it's nowhere to be found?  Do not despair.  All you need is Nimbusinator and some basic Python skillz.

Nimbusinator is a graphical user interface for Python, emulating the graphics and console drivers found in the fabled RM Nimbus SUB-BIOS and providing Pythonic controls that mimick the vocabulary of RM Basic.  It is _not_ an emulation of the RM Nimbus machine itself.  This means you can use all the 21st century computing power at your disposal, and conceal it beneath a 16-bit user interface style that predates Milli Vanilli, Kylie and Jason, and the word-wide-web.

## Installation

None as yet

## Quick-start

```python
import time
from nimbusinator import Nimbus, Command

if __name__ == '__main__':
    nim = Nimbus()      # Create a Nimbus object
    cmd = Command(nim)  # Create Command object and bind it
    nim.boot()          # Boot the Nimbus
    cmd.set_mode(40)    # Low resolution mode
    cmd.set_paper(1)    # Dark blue background
    cmd.cls()           # Clear screen
    cmd.plonk_logo((80, 80))    # Show Nimbus logo
    # Display a message in cyan with shadowing
    cmd.plot('Greetings from the', (25, 45), size=2, brush=0)
    cmd.plot('Greetings from the', (26, 46), size=2, brush=13)
    # Wait 3 secs then shutdown
    time.sleep(3)
    nim.shutdown()
```

## Useful links

- [Center for Computing History](http://www.computinghistory.org.uk/) - original RM Nimbus manuals and technical data
- [The Nimbus Museum](https://thenimbus.co.uk/) - online museum that looks like the Welcome Disk!
- [mame](https://www.mamedev.org/) - comprehensive retro computer emulation project