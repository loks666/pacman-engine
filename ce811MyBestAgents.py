# ce811MyBestAgents.py

from game import Directions
from game import Agent
from game import Actions
import random
import numpy as np
import heapq


class ce811MyBestAgent(Agent):
    def __init__(self):
        super().__init__()
        self.last_action = Directions.STOP
        self.capsules = []
        self.ghost_positions = []
        self.ghost_scared_times = {}
        self.foods = []

    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        pac = gameState.getPacmanPosition()
        maze = gameState.getWalls()
        self.foods = gameState.getFood().asList()
        ghosts = gameState.getGhostStates()
        self.capsules = gameState.getCapsules()

        self.ghost_positions = []
        self.ghost_scared_times = {}
        for gh in ghosts:
            gh_pos = gh.getPosition()
            gh_x, gh_y = int(gh_pos[0]), int(gh_pos[1])
            self.ghost_positions.append((gh_x, gh_y))
            self.ghost_scared_times[(gh_x, gh_y)] = gh.scaredTimer

        if not self.foods:
            return Directions.STOP

        target_capsule = None
        min_dist_capsule = float('inf')
        for cap in self.capsules:
            dist = self.manhattan_distance(pac, cap)
            if dist < min_dist_capsule:
                min_dist_capsule = dist
                target_capsule = cap

        target_food = None
        min_dist_food = float('inf')
        for food in self.foods:
            dist = self.manhattan_distance(pac, food)
            if dist < min_dist_food:
                min_dist_food = dist
                target_food = food

        prioritize_capsule = False
        CAP_THRESHOLD = 15
        if target_capsule and min_dist_capsule < CAP_THRESHOLD:
            prioritize_capsule = True

        target = target_capsule if prioritize_capsule else target_food

        gScores, parents = self.calculate_gscores(maze, pac)
        path = self.calc_path_to_point(target, parents)

        if not path:
            return Directions.STOP

        move_scores = {}
        for move in legalMoves:
            if move == Directions.STOP:
                continue
            new_pos = self.get_new_position(pac, move)
            food_dist = self.get_closest_food_distance(new_pos)
            ghost_dist = self.get_closest_ghost_distance(new_pos)
            safety_weight = 10
            progress_weight = 1
            score = (ghost_dist * safety_weight) - (food_dist * progress_weight)
            move_scores[move] = score

        best_move = max(move_scores, key=move_scores.get)
        best_score = move_scores[best_move]

        ghost_threat = False
        for gh_pos, scared_time in self.ghost_scared_times.items():
            dist = self.manhattan_distance(pac, gh_pos)
            if dist < 5 and scared_time <= 1:
                ghost_threat = True
                break

        if ghost_threat:
            return best_move
        else:
            desired_move = path[0]
            if desired_move in legalMoves:
                return desired_move
            else:
                return best_move

    def calculate_gscores(self, maze, start_node, ghost_radius=5):
        h = maze.height
        w = maze.width
        INF = 999999
        g = np.full((h, w), INF, dtype=int)
        p = {}
        (sx, sy) = start_node
        g[sy][sx] = 0
        p[(sx, sy)] = None
        pq = []
        heapq.heappush(pq, (0, (sx, sy)))

        cost_map = np.ones((h, w), dtype=int)
        for gh_pos in self.ghost_positions:
            gh_x, gh_y = gh_pos
            for x in range(max(0, gh_x - ghost_radius), min(w, gh_x + ghost_radius + 1)):
                for y in range(max(0, gh_y - ghost_radius), min(h, gh_y + ghost_radius + 1)):
                    dist = abs(x - gh_x) + abs(y - gh_y)
                    if dist <= ghost_radius:
                        cost_map[y][x] += (ghost_radius - dist + 1) * 10

        while pq:
            d, (cx, cy) = heapq.heappop(pq)
            if d > g[cy][cx]:
                continue
            for (nx, ny) in self.calculate_neighbouring_nodes((cx, cy), maze):
                nd = d + cost_map[ny][nx]
                if nd < g[ny][nx]:
                    g[ny][nx] = nd
                    p[(nx, ny)] = (cx, cy)
                    heapq.heappush(pq, (nd, (nx, ny)))

        for x in range(w):
            for y in range(h):
                if maze[x][y]:
                    g[y][x] = INF
        return g, p

    def calculate_neighbouring_nodes(self, node, maze):
        (x, y) = node
        h = maze.height
        w = maze.width
        res = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not maze[nx][ny]:
                res.append((nx, ny))
        return res

    def calc_path_to_point(self, end_node, parent_nodes):
        path = []
        c = end_node
        while c in parent_nodes and parent_nodes[c] is not None:
            pa = parent_nodes[c]
            px, py = pa
            cx, cy = c
            if cx == px + 1 and cy == py:
                path.append(Directions.EAST)
            elif cx == px - 1 and cy == py:
                path.append(Directions.WEST)
            elif cx == px and cy == py + 1:
                path.append(Directions.SOUTH)
            elif cx == px and cy == py - 1:
                path.append(Directions.NORTH)
            c = pa
        path.reverse()
        return path

    def get_new_position(self, pos, direction):
        x, y = pos
        if direction == Directions.NORTH:
            return (x, y - 1)
        elif direction == Directions.SOUTH:
            return (x, y + 1)
        elif direction == Directions.EAST:
            return (x + 1, y)
        elif direction == Directions.WEST:
            return (x - 1, y)
        else:
            return pos

    def get_closest_food_distance(self, pos):
        min_dist = float('inf')
        for food in self.foods:
            dist = self.manhattan_distance(pos, food)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def get_closest_ghost_distance(self, pos):
        min_dist = float('inf')
        for gh_pos in self.ghost_positions:
            dist = self.manhattan_distance(pos, gh_pos)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
