

# layout.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Grid
import os
import random
from functools import reduce

VISIBILITY_MATRIX_CACHE = {}

class Layout:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, layoutText,max_dots,dots_live=None):
        self.width = len(layoutText[0])
        self.height= len(layoutText)
        self.walls = Grid(self.width, self.height, False)
        self.food = Grid(self.width, self.height, False)
        self.capsules = []
        self.agentPositions = []
        self.numGhosts = 0
        self.processLayoutText(layoutText,max_dots=max_dots,dots_live=dots_live)
        self.layoutText = layoutText
        self.max_dots=max_dots
        # self.initializeVisibilityMatrix()

    def getNumGhosts(self):
        return self.numGhosts

    def initializeVisibilityMatrix(self):
        global VISIBILITY_MATRIX_CACHE
        if reduce(str.__add__, self.layoutText) not in VISIBILITY_MATRIX_CACHE:
            from game import Directions
            vecs = [(-0.5,0), (0.5,0),(0,-0.5),(0,0.5)]
            dirs = [Directions.NORTH, Directions.SOUTH, Directions.WEST, Directions.EAST]
            vis = Grid(self.width, self.height, {Directions.NORTH:set(), Directions.SOUTH:set(), Directions.EAST:set(), Directions.WEST:set(), Directions.STOP:set()})
            for x in range(self.width):
                for y in range(self.height):
                    if self.walls[x][y] == False:
                        for vec, direction in zip(vecs, dirs):
                            dx, dy = vec
                            nextx, nexty = x + dx, y + dy
                            while (nextx + nexty) != int(nextx) + int(nexty) or not self.walls[int(nextx)][int(nexty)] :
                                vis[x][y][direction].add((nextx, nexty))
                                nextx, nexty = x + dx, y + dy
            self.visibility = vis
            VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)] = vis
        else:
            self.visibility = VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)]

    def isWall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def getRandomLegalPosition(self):
        x = random.choice(list(range(self.width)))
        y = random.choice(list(range(self.height)))
        while self.isWall( (x, y) ):
            x = random.choice(list(range(self.width)))
            y = random.choice(list(range(self.height)))
        return (x,y)

    def getRandomCorner(self):
        poses = [(1,1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        return random.choice(poses)

    def getFurthestCorner(self, pacPos):
        poses = [(1,1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        dist, pos = max([(manhattanDistance(p, pacPos), p) for p in poses])
        return pos

    def isVisibleFrom(self, ghostPos, pacPos, pacDirection):
        row, col = [int(x) for x in pacPos]
        return ghostPos in self.visibility[row][col][pacDirection]

    def __str__(self):
        return "\n".join(self.layoutText)

    def deepCopy(self):
        return Layout(self.layoutText[:],max_dots=self.max_dots,dots_live=self.dots_live)

    def processLayoutText(self, layoutText,max_dots=0,dots_live=None):
        """
        Coordinates are flipped from the input format to the (x,y) convention here

        The shape of the maze.  Each character
        represents a different type of object.
         % - Wall
         . - Food
         o - Capsule
         G - Ghost
         P - Pacman
        Other characters are ignored.
        """
        #print("max_dots",max_dots)
        maxY = self.height - 1
        num_dots_in_text=sum([1 if layoutText[y][x]=="." else 0 for y in range(self.height) for x in range(self.width)])
        if dots_live==None:
            dots_live=list(range(num_dots_in_text))
            random.shuffle(dots_live)
        self.dots_live=dots_live
        dot_count=0
        for y in range(self.height):
            for x in range(self.width):
                #layoutChar = layoutText[maxY - y][x]
                layoutChar = layoutText[y][x]
                if layoutChar==".":
                    if dots_live[dot_count]>=max_dots and max_dots>0:
                        layoutChar=" "
                    dot_count+=1
                self.processLayoutChar(x, y, layoutChar)
        self.agentPositions.sort()
        self.agentPositions = [ ( i == 0, pos) for i, pos in self.agentPositions]

    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == '.':
            self.food[x][y] = True
        elif layoutChar == 'o':
            self.capsules.append((x, y))
        elif layoutChar == 'P':
            self.agentPositions.append( (0, (x, y) ) )
        elif layoutChar in ['G']:
            self.agentPositions.append( (1, (x, y) ) )
            self.numGhosts += 1
        elif layoutChar in  ['1', '2', '3', '4']:
            self.agentPositions.append( (int(layoutChar), (x,y)))
            self.numGhosts += 1
def getLayout(name, back = 2,max_dots=0):
    #print("getLayout",max_dots)
    if name.endswith('.lay'):
        layout = tryToLoad('layouts/' + name,max_dots=max_dots)
        if layout == None: layout = tryToLoad(name,max_dots=max_dots)
    else:
        layout = tryToLoad('layouts/' + name + '.lay',max_dots=max_dots)
        if layout == None: layout = tryToLoad(name + '.lay',max_dots=max_dots)
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back -1,max_dots=max_dots)
        os.chdir(curdir)
    return layout

def tryToLoad(fullname,max_dots):
    #print("tryToLoad",max_dots)
    if(not os.path.exists(fullname)): return None
    f = open(fullname)
    try: return Layout([line.strip() for line in f],max_dots)
    finally: f.close()


