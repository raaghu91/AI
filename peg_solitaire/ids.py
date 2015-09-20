__author__ = 'Raghu'
import sys
from os import listdir
import time
from os.path import isfile, join
import copy
from Queue import PriorityQueue

# Board index given row and column
def get_index(row, col):
    board_index = [['-', '-', 0, 1, 2, '-', '-'],
                   ['-', '-', 3, 4, 5, '-', '-'],
                   [6, 7, 8, 9, 10, 11, 12],
                   [13, 14, 15, 16, 17, 18,19],
                   [20, 21, 22, 23, 24, 25, 26],
                   ['-', '-', 27, 28, 29, '-', '-'],
                   ['-', '-', 30, 31, 32, '-', '-']]

    return board_index[row][col]

# Generate all possible successors of a given state of peg-solitaire board
def generate_successors(state):
    successors = []
    for row in range(7):
        for i in range(7):
            if i <= 4 and state[row][i] == state[row][i + 1] == 'X' and state[row][i + 2] == '0':
                new_state = copy.deepcopy(state)
                new_state[row][i] = '0'
                new_state[row][i + 1] = '0'
                new_state[row][i + 2] = 'X'
                new_state.append([get_index(row, i), get_index(row, i + 2)])
                successors.append(new_state)
            if i <= 4 and state[row][i] == '0' and state[row][i + 1] == state[row][i + 2] == 'X':
                new_state = copy.deepcopy(state)
                new_state[row][i] = 'X'
                new_state[row][i + 1] = '0'
                new_state[row][i + 2] = '0'
                new_state.append([get_index(row, i + 2), get_index(row, i)])
                successors.append(new_state)
            if i <= 4 and state[i][row] == state[i+1][row] == 'X' and state[i+2][row] == '0':
                new_state = copy.deepcopy(state)
                new_state[i][row] = '0'
                new_state[i + 1][row] = '0'
                new_state[i + 2][row] = 'X'
                new_state.append([get_index(i, row), get_index(i+2, row)])
                successors.append(new_state)
            if i <= 4 and state[i][row] == '0' and state[i + 1][row] == state[i + 2][row] == 'X':
                new_state = copy.deepcopy(state)
                new_state[i][row] = 'X'
                new_state[i + 1][row] = '0'
                new_state[i + 2][row] = '0'
                new_state.append([get_index(i + 2, row), get_index(i, row)])
                successors.append(new_state)
    return successors


def print_successors(successors):
    print('successors:')
    for row in successors:
        for row2 in row:
            print(row2)
        print()

# Check if a node state is the goal
#Compare the states and if equal, print only the path

num_of_nodes = 0

def goal(node):
    global num_of_nodes
    num_of_nodes += 1
    final_state = [['-', '-', '0', '0', '0', '-', '-'],
                   ['-', '-', '0', '0', '0', '-', '-'],
                   ['0', '0', '0', '0', '0', '0', '0'],
                   ['0', '0', '0', 'X', '0', '0', '0'],
                   ['0', '0', '0', '0', '0', '0', '0'],
                   ['-', '-', '0', '0', '0', '-', '-'],
                   ['-', '-', '0', '0', '0', '-', '-']]
    if node[:7] == final_state:
        print'Moves made:', node[7:]
        print'Number of nodes:', num_of_nodes
        print'Memory utilized:', sys.getsizeof(node) * num_of_nodes, 'bytes'
        return True

# For a given node, search it's successors recursively till the depth 'limit'
def depth_limited_search(node, limit, current_depth):
    cutoff_occurred = False
    if goal(node):
        print("solution found at depth:", current_depth)
        return 'success'
    elif current_depth == limit:
        return 'cutoff'
    successors = generate_successors(node)
    for successor in successors:
        result = depth_limited_search(successor, limit, current_depth + 1)
        if result == 'cutoff':
            cutoff_occurred = True
        elif result != 'failure':
            return result
    if cutoff_occurred:
        return 'cutoff'
    else:
        return 'failure'

# Beginning of iterative deepening search
def iterative_deepening_search(initial_state):
    for depth in range(1000000):
        # print("depth limit:",depth)
        result = depth_limited_search(initial_state, depth, 0)
        if result != 'cutoff':
            return result
    print('search space tending to infinity')


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

        print("performing iterative deepening search...")
        begin = time.time()
        status = iterative_deepening_search(start_state)
        end = time.time()
        if status == 'success':
            print('solution found!')
        elif status == 'failure':
            print('No solution exists!')
        print 'time taken:', (end - begin), 'seconds'
        print('')


#starting point of execution
main()




