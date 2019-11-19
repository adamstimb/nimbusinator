import time
import random
from nimbusinator import Nimbus, Command

def test_set_border_low_res(nim, cmd):
    cmd.set_mode(40)
    for i in range(0, 16):
        cmd.set_border(i)
        time.sleep(0.1)

def test_set_paper_low_res(nim, cmd):
    cmd.set_mode(40)
    for i in range(0, 16):
        cmd.set_paper(i)
        cmd.cls()
        time.sleep(0.1)

def test_set_border_high_res(nim, cmd):
    cmd.set_mode(80)
    for i in range(0, 4):
        cmd.set_border(i)
        time.sleep(0.1)

def test_set_paper_high_res(nim, cmd):
    cmd.set_mode(80)
    for i in range(0, 4):
        cmd.set_paper(i)
        cmd.cls()
        time.sleep(0.1)

def test_set_curpos_and_put(nim, cmd):
    for mode in [40, 80]:
        cmd.set_mode(mode)
        cmd.set_border(1)
        cmd.set_paper(2)
        cmd.set_pen(0)
        cmd.set_curpos((1, 1))
        cmd.put('Hello')
        for i in range(3, 26):
            cmd.set_curpos((1, i))
            cmd.put("The Ace of Spades 1234567890 !@#$%^&*()_+")
            cmd.set_charset(random.randint(0, 1))
        big_test = ''
        cmd.set_pen(1)
        for i in range(0, 20):
            big_test += 'Double up or quits, double stakes or splits, the Ace of Spades, the Ace of Spades. '
            cmd.set_charset(random.randint(0, 1))
        cmd.set_curpos((7, 16))
        cmd.put(big_test)
        time.sleep(2)

def test_plonk_logo(nim, cmd):
    cmd.set_mode(80)
    for i in range(0, 5000): 
        x = random.randint(0, 650)
        y = random.randint(0, 250)
        cmd.plonk_logo((x, y))
    cmd.set_mode(40)
    for i in range(0, 5000): 
        x = random.randint(0, 350)
        y = random.randint(0, 250)
        cmd.plonk_logo((x, y))

def test_plot(nim, cmd):
    cmd.set_mode(80)
    for i in range(0, 1000):
        x = random.randint(0, 650)
        y = random.randint(0, 250)
        direction = random.randint(0, 3)
        x_size = random.randint(1, 5)
        y_size = random.randint(1, 5)
        brush = random.randint(0, 3)
        font = random.randint(0, 1)
        cmd.plot("Farts!", (x, y), size=(x_size, y_size), brush=brush, direction=direction, font=font)
    time.sleep(1)
    cmd.set_mode(40)
    for i in range(0, 2000):
        x = random.randint(0, 350)
        y = random.randint(0, 250)
        direction = random.randint(0, 3)
        x_size = random.randint(1, 3)
        y_size = random.randint(1, 3)
        brush = random.randint(0, 15)
        font = random.randint(0, 1)
        cmd.plot("PANTS!!!", (x, y), size=(x_size, y_size), brush=brush, direction=direction, font=font)
    time.sleep(1)

def test_area(nim, cmd):
    cmd.set_mode(40)
    for i in range(0, 2000):
        x1 = 0 + random.randint(-10, 10)
        y1 = 0 + random.randint(-10, 10)
        x2 = 150 + random.randint(-10, 10)
        y2 = 250 + random.randint(-10, 10)
        x3 = 300 + random.randint(-10, 10)
        y3 = 0 + random.randint(-10, 10)
        brush = random.randint(0, 15)
        cmd.area([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], brush=brush)
    time.sleep(1)
    cmd.set_mode(80)
    for i in range(0, 2000):
        x1 = 0 + random.randint(-10, 10)
        y1 = 0 + random.randint(-10, 10)
        x2 = 325 + random.randint(-10, 10)
        y2 = 250 + random.randint(-10, 10)
        x3 = 650 + random.randint(-10, 10)
        y3 = 0 + random.randint(-10, 10)
        brush = random.randint(0, 3)
        cmd.area([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], brush=brush)
    time.sleep(1)

def test_line(nim, cmd):
    cmd.set_mode(40)
    for i in range(0, 2000):
        x1 = 0 + random.randint(-10, 10)
        y1 = 0 + random.randint(-10, 10)
        x2 = 150 + random.randint(-10, 10)
        y2 = 250 + random.randint(-10, 10)
        x3 = 300 + random.randint(-10, 10)
        y3 = 0 + random.randint(-10, 10)
        brush = random.randint(0, 15)
        cmd.line([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], brush=brush)
    time.sleep(1)
    cmd.set_mode(80)
    for i in range(0, 2000):
        x1 = 0 + random.randint(-10, 10)
        y1 = 0 + random.randint(-10, 10)
        x2 = 325 + random.randint(-10, 10)
        y2 = 250 + random.randint(-10, 10)
        x3 = 650 + random.randint(-10, 10)
        y3 = 0 + random.randint(-10, 10)
        brush = random.randint(0, 3)
        cmd.line([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], brush=brush)
    time.sleep(1)


if __name__ == '__main__': 
    nim = Nimbus(full_screen=True, debug=False, border_size=40)
    cmd = Command(nim)
    nim.boot(skip_welcome_screen=False)
    test_plonk_logo(nim, cmd)
    test_plot(nim, cmd)
    test_set_border_low_res(nim, cmd)
    test_set_paper_low_res(nim, cmd)
    test_set_border_high_res(nim, cmd)
    test_set_paper_high_res(nim, cmd)
    test_line(nim, cmd)
    test_area(nim, cmd)
    test_set_curpos_and_put(nim, cmd)
    time.sleep(2)
    nim.shutdown()