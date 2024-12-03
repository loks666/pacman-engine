from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ce811ManhattanGhostDodgerHunterAgent(Agent):

    def __init__(self):
        # 初始化逃离方向和逃离模式
        self.escape_direction = None
        self.in_escape_mode = False
        self.previous_move = None

    def getAction(self, gameState):
        """
        决定 Pacman 的下一个动作。
        Pacman 将在危险时躲避鬼魂，害怕时追捕鬼魂，并在其他情况下吃食物或胶囊。
        """

        # 获取合法动作并移除 STOP 以保持 Pacman 移动
        legal_moves = gameState.getLegalPacmanActions()
        if Directions.STOP in legal_moves:
            legal_moves.remove(Directions.STOP)

        # 获取 Pacman 的位置
        pacman_pos = gameState.getPacmanPosition()

        # 获取所有鬼魂的状态、位置和距离
        ghost_states = gameState.getGhostStates()
        ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
        ghost_positions = [ghostState.getPosition() for ghostState in ghost_states]
        ghost_distances = [manhattanDistance(pacman_pos, ghost_pos) for ghost_pos in ghost_positions]

        # 将鬼魂分为危险鬼魂和害怕鬼魂
        dangerous_ghosts = []
        scared_ghosts = []
        for i in range(len(ghost_states)):
            if ghost_scared_times[i] <= 1:
                dangerous_ghosts.append(ghost_positions[i])
            else:
                scared_ghosts.append(ghost_positions[i])

        # 获取食物和胶囊的位置
        food_locations = gameState.getFood().asList()
        capsule_locations = gameState.getCapsules()

        # 找到最近的食物
        if food_locations:
            closest_food_location = min(food_locations, key=lambda food: manhattanDistance(pacman_pos, food))
            closest_food_distance = manhattanDistance(pacman_pos, closest_food_location)
        else:
            closest_food_location = None
            closest_food_distance = float('inf')

        # 找到最近的胶囊
        if capsule_locations:
            closest_capsule_location = min(capsule_locations, key=lambda cap: manhattanDistance(pacman_pos, cap))
            closest_capsule_distance = manhattanDistance(pacman_pos, closest_capsule_location)
        else:
            closest_capsule_location = None
            closest_capsule_distance = float('inf')

        # 定义各个方向的坐标变化
        direction_deltas = {
            Directions.NORTH: (0, 1),
            Directions.SOUTH: (0, -1),
            Directions.EAST:  (1, 0),
            Directions.WEST:  (-1, 0)
        }

        best_move = None
        best_score = -float('inf')

        # 定义相反方向，以防止 Pacman 立即反向移动，导致震荡
        opposite_directions = {
            Directions.NORTH: Directions.SOUTH,
            Directions.SOUTH: Directions.NORTH,
            Directions.EAST: Directions.WEST,
            Directions.WEST: Directions.EAST
        }

        # 如果在逃离模式，优先选择逃离方向
        if self.in_escape_mode and self.escape_direction in legal_moves:
            print(f"在逃离模式，优先选择逃离方向: {self.escape_direction}")
            self.previous_move = self.escape_direction
            return self.escape_direction

        # 评估每一个合法动作
        for move in legal_moves:
            # 如果当前动作是上一步动作的相反方向，则跳过，避免震荡
            if self.previous_move and move == opposite_directions.get(self.previous_move):
                print(f"跳过反向动作: {move}")
                continue

            dx, dy = direction_deltas[move]
            next_x = pacman_pos[0] + dx
            next_y = pacman_pos[1] + dy
            next_pos = (next_x, next_y)

            score = 0
            debug_info = f"评估动作 {move}: 下一位置 {next_pos}, 初始分数 {score}"

            # **安全评分：避免危险鬼魂**
            for ghost_pos in dangerous_ghosts:
                distance = manhattanDistance(next_pos, ghost_pos)
                if distance <= 1:
                    score -= 1000  # 高惩罚，避免死亡
                    debug_info += f"\n  危险鬼魂在 {ghost_pos} 处，距离 {distance}, 施加惩罚 -1000"
                else:
                    bonus = distance * 10
                    score += bonus  # 鼓励远离
                    debug_info += f"\n  危险鬼魂在 {ghost_pos} 处，距离 {distance}, 施加奖励 +{bonus}"

            # **追捕评分：追捕害怕鬼魂**
            for ghost_pos in scared_ghosts:
                distance = manhattanDistance(next_pos, ghost_pos)
                if distance == 0:
                    score += 2000  # 高奖励，吃掉鬼魂
                    debug_info += f"\n  害怕鬼魂在 {ghost_pos} 处，将被吃掉，施加奖励 +2000"
                else:
                    # 距离越近，奖励越高
                    if distance < 5:
                        bonus = (5 - distance) * 100
                        score += bonus
                        debug_info += f"\n  害怕鬼魂在 {ghost_pos} 处，距离 {distance}, 施加奖励 +{bonus}"
                    else:
                        debug_info += f"\n  害怕鬼魂在 {ghost_pos} 处，距离 {distance}, 不施加奖励"

            # **胶囊评分：如果存在危险鬼魂，鼓励吃胶囊**
            if dangerous_ghosts and capsule_locations:
                capsule_distance = manhattanDistance(next_pos, closest_capsule_location)
                if capsule_distance <= 5:
                    bonus = (5 - capsule_distance) * 50
                    score += bonus  # 鼓励接近胶囊
                    debug_info += f"\n  存在危险鬼魂，胶囊在 {closest_capsule_location} 处，距离 {capsule_distance}, 施加奖励 +{bonus}"

            # **食物评分：鼓励接近食物**
            if closest_food_location:
                food_distance = manhattanDistance(next_pos, closest_food_location)
                food_penalty = food_distance * 5
                score -= food_penalty  # 鼓励接近食物
                debug_info += f"\n  最近的食物在 {closest_food_location} 处，距离 {food_distance}, 施加惩罚 -{food_penalty}"

            # **记录每个动作的评分和原因**
            debug_info += f"\n  动作 {move} 的总分数: {score}"

            # 打印调试信息
            print(debug_info)

            # **选择最佳动作**
            if score > best_score:
                best_score = score
                best_move = move
                debug_info_best = f"找到新的最佳动作: {move}，分数 {score}"
                print(debug_info_best)

        # 如果没有最佳动作，尝试选择逃离方向
        if best_move is None and (dangerous_ghosts or scared_ghosts):
            possible_escape_directions = [Directions.NORTH, Directions.SOUTH]
            for escape_dir in possible_escape_directions:
                if escape_dir in legal_moves and escape_dir != opposite_directions.get(self.previous_move):
                    best_move = escape_dir
                    self.escape_direction = escape_dir
                    self.in_escape_mode = True
                    print(f"选择逃离动作: {best_move}")
                    break

        # 如果仍然没有最佳动作，选择得分最高的动作
        if best_move is None:
            if legal_moves:
                best_move = max(legal_moves, key=lambda move: self.evaluate_move(move, pacman_pos, dangerous_ghosts, scared_ghosts, closest_food_location, closest_capsule_location))
                print(f"选择得分最高的动作: {best_move}")
            else:
                best_move = random.choice(legal_moves)
                print(f"没有找到最佳动作，随机选择动作: {best_move}")

        # 打印选择的最佳动作
        if best_move:
            print(f"选择的动作: {best_move}，分数 {best_score}")
            self.previous_move = best_move  # 记录当前动作
            # 如果不再需要逃离模式，重置逃离模式
            if self.in_escape_mode:
                # 检查是否已经脱离危险区域
                is_safe = all(manhattanDistance(best_move, ghost_pos) > 1 for ghost_pos in dangerous_ghosts)
                if is_safe:
                    self.in_escape_mode = False
                    self.escape_direction = None
        else:
            best_move = random.choice(legal_moves)
            print(f"没有找到最佳动作，随机选择动作: {best_move}")
            self.previous_move = best_move  # 记录当前动作

        return best_move

    def evaluate_move(self, move, pacman_pos, dangerous_ghosts, scared_ghosts, closest_food_location, closest_capsule_location):
        """
        评估某个动作的得分
        """
        direction_deltas = {
            Directions.NORTH: (0, 1),
            Directions.SOUTH: (0, -1),
            Directions.EAST:  (1, 0),
            Directions.WEST:  (-1, 0)
        }

        dx, dy = direction_deltas[move]
        next_x = pacman_pos[0] + dx
        next_y = pacman_pos[1] + dy
        next_pos = (next_x, next_y)

        score = 0

        # **安全评分：避免危险鬼魂**
        for ghost_pos in dangerous_ghosts:
            distance = manhattanDistance(next_pos, ghost_pos)
            if distance <= 1:
                score -= 1000  # 高惩罚，避免死亡
            else:
                score += distance * 10  # 鼓励远离

        # **追捕评分：追捕害怕鬼魂**
        for ghost_pos in scared_ghosts:
            distance = manhattanDistance(next_pos, ghost_pos)
            if distance == 0:
                score += 2000  # 高奖励，吃掉鬼魂
            else:
                # 距离越近，奖励越高
                if distance < 5:
                    bonus = (5 - distance) * 100
                    score += bonus

        # **胶囊评分：如果存在危险鬼魂，鼓励吃胶囊**
        if dangerous_ghosts and closest_capsule_location:
            capsule_distance = manhattanDistance(next_pos, closest_capsule_location)
            if capsule_distance <= 5:
                bonus = (5 - capsule_distance) * 50
                score += bonus  # 鼓励接近胶囊

        # **食物评分：鼓励接近食物**
        if closest_food_location:
            food_distance = manhattanDistance(next_pos, closest_food_location)
            score -= food_distance * 5  # 鼓励接近食物

        return score
