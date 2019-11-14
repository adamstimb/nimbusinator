# RM Nimbus colour tables.  

# The Nimbus provided 16 colours in low-resolution mode.  In high
# resolution mode only 4 colours were available, although you can
# assign any of the 16 colours to the 4 slots in the palette.

# The full colour table here is also used in low-res mode.  The key
# is the Nimbus colour number and the value is the BGR composition.
colour_table = {
    #     B    G    R
    0:  [  0,   0,   0],    # black
    1:  [102,   0,   0],    # dark blue
    2:  [  0,   0, 102],    # dark red
    3:  [ 76,   0, 153],    # purple
    4:  [  0,  51,   0],    # dark green
    5:  [102, 102,   0],    # dark cyan
    6:  [  0,  25,  51],    # brown
    7:  [128, 128, 128],    # light grey
    8:  [ 64,  64,  64],    # dark grey
    9:  [255, 128,   0],    # light blue
    10: [  0,   0, 255],    # light red
    11: [255,  51, 255],    # light purple
    12: [  0, 255,   0],    # light green
    13: [255, 255,  51],    # light cyan
    14: [  0, 255, 255],    # yellow
    15: [255, 255, 255]     # white
}

# High-res mode has it's own colour table.  This is the default
# palette for high-res mode but, just like on the Nimbus, any
# 16 colours can be assigned to the 4 slots at runtime.
high_res_colour_table = {
    0: 1,                   # dark blue
    1: 4,                   # dark green
    2: 10,                  # light red
    3: 15                   # white
}