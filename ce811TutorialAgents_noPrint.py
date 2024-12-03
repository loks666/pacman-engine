from game import Directions
import random, util
from game import Agent

class ce811ManhattanGhostDodgerHunterAgent(Agent):

    def __init__(self):
        super().__init__()
        self.escape_direction = self.in_escape_mode = self.escape_steps_remaining = self.escape_cooldown = 0
        self.previous_move = None
        self.move_history = []
        self.history_limit = 10
        self.ghost_house_positions = [(11, 1), (6, 1), (5, 1), (6, 2), (5, 2)]
        self.direction_sequence = [Directions.EAST, Directions.NORTH, Directions.WEST, Directions.SOUTH]
        self.current_direction_index = 0

    def getAction(self, gameState):
        legal_moves = gameState.getLegalActions()
        if Directions.STOP in legal_moves: legal_moves.remove(Directions.STOP)
        ghost_states = gameState.getGhostStates()
        ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
        ghost_positions = [tuple(map(int, ghostState.getPosition())) for ghostState in ghost_states]
        dangerous_ghosts, scared_ghosts = [], []
        for i, ghost_pos in enumerate(ghost_positions):
            if ghost_scared_times[i] > 0 and ghost_pos not in self.ghost_house_positions:
                scared_ghosts.append(ghost_pos)
            elif ghost_pos not in self.ghost_house_positions:
                dangerous_ghosts.append(ghost_pos)

        best_move = None

        if self.in_escape_mode and self.escape_direction in legal_moves:
            self.escape_steps_remaining -= 1
            if self.escape_steps_remaining <= 0:
                self.in_escape_mode = False
                self.escape_cooldown = 5
            self.previous_move = self.escape_direction
            self.move_history.append(self.escape_direction)
            if len(self.move_history) > self.history_limit:
                self.move_history.pop(0)
            return self.escape_direction

        if self.escape_cooldown > 0:
            self.escape_cooldown -= 1

        attempts = 0
        max_attempts = len(self.direction_sequence)
        while attempts < max_attempts:
            current_direction = self.direction_sequence[self.current_direction_index]
            if current_direction in legal_moves:
                best_move = current_direction
                break
            else:
                self.current_direction_index = (self.current_direction_index + 1) % len(self.direction_sequence)
                attempts += 1

        if best_move is None:
            if legal_moves:
                best_move = random.choice(legal_moves)
            else:
                best_move = Directions.STOP

        self.previous_move = best_move
        self.move_history.append(best_move)
        if len(self.move_history) > self.history_limit:
            self.move_history.pop(0)

        return best_move

    def evaluate_move(self, move, pacman_pos, dangerous_ghosts, scared_ghosts, closest_food_location, closest_capsule_location):
        direction_deltas = {Directions.NORTH: (0, 1), Directions.SOUTH: (0, -1), Directions.EAST: (1, 0), Directions.WEST: (-1, 0)}
        dx, dy = direction_deltas[move]
        next_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)

        score = 0
        for ghost_pos in dangerous_ghosts:
            distance = util.manhattanDistance(next_pos, ghost_pos)
            if distance <= 1:
                score -= 1000
            else:
                score += distance * 5

        capsule_active = closest_capsule_location and util.manhattanDistance(next_pos, closest_capsule_location) == 0
        for ghost_pos in scared_ghosts:
            distance = util.manhattanDistance(next_pos, ghost_pos)
            if distance == 0:
                score += 2000
            elif distance < 5:
                bonus = (5 - distance) * (100 if capsule_active else 80)
                score += bonus

        if dangerous_ghosts and closest_capsule_location:
            capsule_distance = util.manhattanDistance(next_pos, closest_capsule_location)
            if capsule_distance <= 5:
                bonus = (5 - capsule_distance) * (50 if capsule_active else 40)
                score += bonus

        if closest_food_location:
            food_distance = util.manhattanDistance(next_pos, closest_food_location)
            score -= food_distance * 5

        return score
