from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ce811ManhattanGhostDodgerHunterAgent(Agent):

    def __init__(self):
        self.escape_direction = None
        self.in_escape_mode = False
        self.previous_move = None
        self.move_history = []

    def getAction(self, gameState):
        legal_moves = gameState.getLegalPacmanActions()
        if Directions.STOP in legal_moves:
            legal_moves.remove(Directions.STOP)

        pacman_pos = gameState.getPacmanPosition()

        ghost_states = gameState.getGhostStates()
        ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
        ghost_positions = [ghostState.getPosition() for ghostState in ghost_states]
        ghost_distances = [manhattanDistance(pacman_pos, ghost_pos) for ghost_pos in ghost_positions]

        dangerous_ghosts = []
        scared_ghosts = []
        for i in range(len(ghost_states)):
            if ghost_scared_times[i] <= 1:
                dangerous_ghosts.append(ghost_positions[i])
            else:
                scared_ghosts.append(ghost_positions[i])

        food_locations = gameState.getFood().asList()
        capsule_locations = gameState.getCapsules()

        if food_locations:
            closest_food_location = min(food_locations, key=lambda food: manhattanDistance(pacman_pos, food))
            closest_food_distance = manhattanDistance(pacman_pos, closest_food_location)
        else:
            closest_food_location = None
            closest_food_distance = float('inf')

        if capsule_locations:
            closest_capsule_location = min(capsule_locations, key=lambda cap: manhattanDistance(pacman_pos, cap))
            closest_capsule_distance = manhattanDistance(pacman_pos, closest_capsule_location)
        else:
            closest_capsule_location = None
            closest_capsule_distance = float('inf')

        direction_deltas = {
            Directions.NORTH: (0, 1),
            Directions.SOUTH: (0, -1),
            Directions.EAST:  (1, 0),
            Directions.WEST:  (-1, 0)
        }

        best_move = None
        best_score = -float('inf')

        opposite_directions = {
            Directions.NORTH: Directions.SOUTH,
            Directions.SOUTH: Directions.NORTH,
            Directions.EAST: Directions.WEST,
            Directions.WEST: Directions.EAST
        }

        if self.in_escape_mode and self.escape_direction in legal_moves:
            self.previous_move = self.escape_direction
            self.move_history.append(self.escape_direction)
            return self.escape_direction

        for move in legal_moves:
            if self.previous_move and move == opposite_directions.get(self.previous_move):
                continue

            dx, dy = direction_deltas[move]
            next_x = pacman_pos[0] + dx
            next_y = pacman_pos[1] + dy
            next_pos = (next_x, next_y)

            score = 0

            for ghost_pos in dangerous_ghosts:
                distance = manhattanDistance(next_pos, ghost_pos)
                if distance <= 1:
                    score -= 1000
                else:
                    bonus = distance * 10
                    score += bonus

            for ghost_pos in scared_ghosts:
                distance = manhattanDistance(next_pos, ghost_pos)
                if distance == 0:
                    score += 2000
                else:
                    if distance < 5:
                        bonus = (5 - distance) * 100
                        score += bonus

            if dangerous_ghosts and capsule_locations:
                capsule_distance = manhattanDistance(next_pos, closest_capsule_location)
                if capsule_distance <= 5:
                    bonus = (5 - capsule_distance) * 50
                    score += bonus

            if closest_food_location:
                food_distance = manhattanDistance(next_pos, closest_food_location)
                food_penalty = food_distance * 5
                score -= food_penalty

            if score > best_score:
                best_score = score
                best_move = move

        if best_move is None and (dangerous_ghosts or scared_ghosts):
            possible_escape_directions = [Directions.NORTH, Directions.SOUTH]
            for escape_dir in possible_escape_directions:
                if escape_dir in legal_moves and escape_dir != opposite_directions.get(self.previous_move):
                    best_move = escape_dir
                    self.escape_direction = escape_dir
                    self.in_escape_mode = True
                    self.escape_direction_pos = (pacman_pos[0] + direction_deltas[escape_dir][0], pacman_pos[1] + direction_deltas[escape_dir][1])
                    if dangerous_ghosts:
                        self.closest_dangerous_distance = min([manhattanDistance(self.escape_direction_pos, ghost_pos) for ghost_pos in dangerous_ghosts])
                    else:
                        self.closest_dangerous_distance = float('inf')
                    self.previous_move = best_move
                    self.move_history.append(best_move)
                    break

        if best_move is None:
            if legal_moves:
                best_move = max(legal_moves, key=lambda move: self.evaluate_move(move, pacman_pos, dangerous_ghosts, scared_ghosts, closest_food_location, closest_capsule_location))
            else:
                best_move = random.choice(legal_moves)

        if best_move:
            self.previous_move = best_move
            if self.in_escape_mode:
                is_safe = all(manhattanDistance((pacman_pos[0] + direction_deltas[best_move][0], pacman_pos[1] + direction_deltas[best_move][1]), ghost_pos) > 1 for ghost_pos in dangerous_ghosts)
                if is_safe:
                    self.in_escape_mode = False
                    self.escape_direction = None
        else:
            best_move = random.choice(legal_moves)
            self.previous_move = best_move

        return best_move

    def evaluate_move(self, move, pacman_pos, dangerous_ghosts, scared_ghosts, closest_food_location, closest_capsule_location):
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

        for ghost_pos in dangerous_ghosts:
            distance = manhattanDistance(next_pos, ghost_pos)
            if distance <= 1:
                score -= 1000
            else:
                score += distance * 10

        for ghost_pos in scared_ghosts:
            distance = manhattanDistance(next_pos, ghost_pos)
            if distance == 0:
                score += 2000
            else:
                if distance < 5:
                    bonus = (5 - distance) * 100
                    score += bonus

        if dangerous_ghosts and closest_capsule_location:
            capsule_distance = manhattanDistance(next_pos, closest_capsule_location)
            if capsule_distance <= 5:
                bonus = (5 - capsule_distance) * 50
                score += bonus

        if closest_food_location:
            food_distance = manhattanDistance(next_pos, closest_food_location)
            score -= food_distance * 5

        return score
