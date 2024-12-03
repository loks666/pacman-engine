from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ce811ManhattanGhostDodgerHunterAgent(Agent):

    def __init__(self):
        # 初始化逃离方向和逃离模式
        self.escape_direction = None
        self.in_escape_mode = False
        self.escape_steps_remaining = 0  # 逃离模式剩余步数
        self.escape_cooldown = 0  # 逃离模式冷却步数
        self.previous_move = None
        self.move_history = []  # 跟踪最近的移动，防止循环
        self.history_limit = 10  # 动作历史记录限制
        # 定义所有鬼屋的位置（根据游戏布局调整）
        self.ghost_house_positions = [(11, 1), (6, 1), (5, 1), (6, 2), (5, 2)]  # 根据实际游戏布局添加所有鬼屋位置
        # 定义移动方向的循环顺序
        self.direction_sequence = [Directions.EAST, Directions.NORTH, Directions.WEST, Directions.SOUTH]
        self.current_direction_index = 0  # 当前方向索引

    def getAction(self, gameState):
        """
        决定 Pacman 的下一个动作。
        Pacman 将按照预定的方向循环移动，碰到墙壁时切换到下一个方向。
        """
        # 获取合法动作并移除 STOP 以保持 Pacman 移动
        legal_moves = gameState.getLegalPacmanActions()
        if Directions.STOP in legal_moves:
            legal_moves.remove(Directions.STOP)

        # 获取所有鬼魂的状态、位置和距离
        ghost_states = gameState.getGhostStates()
        ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
        # 将鬼魂位置转换为整数元组
        ghost_positions = [tuple(map(int, ghostState.getPosition())) for ghostState in ghost_states]

        # 将鬼魂分为危险鬼魂和害怕鬼魂，排除在鬼屋中的鬼魂
        dangerous_ghosts = []
        scared_ghosts = []
        for i in range(len(ghost_states)):
            if ghost_scared_times[i] > 0 and ghost_positions[i] not in self.ghost_house_positions:
                scared_ghosts.append(ghost_positions[i])
            elif ghost_scared_times[i] <= 0 and ghost_positions[i] not in self.ghost_house_positions:
                dangerous_ghosts.append(ghost_positions[i])

        best_move = None

        # **1. 如果在逃离模式，优先选择逃离方向**
        if self.in_escape_mode and self.escape_direction in legal_moves:
            print(f"在逃离模式，优先选择逃离方向: {self.escape_direction}，剩余逃离步数: {self.escape_steps_remaining}")
            self.escape_steps_remaining -= 1
            if self.escape_steps_remaining <= 0:
                self.in_escape_mode = False
                self.escape_direction = None
                self.escape_cooldown = 5  # 设置冷却步数
                print("已完成逃离步数，退出逃离模式，进入冷却")
            self.previous_move = self.escape_direction
            self.move_history.append(self.escape_direction)
            if len(self.move_history) > self.history_limit:
                self.move_history.pop(0)
            return self.escape_direction

        # **处理逃离模式冷却**
        if self.escape_cooldown > 0:
            self.escape_cooldown -= 1

        # **2. 按照方向循环移动，碰到墙壁时切换方向**
        attempts = 0
        max_attempts = len(self.direction_sequence)
        while attempts < max_attempts:
            current_direction = self.direction_sequence[self.current_direction_index]
            if current_direction in legal_moves:
                best_move = current_direction
                best_score = 0  # 可以根据需要调整评分
                print(f"按照预定方向移动: {current_direction}")
                break
            else:
                # 切换到下一个方向
                self.current_direction_index = (self.current_direction_index + 1) % len(self.direction_sequence)
                print(f"方向 {current_direction} 被阻挡，切换到下一个方向")
                attempts += 1

        # 如果所有预定方向都被阻挡，选择随机合法动作
        if best_move is None:
            if legal_moves:
                best_move = random.choice(legal_moves)
                print(f"所有预定方向都被阻挡，随机选择动作: {best_move}")
            else:
                best_move = Directions.STOP
                print("没有合法动作，选择停止")

        # **记录选择的动作**
        print(f"选择的动作: {best_move}")
        self.previous_move = best_move
        self.move_history.append(best_move)
        if len(self.move_history) > self.history_limit:
            self.move_history.pop(0)

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
                score += distance * 5  # 调低奖励权重

        # **追捕评分：追捕害怕鬼魂**
        capsule_active = closest_capsule_location and manhattanDistance(next_pos, closest_capsule_location) == 0
        for ghost_pos in scared_ghosts:
            distance = manhattanDistance(next_pos, ghost_pos)
            if distance == 0:
                score += 2000  # 高奖励，吃掉鬼魂
            else:
                # 距离越近，奖励越高
                if distance < 5:
                    bonus = (5 - distance) * (100 if capsule_active else 80)  # 在胶囊激活时增加奖励
                    score += bonus

        # **胶囊评分：如果存在危险鬼魂，鼓励吃胶囊**
        if dangerous_ghosts and closest_capsule_location:
            capsule_distance = manhattanDistance(next_pos, closest_capsule_location)
            if capsule_distance <= 5:
                bonus = (5 - capsule_distance) * (50 if capsule_active else 40)  # 在胶囊激活时调整奖励
                score += bonus  # 鼓励接近胶囊

        # **食物评分：鼓励接近食物**
        if closest_food_location:
            food_distance = manhattanDistance(next_pos, closest_food_location)
            score -= food_distance * 5  # 减少食物惩罚

        return score
