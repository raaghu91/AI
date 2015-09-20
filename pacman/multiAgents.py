# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys
import math
import time
from operator import itemgetter

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legal_actions = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legal_actions]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_actions[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        pacman_scared = 0

        if newScaredTimes[0] == 0:
            pacman_scared = 1
        # if only pacman is scared return very low value for the action or else pacman just move without caring about the ghosts
        if(pacman_scared):
            for newGhostState in newGhostStates:
                if(math.sqrt((newGhostState.getPosition()[0] - newPos[0])**2 + (newGhostState.getPosition()[1] - newPos[1])**2) <= 1):
                    return -float("inf")
        new_food_count = 0
        current_food_count = 0

        # check for the food count in the new action state
        for new_food, current_food in zip(newFood.asList(), currentGameState.getFood().asList()):
            for x,y in zip(new_food, current_food):
                if x is True:
                    new_food_count += 1
                if y is True:
                    current_food_count += 1

        # Eat food
        if new_food_count < current_food_count:
            return float("inf")
        shortest_food_distance = -float("inf")

        # Move towards food
        for i,food in enumerate(newFood):
            for j,x in enumerate(food):
                if x is True:
                    if(math.sqrt((newPos[0] - i) ** 2 + (newPos[1] - j) ** 2) < shortest_food_distance):
                        shortest_food_distance = math.sqrt((newPos[0] - i) ** 2 + (newPos[1] - j) ** 2)
        return 1/shortest_food_distance



def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    node_count = 0
    def mini_max(self, gameState, current_depth, agentIndex):
        if current_depth > self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # updating agent index and depth
        next_agent_index = agentIndex + 1
        next_depth = current_depth
        # after all ghosts are done start again with pacman
        if next_agent_index >= gameState.getNumAgents():
            next_agent_index = 0
            next_depth += 1


        legal_actions = [action for action in gameState.getLegalActions(agentIndex)]

        results = []
        for action in legal_actions:
            self.node_count += 1
            results.append(self.mini_max( gameState.generateSuccessor(agentIndex, action), next_depth, next_agent_index))
        # pacman's first move
        if agentIndex == 0 and current_depth == 1:
            best_action = max(results)
            bestIndices = []
            for index in range(len(results)):
                if results[index] == best_action:
                    bestIndices.append(index)
            chosenIndex = random.choice(bestIndices)
            return legal_actions[chosenIndex]
        # MAX node
        if agentIndex == 0:
            best_action = max(results)
            return best_action
        # MIN node
        else:
            best_action = min(results)
            return best_action

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        # print("depth", self.depth)

        # min_max_values = []
        # # for each ghost
        # for ghost_index in range(1, gameState.getNumAgents()):
        #     min_max_values.append(self.min_max_value(gameState, ghost_index, self.depth))
        # return max(min_max_values, key = itemgetter(0))[1]
        # no_of_ghosts = gameState.getNumAgents() - 1
        # pacman_move = self.min_max(gameState, self.depth * (no_of_ghosts + 1) + 1, 0)[1]

        # return action associated with the max min_max_value got.
        # util.raiseNotDefined()
        begin = time.time()
        return_value = self.mini_max(gameState, 1, 0 )
        end = time.time()
        print 'time taken:', (end - begin), 'seconds'
        print'Number of nodes:', self.node_count
        print'Memory utilized:', sys.getsizeof(gameState) * self.node_count, 'bytes'
        return return_value








class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    node_count = 0
    def alpha_beta_search(self, gameState, current_depth, agentIndex, alpha, beta):
        # terminal condition check
        if current_depth > self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        legal_actions = [action for action in gameState.getLegalActions(agentIndex)]

        next_agent_index = agentIndex + 1
        next_depth = current_depth
        if next_agent_index >= gameState.getNumAgents():
            next_agent_index = 0
            next_depth += 1
        # pacman's first move
        if agentIndex == 0 and current_depth == 1:
            self.node_count += 1
            results = [self.alpha_beta_search(gameState.generateSuccessor(agentIndex, action) , next_depth, next_agent_index, alpha, beta) for action in legal_actions]
            best_action = max(results)
            bestIndices = []
            for index in range(len(results)):
                if results[index] == best_action:
                    bestIndices.append(index)
            chosenIndex = random.choice(bestIndices)
            return legal_actions[chosenIndex]

        # MAX's move
        if agentIndex == 0:
            best_action = -float("inf")
            for action in legal_actions:
                self.node_count += 1
                best_action = max(best_action, self.alpha_beta_search( gameState.generateSuccessor(agentIndex, action) , next_depth, next_agent_index, alpha, beta))
                if best_action >= beta:
                    return best_action
                alpha = max(alpha, best_action)
            return best_action
        # MIN's move
        else:
            best_action = float("inf")
            for action in legal_actions:
                self.node_count += 1
                best_action = min(best_action, self.alpha_beta_search( gameState.generateSuccessor(agentIndex, action) , next_depth, next_agent_index, alpha, beta))
                if alpha >= best_action:
                    return best_action
                beta = min(beta, best_action)
            return best_action
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        begin = time.time()
        return_value = self.alpha_beta_search(gameState, 1, 0, -float("inf"), float("inf"))
        end = time.time()
        print 'time taken:', (end - begin), 'seconds'
        print'Number of nodes:', self.node_count
        print'Memory utilized:', sys.getsizeof(gameState) * self.node_count, 'bytes'
        return return_value


        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

