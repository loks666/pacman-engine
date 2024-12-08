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
    for x in range(w):
        for y in range(h):
            if maze[x][y]:
                g[y][x] = 0
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
        if caps:
            min_dist_capsule = float('inf')
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
        if target_capsule and min_dist_capsule < 15:  # 可以根据需要调整阈值
            prioritize_capsule = True

        target = target_capsule if prioritize_capsule else target_food
        path = calc_path_to_point(target, parents)

        if len(path) == 0:
            print("无法找到到目标的路径。")
            return Directions.STOP

        # 检查鬼魂的位置，避免被追捕
        ghost_threat = False
        for gh in ghosts:
            gh_pos = gh.getPosition()
            gh_x, gh_y = int(gh_pos[0]), int(gh_pos[1])
            d = gScores[gh_y][gh_x]
            if d < 5 and gh.scaredTimer <= 1:
                ghost_threat = True
                print(f"检测到鬼魂威胁，鬼魂位置: ({gh_x}, {gh_y}), 距离: {d}")
                # 计算远离鬼魂的方向
                away_x = pac[0] - gh_x
                away_y = pac[1] - gh_y
                potential_moves = []
                if away_x > 0 and Directions.EAST in legalMoves:
                    potential_moves.append(Directions.EAST)
                elif away_x < 0 and Directions.WEST in legalMoves:
                    potential_moves.append(Directions.WEST)
                if away_y > 0 and Directions.SOUTH in legalMoves:
                    potential_moves.append(Directions.SOUTH)
                elif away_y < 0 and Directions.NORTH in legalMoves:
                    potential_moves.append(Directions.NORTH)

                if potential_moves:
                    # 优先选择远离鬼魂的方向
                    chosen_move = Directions.SOUTH if Directions.SOUTH in potential_moves else random.choice(potential_moves)
                    print(f"选择远离鬼魂的移动方向: {chosen_move}")
                    return chosen_move

        # 如果没有鬼魂威胁，按计划移动
        desired_move = path[0]
        if desired_move in legalMoves:
            print(f"按计划移动方向: {desired_move}")
            return desired_move
        else:
            # 如果计划的方向被阻挡，随机选择一个合法方向
            print("计划的移动方向被阻挡，随机选择一个合法方向。")
            possible_moves = list(legalMoves)
            # 移除STOP以避免停滞
            if Directions.STOP in possible_moves:
                possible_moves.remove(Directions.STOP)
            if len(possible_moves) > 0:
                chosen_move = random.choice(possible_moves)
                print(f"随机选择的移动方向: {chosen_move}")
                return chosen_move
            else:
                print("没有可行的移动方向，停止行动。")
                return Directions.STOP
