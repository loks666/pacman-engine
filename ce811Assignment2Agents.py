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
        if 0 <= nx < w and 0 <= ny < h and maze[nx][ny] == False:
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

        # 调试信息：打印当前Pacman位置与基本信息
        print("Pacman Position:", pac)
        print("Score:", gameState.getScore())
        print("Legal Moves:", legalMoves)
        print("Foods:", foods)
        print("Capsules:", caps)

        # 如果没有食物，停止行动
        if not foods:
            print("No foods left. Stopping.")
            return Directions.STOP

        # 找到最近的食物
        min_dist = float('inf')
        closest_food = None
        for food in foods:
            dist = gScores[int(food[1]), int(food[0])]
            if dist < min_dist:
                min_dist = dist
                closest_food = food

        if closest_food is None:
            print("No reachable food found. Stopping.")
            return Directions.STOP

        # 计算到最近食物的路径
        path = calc_path_to_point(closest_food, parents)

        if len(path) == 0:
            print("No path to closest food found. Stopping.")
            return Directions.STOP

        # 选择路径上的第一个方向
        desired_move = path[0]
        print("Desired Move:", desired_move)

        # 检查鬼魂的位置，避免被追捕
        ghost_threat = False
        for gh in ghosts:
            gh_pos = gh.getPosition()
            gh_x, gh_y = int(gh_pos[0]), int(gh_pos[1])
            d = gScores[gh_y][gh_x]
            if d < 5 and gh.scaredTimer <= 1:
                ghost_threat = True
                print(f"Ghost threat detected at distance {d} from position ({gh_x}, {gh_y})")
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
                    chosen_move = random.choice(potential_moves)
                    print(f"Choosing to move away from ghost: {chosen_move}")
                    return chosen_move

        # 如果没有鬼魂威胁，按计划移动
        if desired_move in legalMoves:
            print(f"Moving towards desired move: {desired_move}")
            return desired_move
        else:
            # 如果计划的方向被阻挡，随机选择一个合法方向
            print("Desired move blocked. Choosing a random legal move.")
            possible_moves = list(legalMoves)
            # 移除STOP以避免停滞（根据需要保留或去除）
            if Directions.STOP in possible_moves:
                possible_moves.remove(Directions.STOP)
            if len(possible_moves) > 0:
                chosen_move = random.choice(possible_moves)
                print(f"Randomly chosen move: {chosen_move}")
                return chosen_move
            else:
                print("No possible moves left. Stopping.")
                return Directions.STOP
