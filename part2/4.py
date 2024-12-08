from game import Directions
from game import Agent
from game import Actions
import random
import numpy as np
import heapq

def calculate_neighboring_nodes(node, maze):
    (x, y) = node
    h = maze.height
    w = maze.width
    res = []
    for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
        nx, ny = x+dx, y+dy
        if 0<=nx<w and 0<=ny<h and maze[nx][ny]==False:
            res.append((nx,ny))
    return res

def calculate_gscores(maze, start_node):
    h = maze.height
    w = maze.width
    INF = 999999
    g = np.full((h,w), INF, dtype=int)
    p = {}
    (sx,sy) = start_node
    g[sy,sx] = 0
    p[(sx,sy)] = None
    pq=[]
    heapq.heappush(pq, (0,(sx,sy)))
    while pq:
        d,(cx,cy)=heapq.heappop(pq)
        if d>g[cy,cx]:
            continue
        for (nx,ny) in calculate_neighboring_nodes((cx,cy),maze):
            nd=d+1
            if nd<g[ny,nx]:
                g[ny,nx]=nd
                p[(nx,ny)]=(cx,cy)
                heapq.heappush(pq,(nd,(nx,ny)))
    for x in range(w):
        for y in range(h):
            if maze[x][y]:
                g[y,x]=0
    return g,p

class ce811OneStepLookaheadDijkstraAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.evaluateBoardState(gameState.generatePacmanSuccessor(a)) for a in legalMoves]
        m = max(scores)
        L = [i for i,x in enumerate(scores) if x==m]
        return legalMoves[random.choice(L)]

    def evaluateBoardState(self, gameState):
        pac = gameState.getPacmanPosition()
        maze = gameState.getWalls()
        gScores,parents = calculate_gscores(maze,(int(pac[0]),int(pac[1])))
        foods = gameState.getFood().asList()
        ghosts = gameState.getGhostStates()
        caps = gameState.getCapsules()
        score = gameState.getScore()
        if foods:
            fdists = [gScores[int(y),int(x)] for x,y in foods if gScores[int(y),int(x)]<999999]
            if fdists:
                score -= 2*min(fdists)
        gdist_danger = []
        gdist_scared = []
        for gho in ghosts:
            gx,gy = gho.getPosition()
            gx,gy = int(gx),int(gy)
            d = gScores[gy,gx]
            if d<999999:
                if gho.scaredTimer>1:
                    gdist_scared.append(d)
                else:
                    gdist_danger.append(d)
        for d in gdist_danger:
            if d==0:
                score -=1000
            else:
                score -=30.0/d
        for d in gdist_scared:
            if d>0:
                score +=20.0/d
        if caps:
            cdists = [gScores[int(y),int(x)] for x,y in caps if gScores[int(y),int(x)]<999999]
            if cdists:
                cmin = min(cdists)
                if cmin>0:
                    score +=5.0/(cmin+1)
        return score
