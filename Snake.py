import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()

# snake charecter and attributes
class Snake(object):
    body = []
    turns = {}  # dictionary of snake head direction turns at pos (x, y)

    def __init__(self, pos, color):
        self.head = Cube(pos)
        self.body.append(self.head)
        self.color = color
        self.directionX = 1     # initially the snake is moving to the right
        self.directionY = 0
        self.vel = 3

    # calls the cube class to draw the snake body and head
    def draw(self, surface):
        for index, sCube in enumerate(self.body):
            if index == 0:
                sCube.draw(surface, True)     # This simply tells the program that this is the head of the snake
            else:
                sCube.draw(surface)

    # motion of the snake
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.directionX = -1
                    self.directionY = 0
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                elif keys[pygame.K_RIGHT]:
                    self.directionX = 1
                    self.directionY = 0
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                elif keys[pygame.K_UP]:
                    self.directionX = 0
                    self.directionY = -1
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                elif keys[pygame.K_DOWN]:
                    self.directionX = 0
                    self.directionY = 1
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]
                # self.turns tells the entire body of the snake where the head turned

        # gets the index and cube in the body list [self.body has the cube objects of the snake]
        for index, sCube in enumerate(self.body):
            posCube = sCube.pos[:]
            if posCube in self.turns:
                turn = self.turns[posCube]
                sCube.move(turn[0], turn[1])
                if index == len(self.body) - 1:
                    self.turns.pop(posCube)
            else:
                if sCube.directionX == -1 and sCube.pos[0] <= 0:
                    sCube.pos = (sCube.rows - 1, sCube.pos[1])
                elif sCube.directionX == 1 and sCube.pos[0] >= sCube.rows - 1:
                    sCube.pos = (0, sCube.pos[1])
                elif sCube.directionY == 1 and sCube.pos[1] >= sCube.rows - 1:
                    sCube.pos = (sCube.pos[0], 0)
                elif sCube.directionY == -1 and sCube.pos[1] <= 0:
                    sCube.pos = (sCube.pos[0], sCube.rows - 1)
                else:
                    sCube.move(sCube.directionX, sCube.directionY)    # else if no turns or edge of the screen the just keep moving in cureent dir

    # grow the snake from the tail every time it eats a snack
    def grow(self):
        # identify the tail of the snake the add to the position before that
        sTail = self.body[-1]
        dirx = sTail.directionX    # checks which direction the tail of the cube is currently moving so we know
        diry = sTail.directionY    # to grow from the top, bottom, left or right side of the snake body

        if  dirx == 1 and diry == 0:    # moving to the right
            self.body.append(Cube((sTail.pos[0] - 1, sTail.pos[1])))    # therefore grows the snake 1 pixel to the left(opp direction) of the snake
        elif dirx == -1 and diry == 0:  # moving left
            self.body.append(Cube((sTail.pos[0] + 1, sTail.pos[1])))
        elif dirx == 0 and diry == -1:  # moving up
            self.body.append(Cube((sTail.pos[0], sTail.pos[1] + 1)))
        elif dirx == 0 and diry == 1:   # moving down
            self.body.append(Cube((sTail.pos[0], sTail.pos[1] - 1)))

        self.body[-1].directionX = dirx
        self.body[-1].directionY = diry   # sets the direction that new body part must be moving along with the body currently

    # restarts the game when the player has lost
    def resetGame(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directionY = 0
        self.directionX = 1


# body parts of the snake
class Cube(object):
    rows = 15
    dimension = 600

    def __init__(self, startPos, directionX=1, directionY=0, color=(0, 128, 0)):
        self.pos = startPos
        self.directionX = 1
        self.directionY = 0
        self.color = color

    def move(self, directionX, directionY):
        self.directionX = directionX
        self.directionY = directionY
        self.pos = (self.pos[0] + self.directionX, self.pos[1] + self.directionY)

    def draw(self, surface, head=False):
        blocks = self.dimension // self.rows
        rw = self.pos[0]
        col = self.pos[1]   # rows and columns of our pixels

        # draws the snake body and head
        pygame.draw.rect(surface, self.color, (rw * blocks + 1, col * blocks + 1, blocks - 2, blocks - 2))

        # makes the head different from the rest of the body
        if head:
            pygame.draw.rect(surface, (0, 0, 128), (rw * blocks + 1, col * blocks + 1, blocks - 2, blocks - 2))


# The apple the snake must eat spawn position
def randomApple(rows, snakeParts):
    spots = snakeParts.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # function z (a filtered list of the parts of the snake) is checked if it contains the random (x,y) generated above
        # then this should help ensure that the apple isn't randomly generated in top of the snake
        if len(list(filter(lambda z: z.pos == (x, y), spots))) > 0:
            continue
        else:
            break

    return (x,y)


# remove once start creating levels
def drawGrid(surface, rows, width):
    # size of each block
    block = width // rows

    x = 0
    y = 0
    for i in range(rows):
        # Drawing the lines for the blocks
        x = x + block
        y = y + block
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, dimension))      # Line from top to bottom (vertical)
        pygame.draw.line(surface, (255, 255, 255), (0, y), (dimension, y))      # Line from left to right (horizontal)


# Window refresh
def reDrawWindow(surface):
    global dimension, rows, player, apple
    surface.fill((0, 0, 0))
    #drawGrid(surface, rows, dimension)
    player.draw(surface)
    apple.draw(surface)
    pygame.display.update()

# Allows the player to restart game after they've lost
def gameOver(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# mainloop
def main():
    global dimension, rows, player, apple, delay
    dimension = 600     # since its going to be a square
    rows = 15   # block pixels on screen
    delay = 250     # makes the snake faster as the game goes along

    # window and background
    surface = pygame.display.set_mode((dimension, dimension))
    pygame.display.set_caption('Snake Park')

    # Game objects
    player = Snake((10, 10), (0, 128, 0))
    apple = Cube(randomApple(rows, player), color=(255, 0, 0))
    # game in progress flag
    inGame = True

    # Refresh rate timer
    clock = pygame.time.Clock()

    while inGame:
        pygame.time.delay(delay)       # speed in which the game will be running (lower = faster game)
        clock.tick(60) # refresh rate  (lower = slower game)
        player.move()

        # check if the snake has eaten the apple then generate a new apple and grow snake body
        if player.body[0].pos == apple.pos:
            player.grow()
            if delay > 50:
                delay -= 15
            else:
                print('Score: ', len(player.body))
                gameOver('You Lost!', 'Play again...')  # going to remove later
                player.resetGame((10, 10))
                break
            apple = Cube(randomApple(rows, player), color=(255, 0, 0))   # generate new apple

        for x in range(len(player.body)):
            if player.body[x].pos in list(map(lambda z: z.pos, player.body[x + 1:])):
                print('Score: ', len(player.body))
                gameOver('You Lost!', 'Play again...')       # going to remove later
                player.resetGame((10, 10))
                break
        reDrawWindow(surface)
    pass


main()
