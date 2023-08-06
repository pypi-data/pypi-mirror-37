import time, sys, random, code
from pyconio import *
from pyconio.constants import *

hidecur()
clrscr()
title("Game")

colorlist = [
    Red,
    Blue,
    Green,
    Yellow,
    Gray,
    LightGreen,
    LightRed,
    Cyan, 
    LightYellow,
]


def drawbox():  # generate random objects
    start_bch = time.time()
    x, y, xpos, ypos = [], [], [], []
    a, b, c, d = 1, 1, 1, 1

    while a <= 55:
        gotoxy(a, 1)
        puts("═")
        a += 1

    while b <= 55:
        gotoxy(b, 25)
        puts("═")
        b += 1

    while c <= 25:
        gotoxy(1, c)
        puts("║")
        c += 1

    while d <= 25:
        gotoxy(55, d)
        puts("║")
        d += 1

    gotoxy(55, 1)
    puts("╗")
    gotoxy(55, 25)
    puts("╝")
    gotoxy(1, 1)
    puts("╔")
    gotoxy(1, 25)
    puts("╚")

    for xi in range(2, 54):
        x.append(xi)
        for yi in range(2, 24):
            y.append(yi)
            random.seed(time.time())
            epochext = time.time()

            xrand = random.choice(x)
            yrand = random.choice(y)

            gotoxy(xrand, yrand)
            textcolor(random.choice(colorlist))
            puts("×")

           # yield xrand, yrand

    end_bch = time.time()
    return start_bch - end_bch


def charc():
    puts("*")
    normvideo()


def gameover():
    clrscr()
    normvideo()
    puts(BEL)
    print("Don't touch the walls!")
    sys.exit()

'''
def coord_dump():
    while 1:  # Dumping random objects coordinates.
        fl = open("posfl.log", 'w')
        apos = drawbox()

        for d in apos:
            fl.write(str(d))

        fl.close()
        break

'''
def drawboxW():
    dr = drawbox()
    gotoxy(0, 28)
    puts(dr)
    
def main():
    x = 27
    y = 12
    punt = 0

    #coord_dump()
    drawboxW()

    while 1:
        textcolor(LightWhite)
        gotoxy(0, 26)
        puts("X:%s Y:%s" % (x, y))
        gotoxy(0, 27)
        puts("Use WASD to move, r to regenerate, and x for exit.", "konniskatt 2018")

        textcolor(LightRed)
        gotoxy(x, y)
        puts("█")

        key = getch()
        gotoxy(x, y)
        puts(" ")  # Cleans gotoxy footprint

        if key == "w":
            y -= 1

        elif key == "a":
            x -= 1

        elif key == "s":
            y += 1

        elif key == "d":
            x += 1

        elif key == "r":
            clrscr()
            normvideo()
            #coord_dump()
            drawboxW()

        elif key == "x":
            showcur()
            normvideo()
            clrscr()
            sys.exit("")

        elif key == "m":
            gotoxy(0, 29)
            textcolor(White)
            
            try:
                exec(input("-> "))
            except:
                pass
            #code.interact(banner="-> ", local=locals())

        if x >= 55 or x <= 1 or y <= 1 or y >= 25 or x == 1:
            gameover()

        """
        if x > 55:
            x = 0
            y += 1
            gotoxy(x, y)
         """



main()
