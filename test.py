import time
from nimbusinator.nimbus_pg import Nimbus

if __name__ == '__main__':
    nim = Nimbus(full_screen=True)
    nim.boot()
    time.sleep(5)
    nim.shutdown()