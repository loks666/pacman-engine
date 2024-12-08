# python pacman.py -p ce811OneStepLookaheadManhattanAgent -n 10 -q -f

from game import Directions
from game import Agent
from util import manhattanDistance
import random

class ce811OneStepLookaheadManhattanAgent(Agent):
    """
      A one-step lookahead agent which chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
    """

    def getAction(self, gameState):
        """
        Just like in the tutorial, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluateBoardState(gameState.generatePacmanSuccessor(action)) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def evaluateBoardState(self, gameState):
        """
        Evaluate the desirability of a given game state.

        We start from the gameState's built-in score, then adjust it based on:
        - Distances to non-scared ghosts (farther is better)
        - Distances to scared ghosts (closer is better if we can eat them)
        - Distance to the nearest food (closer is better)
        - Distance to the nearest capsule (closer is better)
        - The fewer the food items left, the better (although this is indirectly handled via the state score)
        """

        # Useful information from the state
        pacman_pos = gameState.getPacmanPosition()
        food_positions = gameState.getFood().asList()
        ghost_states = gameState.getGhostStates()
        capsule_positions = gameState.getCapsules()

        # Current score as baseline
        evaluation = gameState.getScore()

        # Distances to food
        if len(food_positions) > 0:
            food_distances = [manhattanDistance(pacman_pos, food_pos) for food_pos in food_positions]
            min_food_distance = min(food_distances)
        else:
            min_food_distance = 0

        # Distances to ghosts
        ghost_scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
        ghost_positions = [ghostState.getPosition() for ghostState in ghost_states]

        # Separate ghosts into scared and dangerous
        dangerous_ghost_distances = []
        scared_ghost_distances = []
        for (g_pos, s_time) in zip(ghost_positions, ghost_scared_times):
            dist = manhattanDistance(pacman_pos, g_pos)
            if s_time > 1:
                # Ghost is scared enough to be eaten
                scared_ghost_distances.append(dist)
            else:
                # Ghost is dangerous
                dangerous_ghost_distances.append(dist)

        # Distances to capsules
        if len(capsule_positions) > 0:
            capsule_distances = [manhattanDistance(pacman_pos, cap_pos) for cap_pos in capsule_positions]
            min_capsule_distance = min(capsule_distances)
        else:
            min_capsule_distance = 0

        # --- Heuristics ---

        # 1. Prefer being closer to food:
        # If min_food_distance > 0, we slightly penalize states where the nearest food is far.
        # Using a negative factor: the farther the food, the worse the evaluation.
        evaluation -= 2 * min_food_distance

        # 2. Dangerous ghosts:
        # We want to strongly avoid being close to dangerous ghosts.
        # A reciprocal-based penalty works well: closer ghosts = higher penalty.
        for dist in dangerous_ghost_distances:
            if dist == 0:
                # Being on the same cell as a dangerous ghost is game-ending
                evaluation -= 1000
            else:
                evaluation -= 30.0 / dist  # The closer a dangerous ghost, the more we penalize

        # 3. Scared ghosts:
        # If ghosts are scared, being closer is beneficial (we can potentially eat them).
        # Encourage chasing scared ghosts if they are reachable.
        for dist in scared_ghost_distances:
            if dist > 0:
                evaluation += 20.0 / dist

        # 4. Capsules:
        # Capsules allow us to scare ghosts, so it's usually good to go towards them.
        # We'll give a small incentive to be closer to capsules.
        if min_capsule_distance > 0:
            evaluation += 5.0 / (min_capsule_distance + 1)

        return evaluation
