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
            for offset in [0, 28, 56]:
                cmd.line([
                    (0+(brush*10)+offset, 0), 
                    (50+(brush*10)+offset, 50), 
                    (200+(brush*10)+offset, 0)
                    ], brush=brush)
        time.sleep(1)

def test_set_curpos_and_put(nim, cmd):
    for mode in [40, 80]:
        cmd.set_mode(mode)
        cmd.set_border(1)
        cmd.set_paper(2)
        cmd.set_curpos((1, 1))
        cmd.put('Hello')
        for i in range(1, 26):
            cmd.set_curpos((1, i))
            cmd.put("abcdefABCDEF 1234567890")
        big_test = ''
        cmd.set_pen(1)
        for i in range(0, 20):
            big_test += 'Iggle Piggle Iggle Onk ABCDEF abcdeg  12345 _ - 67890 %^$&#&$'
        cmd.set_curpos((7, 16))
        cmd.put(big_test)
        time.sleep(2)


if __name__ == '__main__': 
    nim = Nimbus(full_screen=False, debug=True, border_size=40)
    cmd = Command(nim)
    nim.boot(skip_loading_screen=True)
    cmd.set_mode(80)
    cmd.plonk_logo((0, 0))
    cmd.plonk_logo((-20, -20))
    cmd.plonk_logo((500, 100))
    cmd.plonk_logo((100, 100))
    cmd.plonk_logo((150, 230))
    time.sleep(1)
    cmd.plot("Hello!", (70, 70))
    cmd.plot("Bigger..?", (0, 150), size=2)
    cmd.plot("what is happening", (100, 100), size=2, brush=1)
    cmd.plot("Standing up!!!", (150, 0), size=2, direction=1, brush=2)
    time.sleep(3)
    cmd.set_mode(40)
    cmd.plonk_logo((5, 100))
    time.sleep(1)
    test_set_curpos_and_put(nim, cmd)
    test_set_border_low_res(nim, cmd)
    test_set_paper_low_res(nim, cmd)
    test_set_border_high_res(nim, cmd)
    test_set_paper_high_res(nim, cmd)
    test_line(nim, cmd)
    nim.shutdown()