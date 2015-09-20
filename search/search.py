# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"

  from spade import pyxf

  myXSB = pyxf.xsb("/home/raghu/ai/XSB/bin/xsb")
  myXSB.load("maze1.P")
  myXSB.load("dfs.P")
  result = myXSB.query("dfs(start,[],P).")
  #print result
  path = result[0]['P']
  #print path
  #print type(path)
  path_no_null = path[6:-6]
  #print path_no_null
  path_list = path_no_null.split(",")
  #print path_list
  path_upper_list = [word[:1].upper() + word[1:] for word in path_list]
  #print path_upper_list
  return path_upper_list

  #util.raiseNotDefined()

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  from spade import pyxf

  myXSB = pyxf.xsb("/home/raghu/ai/XSB/bin/xsb")

  myXSB.load("maze1.P")
  myXSB.load("bfs.P")
  result1 = myXSB.query("bfs([[start]],P).")
  #print result1
  path = result1[0]['P']
  #print path
  #print type(path)
  path_no_null = path[6:-12]
  #print path_no_null
  path_list = path_no_null.split(",")
  #print path_list
  path_dir = path_list[1::2]
  #print "path_dir " + str(path_dir)
  path_upper_list = [word[:1].upper() + word[1:] for word in path_dir]
  #print path_upper_list
  path_reverse = path_upper_list[::-1]
  print path_reverse
  return path_reverse

  #util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from spade import pyxf

  myXSB = pyxf.xsb("/home/raghu/ai/XSB/bin/xsb")
  myXSB.load("maze_astar.P")
  myXSB.load("astar2.P")
  result1 = myXSB.query("astar1([[start]],P).")
  #print result1
  path = result1[0]['P']
  print path
  #print type(path)
  #path_no_null = path[:-12]
  print path
  path_list = path.split(",")
  print path_list
  path_dir = path_list[1::3]
  print "path_dir " + str(path_dir)
  path_no_null = path_dir[:-1]
  path_upper_list = [word[:1].upper() + word[1:] for word in path_no_null]
  #print path_upper_list
  path_reverse = path_upper_list[::-1]
  #print path_reverse
  return path_reverse

  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch