import numpy as np
import layout
import heapq  # We'll use a priority queue for Dijkstra

def calculate_neighbouring_nodes(node, maze):
    (x, y) = node
    maze_height = maze.height
    maze_width = maze.width
    neighbours = []
    # Check the four directions: up, down, left, right
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze_width and 0 <= ny < maze_height:
            # If it's not a wall
            if maze[nx][ny] == False:
                neighbours.append((nx, ny))
    return neighbours

def calculate_gscores(maze, start_node):
    assert str(type(maze))=="<class 'game.Grid'>"
    maze_height = maze.height
    maze_width = maze.width
    assert maze[start_node[0]][start_node[1]]==False,"start_node error "+str(start_node) # start node must not be a wall

    # Initialize gScores with a large number (e.g., a large int)
    INF = 999999
    array_gScores = np.full((maze_height, maze_width), INF, dtype=int)

    # Parent nodes dictionary { (x,y): (px,py) }
    parent_nodes = {}

    # Convert start_node and indexing
    (sx, sy) = start_node
    array_gScores[sy, sx] = 0
    parent_nodes[(sx, sy)] = None

    # Priority queue for Dijkstra (distance, (x,y))
    pq = []
    heapq.heappush(pq, (0, (sx, sy)))

    while pq:
        cur_dist, (cx, cy) = heapq.heappop(pq)
        if cur_dist > array_gScores[cy, cx]:
            # Skip this node if we already have a better path
            continue
        # Explore neighbours
        for (nx, ny) in calculate_neighbouring_nodes((cx, cy), maze):
            new_dist = cur_dist + 1
            if new_dist < array_gScores[ny, nx]:
                array_gScores[ny, nx] = new_dist
                parent_nodes[(nx, ny)] = (cx, cy)
                heapq.heappush(pq, (new_dist, (nx, ny)))

    # For all walls, set gScore to 0 as per requirement
    for x in range(maze_width):
        for y in range(maze_height):
            if maze[x][y] == True:
                array_gScores[y, x] = 0

    return [array_gScores, parent_nodes]
