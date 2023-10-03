# ce811TutorialAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
#
# Adapted for CE811 by M. Fairbank
# Put your agents for the CE811 pacman tutorial in here.

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ce811GoWestAgent(Agent):

  def getAction(self, gameState):
    legalMoves = gameState.getLegalActions()
    #return Directions.WEST
    return random.choice(legalMoves) 

