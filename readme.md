# ![Nimbusinator](nimbusinator.png)

RM Nimbus GUI for Python

## About

Nimbusinator is a graphical user-interface package for Python that mimicks the graphics and text drivers of the RM Nimbus PC186.  It is _not_ an emulation of the Nimbus itself.  This means you get the best of both worlds:  Cutting-edge Python computing power, beautifully presented in up to 16 colours!

## Usage

To implement a Nimbus user interface all you need to do is import the `Nimbus` and `Command` classes, like this:

```python
from nimbusinator import Nimbus, Command
```

Then create one object of each, and bind the `Command` object to the `Nimbus` object:

```python
nim = Nimbus()
cmd = Command(nim)
```

To display the screen, call the `boot` method on the `Nimbus` object.  By default, you'll see the famous blue "Welcome Screen" before control is released back to your program.  To skip the Welcome Screen simply pass the argument `skip_welcome_screen=True` when calling `boot`, like this:

```python
# Boot the Nimbus with Welcome Screen
nim.boot()
# Boot the Nimbus without Welcome Screen  
nim.boot(skip_welcome_screen=True)
```

Note that the original Welcome Screen reported the memory status of the computer (in kilobytes!), alongside the RM firmware version and machine serial number.  Nimbusinator also displays memory status (but in units of Megabytes) and uses your Python version as the firmware version and your OS release number as the serial number.  It also uses information from your runtime environment to simulate a short DOS-like boot sequence before finally releasing control back to your application.  All the while you can enjoy the dulcet tones of an imaginary floppy drive.

To bring the Nimbus programming experience into the 21st century, the API - although Pythonic - has been modelled on the syntax of RM Basic.  For example, in RM Basic to write a greeting in big, red letters in the bottom-left corner of the screen you would use the `PLOT` command:

```basic
PLOT "Hi kittens!", 10, 10 BRUSH 2 SIZE 4
```

And in Python with Nimbusinator you can write the same instruction like this:

```python
cmd.plot('Hi kittens!', (10, 10), brush=2, size=4)
```

It is recommended to read the RM Basic manual to get familiar with the original commands and how graphics and text were handled on the Nimbus (see links below).

To cleanly exit your application, call the `shutdown` method on the `Nimbus` object:

```python
# Always do this before your app quits:
nim.shutdown()
```

## Installation

```bash
# Linux users first need to install libasound2:
sudo apt-get install -y python3-dev libasound2-dev

# Everyone else go straight to:
pip install nimbusinator
```

## Quick-start

```python
import time
from nimbusinator import Nimbus, Command

if __name__ == '__main__': 
    # Create and bind nimbusinator objects:
    nim = Nimbus()
    cmd = Command(nim)
    nim.boot()          # Boot the Nimbus
    cmd.set_mode(40)    # Low resolution mode
    cmd.set_border(1)   # Dark blue border
    cmd.set_paper(9)    # Light blue paper
    cmd.cls()           # Clear screen
    cmd.plonk_logo((10, 120))    # Show Nimbus logo
    # Display a message in cyan with shadowing
    cmd.plot('Greetings from', (30, 155), size=2, brush=0)
    cmd.plot('Greetings from', (31, 156), size=2, brush=13)
    cmd.plot('(not really)', (110, 80), brush=14)
    # Wait 5 seconds then shutdown
    time.sleep(5)
    nim.shutdown()
```

## Links

- [Center for Computing History](http://www.computinghistory.org.uk/) - original RM Nimbus manuals and technical data
- [The Nimbus Museum](https://thenimbus.co.uk/) - online museum that looks like the Welcome Disk!
- [mame](https://www.mamedev.org/) - comprehensive retro computer emulation project
- [Freesound pack: Floppy disk drive](https://freesound.org/people/MrAuralization/packs/15891/) - source of the floppy drive sounds
- [Ironstone Innovation](https://ironstoneinnovation.eu) - what I do for a living