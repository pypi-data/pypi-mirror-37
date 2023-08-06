# This file is part of the PyConio module.
# Copyright 2018 - konniskatt
# Windows colors convertions 

def _winfore2back(a):
    _color_code = {
        0: 0,  # Black
        1: 16,  # Blue
        2: 32,  # Green
        4: 64,  # Red
        6: 96,  # Yellow
        3: 48,  # Cyan
        5: 80,  # Magenta
        7: 112,  # White
        8: 128,  # Gray
        12: 192,  # Light Red
        10: 160,  # Light Green
        9: 144,  # Light Blue
        15: 240,  # Light White
        14: 224,  # Light Yellow
        11: 176,  # Light Cyan
        13: 208,  # Light Magenta
        # ?:368, #Light Gray
    }

    return _color_code[a]


def _winback2fore(a):
    _color_code = {
        0: 0,  # Black
        16: 1,  # Blue
        32: 2,  # Green
        64: 4,  # Red
        96: 6,  # Yellow
        48: 3,  # Cyan
        80: 5,  # Magenta
        112: 7,  # White
        128: 8,  # Gray
        192: 12,  # Light Red
        160: 10,  # Light Green
        144: 9,  # Light Blue
        240: 15,  # Light White
        224: 14,  # Light Yellow
        176: 11,  # Light Cyan
        208: 12,  # Light Magenta
        # ?:368, #Light Gray
    }

    return _color_code[a]
