import ctypes
import msvcrt
from .winconv import _winfore2back, _winback2fore

# ctypes Constants
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
LF_FACESIZE = 32
HANDLE = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

vXpos, vYpos = 1, 1

Black = 0
Blue = 1 
Green = 2  
Red = 4
Yellow = 6
Cyan = 3
Magenta = 5
White = 7
Gray = 8

# The followings colors are combinations using high tone
LightRed = 12
LightGreen = 10
LightBlue = 9
LightWhite = 15
LightYellow = 14
LightCyan = 11
LightMagenta = 13

abgcolor = Black
acolor = White
class CONSOLE_CURSOR_INFO(ctypes.Structure):
    _fields_ = [('dwSize', ctypes.c_int),
                ('bVisible', ctypes.c_int)]

class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short),
                    ("Y", ctypes.c_short)]


def clrscr(mode="a"): 
    os.system("cls")


def getch():
    return msvcrt.getwch()
    

def getche():
    ch = msvcrt.getwch()
    print(ch)
    return ch

    
def gotoxy(x=0, y=0): 
    ctypes.windll.kernel32.SetConsoleCursorPosition(HANDLE, COORD(x, y))
    global vXpos, vYpos
    vXpos, vYpos = x, y

    
def pause(msg="Press any key to continue . . . "):
    puts(prompt)
    getch()


def hidecur():
    cursorInfo = CONSOLE_CURSOR_INFO()
    cursorInfo.dwSize = 1
    cursorInfo.bVisible = 0
    ctypes.windll.kernel32.SetConsoleCursorInfo(HANDLE, ctypes.byref(cursorInfo))

    
def showcur():
    # This function is same as hidecur() function.
    # just the cursorInfo.bVisible changes to 1
    cursorInfo = CONSOLE_CURSOR_INFO()
    cursorInfo.dwSize = 1
    cursorInfo.bVisible = 1
    ctypes.windll.kernel32.SetConsoleCursorInfo(HANDLE, ctypes.byref(cursorInfo))
    
    
def normvideo(): 
    ctypes.windll.kernel32.SetConsoleTextAttribute(HANDLE, 7)


def reversevideo():
    ctypes.windll.kernel32.SetConsoleTextAttribute(HANDLE, _winback2fore(abgcolor) | _winfore2back(acolor))


def textcolor(color):
    bgcol = abgcolor
    ctypes.windll.kernel32.SetConsoleTextAttribute(HANDLE, color | bgcol)
    global acolor 
    acolor = color


def textbackground(bgcolor): 
    bgcol = _winfore2back(bgcolor)
    ctypes.windll.kernel32.SetConsoleTextAttribute(HANDLE, acolor | bgcol)
    global abgcolor
    abgcolor = bgcol

def title(titlestr): 
    ctypes.windll.kernel32.SetConsoleTitleW(titlestr)


import atexit
atexit.register(normvideo) # Resets video before exiting.
