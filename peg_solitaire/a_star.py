__author__ = 'Raghu'
import copy
import sys
from Queue import PriorityQueue
import time
from os import listdir
from os.path import isfile, join

# Board index given row and column
def get_index(row, col):
    board_index = [['-', '-', 0, 1, 2, '-', '-'],
                   ['-', '-', 3, 4, 5, '-', '-'],
                   [6, 7, 8, 9, 10, 11, 12],
                   [13, 14, 15, 16, 17, 18, 19],
                   [20, 21, 22, 23, 24, 25, 26],
                   ['-', '-', 27, 28, 29, '-', '-'],
                   ['-', '-', 30, 31, 32, '-', '-']]

    return board_index[row][col]

# Generate all possible successors of a given state of peg-solitaire board
def generate_successors(node, heuristic):
    successors = []
    for row in range(7):
        for i in range(7):
            if i <= 4 and node.state[row][i] == node.state[row][i+1] == 'X' and node.state[row][i+2] == '0':
                new_node = copy.deepcopy(node)
                new_node.state[row][i] = '0'
                new_node.state[row][i + 1] = '0'
                new_node.state[row][i + 2] = 'X'
                new_node.path.append([get_index(row, i), get_index(row, i + 2)])
                new_node.cost = 1
                if heuristic == 'h1':
                    new_node.distance_from_goal = distance_from_goal_h1(new_node.state)
                else:
                    new_node.distance_from_goal = distance_from_goal_h2(new_node.state)
                successors.append(new_node)
            if i <= 4 and node.state[row][i] == '0' and node.state[row][i+1] == node.state[row][i+2] == 'X':
                new_node = copy.deepcopy(node)
                new_node.state[row][i] = 'X'
                new_node.state[row][i + 1] = '0'
                new_node.state[row][i + 2] = '0'
                new_node.path.append([get_index(row, i+2), get_index(row, i)])
                new_node.cost = 1
                if heuristic == 'h1':
                    new_node.distance_from_goal = distance_from_goal_h1(new_node.state)
                else:
                    new_node.distance_from_goal = distance_from_goal_h2(new_node.state)
                successors.append(new_node)
            if i <= 4 and node.state[i][row] == node.state[i+1][row] == 'X' and node.state[i+2][row] == '0':
                new_node = copy.deepcopy(node)
                new_node.state[i][row] = '0'
                new_node.state[i + 1][row] = '0'
                new_node.state[i + 2][row] = 'X'
                new_node.path.append([get_index(i, row), get_index(i+2, row)])
                new_node.cost = 1
                if heuristic == 'h1':
                    new_node.distance_from_goal = distance_from_goal_h1(new_node.state)
                else:
                    new_node.distance_from_goal = distance_from_goal_h2(new_node.state)
                successors.append(new_node)
            if i <= 4 and node.state[i][row] == '0' and node.state[i+1][row] == node.state[i+2][row] == 'X':
                new_node = copy.deepcopy(node)
                new_node.state[i][row] = 'X'
                new_node.state[i + 1][row] = '0'
                new_node.state[i + 2][row] = '0'
                new_node.path.append([get_index(i + 2, row), get_index(i, row)])
                new_node.cost = 1
                if heuristic == 'h1':
                    new_node.distance_from_goal = distance_from_goal_h1(new_node.state)
                else:
                    new_node.distance_from_goal = distance_from_goal_h2(new_node.state)
                successors.append(new_node)
    return successors


def print_successors(successors):
    print('successors:')
    for row in successors:
        for row2 in row:
            print(row2)
        print()

# Check if a node state is the goal
#Compare the states and if equal, print only the path
def goal(node, count):
    final_state = [['-', '-', '0', '0', '0', '-', '-'],
                   ['-', '-', '0', '0', '0', '-', '-'],
                   ['0', '0', '0', '0', '0', '0', '0'],
                   ['0', '0', '0', 'X', '0', '0', '0'],
                   ['0', '0', '0', '0', '0', '0', '0'],
                   ['-', '-', '0', '0', '0', '-', '-'],
                   ['-', '-', '0', '0', '0', '-', '-']]
    if node.state == final_state:
        print'Moves made:', node.path
        print'Number of nodes:', count
        print'Memory utilized:', sys.getsizeof(node) * count, 'bytes'
        return True

#Heuristic 1 : number of pegs left on the board
def distance_from_goal_h1(state):
    count = 0
    for row in range(7):
        for col in range(7):
            if state[row][col] == 'X':
                count += 1
    return count - 1


#Heuristic 2: Manhattan distance - a better heuristic
def distance_from_goal_h2(state):
    m_distance = 0
    for row in range(7):
        for col in range(7):
            if state[row][col] == 'X':
                m_distance += (abs(row - 3) + abs(col - 3))
    return m_distance

#To avoid unorderable type error for comparing nodes, compare the priorities only
class TupleSortingOn0(tuple):
    def __lt__(self, rhs):
        return self[0] < rhs[0]

    def __gt__(self, rhs):
        return self[0] > rhs[0]

    def __le__(self, rhs):
        return self[0] <= rhs[0]

    def __ge__(self, rhs):
        return self[0] >= rhs[0]

# A* search
def a_star_search(node, heuristic):
    fringe = PriorityQueue()
    fringe.put(TupleSortingOn0((node.cost + node.distance_from_goal, node)))
    num_of_nodes = 0
    while not fringe.empty():
        num_of_nodes += 1
        current_node = fringe.get()[1]
        if goal(current_node, num_of_nodes):
            return 'success'
        successors = generate_successors(current_node, heuristic)
        for successor in successors:
            fringe.put(TupleSortingOn0((successor.cost + successor.distance_from_goal, successor)))
    return 'failure'

class Node:
    state = None
    cost = None
    distance_from_goal = None

    def __init__(self, state, cost, distance_from_goal):
        self.state = state
        self.cost = cost
        self.distance_from_goal = distance_from_goal
        self.path = []
        
def main():
    my_path = 'test'
    for f in listdir(my_path):
        if isfile(join(my_path, f)):
            print'file:', f
            input_data = open(join(my_path, f), 'r')
            temp_list = []
            print('start state:')
            for line in input_data:
                temp_line = []
                for character in line.rstrip():
                    temp_line.append(character)
                print(temp_line)
                temp_list.append(temp_line)
            start_state = temp_list
            # print(start_state)
            # print("performing iterative deepening search...")
            # status = iterative_deepening_search(start_state)
            # if status == 'success':
            #     print('solution found!')
            # elif status == 'failure':
            #     print('No solution exists!')

            print("performing A-Star search with heuristics 1")
            heuristic = "h1"
            begin = time.time()
            status = a_star_search(Node(start_state, 0, distance_from_goal_h1(start_state)), heuristic)
            end = time.time()
            if status == 'success':
                print('solution found!')
            elif status == 'failure':
                print('No solution exists!')
            print 'time taken:', (end - begin), 'seconds'
            print('')

            print("performing A-Star search with heuristics 2")
            heuristic = "h2"
            begin = time.time()
            status = a_star_search(Node(start_state, 0, distance_from_goal_h2(start_state)), heuristic)
            end = time.time()
            if status == 'success':
                print('solution found!')
            elif status == 'failure':
                print('No solution exists!')
            print 'time taken:', (end - begin), 'seconds'
            print('')


#starting point of execution

main()




