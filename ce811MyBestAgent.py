from game import Directions
from game import Agent
from game import Actions
import random

class ce811MyBestAgent(Agent):
  def getAction(self, gameState):
    legalMoves = gameState.getLegalActions()
    return random.choice(legalMoves) # Pick randomly among the best