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
    cmd.set_mode(80)
    cmd.set_curpos((1, 1))
    cmd.put(5)
    cmd.put('Hello')
    cmd.set_curpos((40, 12))
    cmd.put('Owner of a loney heart much better than a owner of a broken heart')
    big_test = ''
    for i in range(0, 20):
        big_test += 'Owner of a loney heart much better than a owner of a broken heart'
    cmd.set_curpos((1, 16))
    cmd.put(big_test)
    time.sleep(5)

if __name__ == '__main__': 
    nim = Nimbus(zoom=3, full_screen=True, debug=True)
    cmd = Command(nim)
    nim.boot(skip_loading_screen=True)
    test_set_curpos_and_put(nim, cmd)
    test_set_border_low_res(nim, cmd)
    test_set_paper_low_res(nim, cmd)
    test_set_border_high_res(nim, cmd)
    test_set_paper_high_res(nim, cmd)
    test_line(nim, cmd)
    nim.shutdown()