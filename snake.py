import sys
import time
from .colorain import *
import random

Stx = StyledText

BLOCK_FULL = chr(9608)
BLOCK_THREEQTR = chr(9619)
BLOCK_HALF = chr(9618)
BLOCK_QTR = chr(9817)

BLOCKS = [BLOCK_FULL, BLOCK_THREEQTR, BLOCK_HALF, BLOCK_QTR]

def move_cursor(line, col):
    base = "\033["

    linedir = "A" if line < 0 else "B"
    coldir = "C" if col > 0 else "D"
    
    linecode = f"{base}{abs(line)}{linedir}"
    colcode = f"{base}{abs(col)}{coldir}"
    sys.stdout.write(linecode)
    sys.stdout.write(colcode) 


def getChar():
    try:
        # for Windows-based systems
        import msvcrt # If successful, we are on Windows
        return msvcrt.getch()

    except ImportError:
        # for POSIX-based systems (with termios & tty support)
        import tty, sys, termios  # raises ImportError if unsupported

        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

        return answer


class Scene2D:
    def __init__(self, width, height, colour = None):
        self.width = width
        self.height = height
        self.scene = [[BLOCKS[0]][:]*2*self.width for i in range(self.height)]
    
    def render(self, reset=True):
        sys.stdout.write('\n'.join([''.join(ln) for ln in self.scene]))
        if reset:
            move_cursor(-self.height+1, -2*self.width)
        else: print()

    def edit_pixel(self, x, y, newval):
        self.scene[y][2*x] = newval
        self.scene[y][2*x+1] = newval
    
    def reset_pixel(self, x, y):
        self.edit_pixel(x, y, BLOCKS[0])

    def paint_pixel(self, x, y, colour):
        self.edit_pixel(x, y, Stx(f"<{fgtokens[colour]}>{BLOCKS[0]}</>").parsed)


class Coord2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"{(self.x, self.y)}"
    
    def __add__(self, coord):
        return Coord2D(self.x + coord.x, self.y + coord.y)
    
    def __sub__(self, coord):
        return Coord2D(self.x - coord.x, self.y - coord.y)
    
    def __eq__(self, coord):
        return self.x == coord.x and self.y == coord.y

class Snake:
    def __init__(self, head_init, scene):
        self.length = 2
        self.positions =  [head_init, Coord2D(head_init.x-1, head_init.y)]
        self.scene = scene
        self.draw( )

    def draw(self):
        self.scene.edit_pixel(self.positions[0].x, self.positions[0].y, Stx(f"<f=lg;b=b>{BLOCKS[2]}</>").parsed)
        for pos in self.positions[1:]:
            self.scene.edit_pixel(pos.x, pos.y, Stx(f"<f=lr;b=y>{BLOCKS[2]}</>").parsed)
    
    def erase(self):
        for pos in self.positions:
            self.scene.reset_pixel(pos.x, pos.y)

    def grow(self, direction):
        tail = self.positions[-1]
        if direction == 'VER':
            self.positions.append(Coord2D(tail.x, tail.y-1))
        elif direction == 'HOR':
            self.positions.append(Coord2D(tail.x-1, tail.y))
        elif direction in ['w', 'a', 's', 'd']:
            dx = -1 if direction=='d' else (1 if direction=='a' else 0)
            dy = -1 if direction=='s' else (1 if direction=='w' else 0)
            self.positions.append(Coord2D((tail.x + dx)%self.scene.width, (tail.y + dy)%self.scene.height))
        self.draw()

    def translate(self, x, y):
        self.erase()
        for pos in self.positions:
            pos.x += x
            pos.y += y
        self.draw()

    def move(self, direction):
        self.erase()

        self.positions[0] += direction
        prevdir = direction

        for i in range(1,len(self.positions)):
            currpos = self.positions[i]
            currpos_old = Coord2D(currpos.x, currpos.y)
            prevpos = self.positions[i-1]
            
            if currpos.x == prevpos.x:
                if currpos.y > prevpos.y:
                    currpos.y -= 1 
                elif currpos.y < prevpos.y:
                    currpos.y += 1
                else:
                    pass
            elif currpos.y == prevpos.y:
                if currpos.x > prevpos.x:
                    currpos.x -= 1
                elif currpos.x < prevpos.x:
                    currpos.x += 1
                else:
                    pass
            else:
                if prevdir.x in [-1,1]:
                    if currpos.y < prevpos.y:
                        currpos.y += 1
                    elif currpos.y > prevpos.y:
                        currpos.y -= 1
                elif prevdir.y in [-1,1]:
                    if currpos.x < prevpos.x:
                        currpos.x += 1
                    elif currpos.x > prevpos.x:
                        currpos.x -= 1
            
            prevdir = currpos - currpos_old
        
        self.draw()
        # everything follows predecessor

def spawn_apple(scene, snake):
    width = scene.width
    height = scene.height
    ok = False
    while not ok:
        ok = True
        apple_x = random.randint(0, width-1)
        apple_y = random.randint(0, height-1)
        apple_pos = Coord2D(apple_x, apple_y)

        for pos in snake.positions:
            if pos == apple_pos:
                ok = False
    scene.paint_pixel(apple_pos.x, apple_pos.y, 'lightred')
    
    return apple_pos

def update_scoreboard(prev_score, scoreboard):
    curr_score = prev_score + 1
    scoreboard_text = f"Score: {curr_score}"
    
    for i in range(len(scoreboard_text)):
        scoreboard.scene[0][i] = Stx(f"<f=b;b=gr>{scoreboard_text[i]}</>").parsed
    
    return curr_score, scoreboard


def snake_game(width, height, start_pos, fps = 10):
    gamesc = Scene2D(width, height)
    
    scoreboard = Scene2D(width, 1)
    score, scoreboard = update_scoreboard(-1, scoreboard)

    snake = Snake(Coord2D(*start_pos), gamesc)
    
    apple_pos = spawn_apple(gamesc, snake)
    
    while True:
        scoreboard.render(reset=False)
        gamesc.render()
        key = getChar()

        if key == 'w':
            snake.move(Coord2D(0,-1))
        elif key == 's':
            snake.move(Coord2D(0, 1))
        elif key == 'a':
            snake.move(Coord2D(-1,0))
        elif key == 'd':
            snake.move(Coord2D(1, 0))
        elif key == 'q':
            break
        
        if snake.positions[0] == apple_pos:
            score, scoreboard = update_scoreboard(score, scoreboard)
            snake.grow(key)
            apple_pos = spawn_apple(gamesc, snake)
        
        move_cursor(-1,-1)
        time.sleep(1/fps)
    
    return gamesc, snake