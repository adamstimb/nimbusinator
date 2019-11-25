from nimbusinator.nimbus_pillow import Nimbus 
from nimbusinator.command import Command 

if __name__ == '__main__':
    nim = Nimbus(full_screen=False)
    cmd = Command(nim)
    nim.boot()
    nim.shutdown()
