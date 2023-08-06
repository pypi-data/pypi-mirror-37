#!/usr/bin/env python3
# -*- coding: <utf-8> -*-
# pyconio module v1.0.2a
# Cross-platform Python Console I/O
# Copyright 2018 - konniskatt


#- konniskatt
#-(cpypasjlgo)


__version__ = "1.0.2"
__author__ = "konniskatt"
__license__ = "GNU GPL v2"
__name__ = "pyconio"

import os
import sys

Black = "30"
Gray = "90"
Blue = "34"
Cyan = "36"
Green = "32"
Magenta = "35"
Red = "31"
Yellow = "33"
White = "37"

LightBlue = "94"
LightCyan = "96"
LightGreen = "92"
LightMagenta = "95"
LightRed = "91"
LightYellow = "93"
LightWhite = "97"

vXpos, vYpos = 1, 1

def _fore2back(var):
    _clrdict = {
        "30": "40",
        "31": "41",
        "32": "42",
        "33": "43",
        "34": "44",
        "35": "45",
        "36": "46",
        "37": "47",
        "90": "100",
        "91": "101",
        "92": "102",
        "93": "103",
        "94": "104",
        "95": "105",
        "96": "106",
        "97": "107",
    }

    return _clrdict[var]


"""
# legacy old code (f)
def _fore2back(s, a, b):
    index = s.find(a)
    if index == -1:
        return s
    return "".join((s[:index], b, s[index + 1:]))
"""

# abgcolor = _fore2back(Black)
# eabgcolor = 232
acolor = White
eacolor = 7


# Universal functions

def clrscr(mode="a"):
    if mode.lower() == "a":
        print("\x1b[2J")

    elif mode.lower() == "l":
        print("\x1b[2K")

    else:
        print("\x1b[2J")


def fflush():
    sys.stdin.flush()
    sys.stdout.flush()
    sys.stderr.flush()


def getchar():
    return sys.stdin.readline(1)


def kbhit():
    m = getch()
    if m is None:
        pass

    else:
        return True


def hidecur():
    puts("\x1b[?25l")


def gettermsz():
    x, y = os.get_terminal_size()[0], os.get_terminal_size()[1]
    return x, y


def gotoxy(x=0, y=0):
    puts("\x1b[%d;%df" % (y, x))
    global vXpos, vYpos
    vXpos, vYpos = x, y


def normvideo():
    puts("\x1b[;0m")


def puts(*objects, sep="", end="", flush=True):
    for i in objects:
        sys.stdout.write(str(i))
        sys.stdout.write(sep)

    sys.stdout.write(end)

    if flush:
        sys.stdout.flush()


def reversevideo():
    print("\x1b[7m")


def rgb_textcolor(r=0, g=0, b=0):
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
        raise RuntimeError("Supplied RGB code was: R:%s G:%s B:%s" % (r, g, b))
    else:
        puts("\x1b[38;2;%s;%s;%sm \x1b[0m" % (r, g, b))


def rgb_backgroundcolor(r=0, g=0, b=0):
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
        raise RuntimeError("Supplied RGB code was: R:%s G:%s B:%s" % (r, g, b))
    else:
        puts("\x1b[48;2;%s;%s;%sm \x1b[0m" % (r, g, b))


def showcur():
    puts("\x1b[?25h")


def textcolor(color, palette=4):
    if palette == 4:
        try:
            bgcol = abgcolor

        except NameError:
            puts("\x1b[%sm" % (color))

        else:
            puts("\x1b[;%s;%sm" % (color, bgcol))

        global acolor
        acolor = color

    elif palette == 8:
        try:
            bgcol = eabgcolor

        except NameError:
            puts("\x1b[;38;5;%sm" % (color))

        else:
            puts("\x1b[;38;5;%s;48;5;%sm" % (color, bgcol))

        global eacolor
        eacolor = color


def textbackground(bgcolor, palette=4):
    if palette == 4:
        try:
            bgcol = _fore2back(bgcolor)

        except NameError:
            print("\x1b[;%sm" % acolor)

        else:
            print("\x1b[;%s;%sm" % (acolor, bgcol))

        global abgcolor
        abgcolor = bgcol

    elif palette == 8:
        try:
            print("\x1b[;38;5;%s;48;5;%sm" % (eacolor, bgcolor))

        except:
            print("\x1b[;38;5;%sm" % bgcolor)

        global eabgcolor
        eabgcolor = bgcolor


def wherex():
    return vXpos


def wherey():
    return vYpos


def wherexy():
    return (vXpos, vYpos)


if os.name == "posix":

    # The reason why theses libraries are exported here,
    # is because are only available on Posix systems

    import tty
    import termios


    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())

        ch = sys.stdin.read(1)

        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


    def getche():
        ch = getch()
        print(ch)
        return ch


    def movcur_up(t=0):
        puts("\x1b[%dA" % t)


    def movcur_dw(t=0):
        puts("\x1b[%dB" % t)


    def movcur_lf(t=0):
        puts("\x1b[%dD" % t)


    def movcur_rg(t=0):
        puts("\x1b[%dC" % t)


    def pause(msg="Press any key to continue . . . "):
        puts(msg)
        getch()


    def title(titlestr):
        command = 'echo "\x1b]0;"' + titlestr + '\x1b'
        os.system(command)


# PyConio NT specific functions
elif os.name == "nt":  # os.name == "nt" and sys.getwindowsversion().major < 10:

    import ctypes
    import msvcrt


    def getch():
        return msvcrt.getwch()


    def getche():
        ch = msvcrt.getwch()
        print(ch)
        return ch


    def pause(msg="Press any key to continue . . . "):
        puts(msg)
        getch()


    def title(titlestr):
        ctypes.windll.kernel32.SetConsoleTitleW(titlestr)

import atexit


def _exithandle():
    normvideo()
    if os.name == "nt":
        """
        # should i?
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 1)
        """


atexit.register(_exithandle)  # Resets video before exiting.
