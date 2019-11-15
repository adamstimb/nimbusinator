import time
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

def test_line(nim, cmd):
    for mode in [40, 80]:
        cmd.set_mode(mode)
        for brush in range(1, 4):
            cmd.line([
                (0+(brush*5), 0), 
                (50+(brush*5), 50), 
                (200+(brush*5), 0)
                ], brush=brush)
        time.sleep(1)

def test_set_curpos_and_put(nim, cmd):
    for mode in [40, 80]:
        cmd.set_mode(mode)
        cmd.set_border(1)
        cmd.set_paper(2)
        cmd.set_pen(3)
        cmd.set_curpos((1, 1))
        cmd.put('Hello')
        for i in range(1, 26):
            cmd.set_curpos((1, i))
            cmd.put('Owner of a loney heart')
        big_test = ''
        for i in range(0, 20):
            big_test += 'Owner of a loney heart much better than a owner of a broken heart'
        cmd.set_curpos((1, 16))
        cmd.put(big_test)
        time.sleep(1)


if __name__ == '__main__': 
    nim = Nimbus(full_screen=True, debug=True)
    cmd = Command(nim)
    nim.boot(skip_loading_screen=True)
    test_set_curpos_and_put(nim, cmd)
    test_set_border_low_res(nim, cmd)
    test_set_paper_low_res(nim, cmd)
    test_set_border_high_res(nim, cmd)
    test_set_paper_high_res(nim, cmd)
    test_line(nim, cmd)
    nim.shutdown()