import numpy as np
import layout
from game import Directions
import heapq

def calculate_neighbouring_nodes(node, maze):
    (x, y) = node
    maze_height = maze.height
    maze_width = maze.width
    neighbours = []
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze_width and 0 <= ny < maze_height:
            if maze[nx][ny] == False:
                neighbours.append((nx, ny))
    return neighbours

def calculate_gscores(maze, start_node):
    assert str(type(maze))=="<class 'game.Grid'>"
    maze_height = maze.height
    maze_width = maze.width
    assert maze[start_node[0]][start_node[1]]==False,"start_node error "+str(start_node)

    INF = 999999
    array_gScores = np.full((maze_height, maze_width), INF, dtype=int)
    parent_nodes = {}

    (sx, sy) = start_node
    array_gScores[sy, sx] = 0
    parent_nodes[(sx, sy)] = None

    pq = []
    heapq.heappush(pq, (0, (sx, sy)))

    while pq:
        cur_dist, (cx, cy) = heapq.heappop(pq)
        if cur_dist > array_gScores[cy, cx]:
            continue
        for (nx, ny) in calculate_neighbouring_nodes((cx, cy), maze):
            new_dist = cur_dist + 1
            if new_dist < array_gScores[ny, nx]:
                array_gScores[ny, nx] = new_dist
                parent_nodes[(nx, ny)] = (cx, cy)
                heapq.heappush(pq, (new_dist, (nx, ny)))

    # Set walls to 0 gScore
    for x in range(maze_width):
        for y in range(maze_height):
            if maze[x][y] == True:
                array_gScores[y, x] = 0

    return [array_gScores, parent_nodes]

def calc_path_A_to_B(start_node, end_node, maze_walls):
    gScores, parent_nodes = calculate_gscores(maze_walls, start_node)
    return calc_path_to_point(end_node, parent_nodes)

def calc_path_to_point(end_node, parent_nodes):
    path = []
    current = end_node

    # Walk backwards from end_node to start_node using parent_nodes
    while current is not None and parent_nodes[current] is not None:
        parent = parent_nodes[current]
        (px, py) = parent
        (cx, cy) = current

        # Determine direction from parent to current
        if cx == px + 1 and cy == py:
            path.append(Directions.EAST)
        elif cx == px - 1 and cy == py:
            path.append(Directions.WEST)
        elif cx == px and cy == py + 1:
            path.append(Directions.SOUTH)
        elif cx == px and cy == py - 1:
            path.append(Directions.NORTH)

        current = parent

    # Reverse the path since we constructed it backwards
    path.reverse()
    return path
