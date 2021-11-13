import sys
import time
from .colorain import *
from .engine import *
import random


class Snake(Sprite):
    def __init__(self, head_init, scene):
        if isinstance(head_init, tuple):
            head_init = Coord2D(*head_init)
        self.positions =  [head_init, Coord2D(head_init.x-1, head_init.y), Coord2D(head_init.x-2, head_init.y)]
        super().__init__(scene, self.positions)
    
    def draw(self):
        self.scene.edit_pixel(self.positions[0], Stx(f"<f=lg;b=b>-</>").parsed)
        for pos in self.positions[1:]:
            self.scene.edit_pixel(pos, Stx(f"<f=lr;b=y>{BLOCKS[2]}</>").parsed)

    def grow(self, direction):
        tail = self.positions[-1]
        if isinstance(direction, Coord2D):
            self.positions.append(direction)
        elif direction == 'VER':
            self.positions.append(Coord2D(tail.x, tail.y-1))
        elif direction == 'HOR':
            self.positions.append(Coord2D(tail.x-1, tail.y))
        elif direction in ['w', 'a', 's', 'd']:
            dx = -1 if direction=='d' else (1 if direction=='a' else 0)
            dy = -1 if direction=='s' else (1 if direction=='w' else 0)
            self.positions.append(Coord2D((tail.x + dx)%self.scene.width, (tail.y + dy)%self.scene.height))
        self.draw()

    def move(self, direction):
        if direction == Coord2D(0,0): 
            return self.positions[-1]
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
        return currpos_old


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
    scene.paint_pixel(apple_pos, 'lightred')
    
    return apple_pos

def update_scoreboard(prev_score, scoreboard):
    curr_score = prev_score + 1
    scoreboard_text = f"Score: {curr_score}"
    
    for i in range(len(scoreboard_text)):
        scoreboard.scene[0][i] = Stx(f"<f=b;b=gr>{scoreboard_text[i]}</>").parsed
    
    return curr_score, scoreboard


def key_to_coord(key):
    if key == 'w':
        return Coord2D(0,-1)
    elif key == 's':
        return Coord2D(0, 1)
    elif key == 'a':
        return Coord2D(-1,0)
    elif key == 'd':
        return Coord2D(1, 0)
    else:
        return Coord2D(0,0)


def snake_game(width = 20, height = 20, start_pos = (5,3), fps = 32):
    gamesc = Scene2D(width, height)
    
    scoreboard = Scene2D(width, 1)
    score, scoreboard = update_scoreboard(-1, scoreboard)

    snake = Snake(Coord2D(*start_pos), gamesc)
    
    apple_pos = spawn_apple(gamesc, snake)
    
    while True:
        scoreboard.render(reset=False)
        gamesc.render()
        key = getChar()

        if key == 'q':
            break
        else:
            tail_last_pos = snake.move(key_to_coord(key))
        
        if snake.positions[0] == apple_pos:
            score, scoreboard = update_scoreboard(score, scoreboard)
            snake.grow(tail_last_pos)
            apple_pos = spawn_apple(gamesc, snake)
        
        move_cursor(-1,-1)
        time.sleep(1/fps)
    
    return gamesc, snake