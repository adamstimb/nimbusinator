import random
from nimbusinator.nimbus import Nimbus
from nimbusinator.command import Command


def test_slice(nim, cmd):
    for mode in [40, 80]:
        cmd.set_mode(mode)
        if mode == 80:
            x_max = 650
            colour_max = 3
        else:
            x_max = 320
            colour_max = 15
        for i in range(0, 5000): 
            x = random.randint(0, x_max)
            y = random.randint(0, 250)
            radius = random.randint(1, 50)
            from_angle = random.randint(1, 359)
            to_angle = 360 - random.randint(0, from_angle)
            brush = random.randint(0, colour_max)
            cmd.slice(radius, from_angle, to_angle, [(x, y)], brush=brush)
        nim.sleep(1)

def test_circle(nim, cmd):
    for mode in [40, 80]:
        cmd.set_mode(mode)
        if mode == 80:
            x_max = 650
            colour_max = 3
        else:
            x_max = 320
            colour_max = 15
        for i in range(0, 5000): 
            x = random.randint(0, x_max)
            y = random.randint(0, 250)
            radius = random.randint(1, 50)
            brush = random.randint(0, colour_max)
            cmd.circle(radius, [(x, y)], brush=brush)
        nim.sleep(1)

def test_put(nim, cmd):
    for charset in [0, 1]:
        cmd.set_charset(charset)
        for mode in [40, 80]:
            cmd.set_mode(mode)
            cmd.set_paper(1)
            cmd.cls()
            if mode == 40:
                repeats = 3
            else:
                repeats = 30
            for r in range(0, repeats + 1):
                if mode == 40:
                    max_pen_colour = 15
                else:
                    max_pen_colour = 3
                for i in range(0, max_pen_colour + 1):
                    cmd.set_pen(i)
                    cmd.set_paper(max_pen_colour - i)
                    cmd.put('blah blah BLAH  1234 *&*#@@_-')
            nim.sleep(1)

def test_print(nim, cmd):
    cmd.set_cursor(True)
    for charset in [0, 1]:
        cmd.set_charset(charset)
        for mode in [40, 80]:
            cmd.set_mode(mode)
            cmd.set_paper(1)
            cmd.cls()
            if mode == 40:
                repeats = 3
            else:
                repeats = 30
            for r in range(0, repeats + 1):
                if mode == 40:
                    max_pen_colour = 15
                else:
                    max_pen_colour = 3
                for i in range(0, max_pen_colour + 1):
                    cmd.set_pen(i)
                    cmd.set_paper(max_pen_colour - i)
                    cmd.print('What is your favourite colour?')
                    cmd.print('Blue -- no, red!')
            nim.sleep(1)
    cmd.set_cursor(False)

def test_input(nim, cmd):
    for mode in [40, 80]:
        cmd.set_mode(mode)
        cmd.set_cursor(True)
        test = cmd.input('What is your quest? ')
        cmd.print('{}, eh?  Fancy that.'.format(test))
        nim.sleep(1)
        cmd.set_cursor(False)

def test_set_border_low_res(nim, cmd):
    cmd.set_mode(40)
    for i in range(0, 16):
        cmd.set_border(i)
        nim.sleep(0.1)

def test_set_paper_low_res(nim, cmd):
    cmd.set_mode(40)
    for i in range(0, 16):
        cmd.set_paper(i)
        cmd.cls()
        nim.sleep(0.1)

def test_set_border_high_res(nim, cmd):
    cmd.set_mode(80)
    for i in range(0, 4):
        cmd.set_border(i)
        nim.sleep(0.1)

def test_set_paper_high_res(nim, cmd):
    cmd.set_mode(80)
    for i in range(0, 4):
        cmd.set_paper(i)
        cmd.cls()
        nim.sleep(0.1)

def test_plonk_logo(nim, cmd):
    cmd.set_mode(80)
    for i in range(0, 5000): 
        x = random.randint(0, 650)
        y = random.randint(0, 250)
        cmd.plonk_logo((x, y))
    nim.sleep(1)
    cmd.set_mode(40)
    for i in range(0, 10000): 
        x = random.randint(0, 350)
        y = random.randint(0, 250)
        cmd.plonk_logo((x, y))
    nim.sleep(1)

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
        cmd.plot("Farty pants?!", (x, y), size=(x_size, y_size), brush=brush, direction=direction, font=font)
    nim.sleep(1)
    cmd.set_mode(40)
    for i in range(0, 1000):
        x = random.randint(0, 350)
        y = random.randint(0, 250)
        direction = random.randint(0, 3)
        x_size = random.randint(1, 3)
        y_size = random.randint(1, 3)
        brush = random.randint(0, 15)
        font = random.randint(0, 1)
        cmd.plot("SmElLy Pants!!!", (x, y), size=(x_size, y_size), brush=brush, direction=direction, font=font)
    nim.sleep(1)

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
        cmd.area([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], brush=brush, scale=2)
    nim.sleep(1)
    cmd.set_mode(80)
    for i in range(0, 2000):
        x1 = 0 + random.randint(-10, 10)
        y1 = 0 + random.randint(-10, 10)
        x2 = 325 + random.randint(-10, 10)
        y2 = 250 + random.randint(-10, 10)
        x3 = 650 + random.randint(-10, 10)
        y3 = 0 + random.randint(-10, 10)
        brush = random.randint(0, 3)
        cmd.area([(x1, y1), (x2, y2), (x3, y3), (x1, y1)], brush=brush, scale=2)
    nim.sleep(1)

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
        cmd.line([(x1, y1), (x2, y2), (x3, y3), (x1, y1), (125, 125)], brush=brush)
    nim.sleep(1)
    cmd.set_mode(80)
    for i in range(0, 2000):
        x1 = 0 + random.randint(-10, 10)
        y1 = 0 + random.randint(-10, 10)
        x2 = 325 + random.randint(-10, 10)
        y2 = 250 + random.randint(-10, 10)
        x3 = 650 + random.randint(-10, 10)
        y3 = 0 + random.randint(-10, 10)
        brush = random.randint(0, 3)
        cmd.line([(x1, y1), (x2, y2), (x3, y3), (x1, y1), (125, 125)], brush=brush)
    nim.sleep(1)

if __name__ == '__main__':
    nim = Nimbus(full_screen=False)
    cmd = Command(nim)
    nim.boot(skip_welcome_screen=True)
    #test_slice(nim, cmd)
    #test_circle(nim, cmd)
    #test_line(nim, cmd)
    test_area(nim, cmd)
    test_plot(nim, cmd)
    test_input(nim, cmd)
    test_put(nim, cmd)
    test_print(nim, cmd)
    test_set_border_high_res(nim, cmd)
    test_set_border_low_res(nim, cmd)
    test_set_paper_high_res(nim, cmd)
    test_set_paper_low_res(nim, cmd)
    test_plonk_logo(nim, cmd)
    nim.shutdown()