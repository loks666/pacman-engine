from game import Directions
import random, util
import numpy as np
import heapq
from game import Agent

def calculate_neighbouring_nodes(node, maze):
    (x, y) = node
    h = maze.height
    w = maze.width
    res = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not maze[nx][ny]:
            res.append((nx, ny))
    return res

def calculate_gscores(maze, start_node):
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
    while pq:
        d, (cx, cy) = heapq.heappop(pq)
        if d > g[cy][cx]:
            continue
        for (nx, ny) in calculate_neighbouring_nodes((cx, cy), maze):
            nd = d + 1
            if nd < g[ny][nx]:
                g[ny][nx] = nd
                p[(nx, ny)] = (cx, cy)
                heapq.heappush(pq, (nd, (nx, ny)))
    # 修正墙壁的代价为INF
    for x in range(w):
        for y in range(h):
            if maze[x][y]:
                g[y][x] = INF
    return g, p

def calc_path_to_point(end_node, parent_nodes):
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

class ce811DijkstraRuleAgent(Agent):
    def __init__(self):
        self.route = []
        self.last_action = Directions.STOP

    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        pac = gameState.getPacmanPosition()
        maze = gameState.getWalls()
        gScores, parents = calculate_gscores(maze, (int(pac[0]), int(pac[1])))

        foods = gameState.getFood().asList()
        ghosts = gameState.getGhostStates()
        caps = gameState.getCapsules()

        # 关键调试信息：Pacman位置与剩余食物数量
        print(f"Pacman位置: {pac}, 剩余食物数量: {len(foods)}")

        # 如果没有食物，停止行动
        if not foods:
            print("所有食物已被吃完。")
            return Directions.STOP

        # 找到最近的胶囊（如果有）
        target_capsule = None
        min_dist_capsule = float('inf')
        if caps:
            for cap in caps:
                dist = gScores[int(cap[1]), int(cap[0])]
                if dist < min_dist_capsule:
                    min_dist_capsule = dist
                    target_capsule = cap

        # 找到最近的食物
        target_food = None
        min_dist_food = float('inf')
        for food in foods:
            dist = gScores[int(food[1]), int(food[0])]
            if dist < min_dist_food:
                min_dist_food = dist
                target_food = food

        # 决定优先级：如果有胶囊且距离较近，优先收集胶囊
        prioritize_capsule = False
        CAP_THRESHOLD = 15  # 可以根据需要调整阈值
        if target_capsule and min_dist_capsule < CAP_THRESHOLD:
            prioritize_capsule = True

        target = target_capsule if prioritize_capsule else target_food
        path = calc_path_to_point(target, parents)

        if len(path) == 0:
            print("无法找到到目标的路径。")
            return Directions.STOP

        # 引入移动评分系统
        move_scores = {}
        for move in legalMoves:
            if move == Directions.STOP:
                continue  # 可以根据需要决定是否考虑停顿
            # 计算移动后的新位置
            new_pos = self.get_new_position(pac, move)
            # 计算到最近食物的距离
            food_dist = self.get_closest_food_distance(new_pos, foods, gScores)
            # 计算到最近鬼魂的距离
            ghost_dist = self.get_closest_ghost_distance(new_pos, ghosts)
            # 计算评分：安全性优先，进展次之
            # 可以调整权重，根据需要平衡
            safety_weight = 10
            progress_weight = 1
            score = (ghost_dist * safety_weight) - (food_dist * progress_weight)
            move_scores[move] = score
            # 打印评分信息（可选）
            # print(f"Move: {move}, Score: {score}")

        # 选择最高分的移动方向
        best_move = max(move_scores, key=move_scores.get)
        best_score = move_scores[best_move]

        # 判断是否存在鬼魂威胁
        ghost_threat = False
        for gh in ghosts:
            gh_pos = gh.getPosition()
            gh_x, gh_y = int(gh_pos[0]), int(gh_pos[1])
            d = self.manhattan_distance(pac, (gh_x, gh_y))
            if d < 5 and gh.scaredTimer <= 1:
                ghost_threat = True
                break

        if ghost_threat:
            # 如果存在鬼魂威胁，选择得分最高的安全移动方向
            print(f"存在鬼魂威胁，选择移动方向: {best_move}")
            return best_move
        else:
            # 如果没有威胁，按计划移动
            desired_move = path[0]
            if desired_move in legalMoves:
                print(f"按计划移动方向: {desired_move}")
                return desired_move
            else:
                # 如果计划的方向被阻挡，选择得分最高的移动方向
                print("计划的移动方向被阻挡，选择得分最高的移动方向。")
                print(f"选择移动方向: {best_move}")
                return best_move

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
            return pos  # STOP

    def get_closest_food_distance(self, pos, foods, gScores):
        min_dist = float('inf')
        for food in foods:
            dist = gScores[int(food[1]), int(food[0])]
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def get_closest_ghost_distance(self, pos, ghosts):
        min_dist = float('inf')
        for gh in ghosts:
            gh_pos = gh.getPosition()
            gh_x, gh_y = int(gh_pos[0]), int(gh_pos[1])
            dist = self.manhattan_distance(pos, (gh_x, gh_y))
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
