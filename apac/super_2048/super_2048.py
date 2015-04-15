#!/usr/bin/env python3
import sys
import argparse

def revert_board(board, board_size, move):
    if move == 'right':
        return board
    if move == 'left':
        return reverse_rows(board, board_size)
    if move == 'up':
        board = reverse_rows(board, board_size)
        board = transpose_board(board, board_size)
        return board
    if move == 'down':
        board = transpose_board(board, board_size)
        return board

def orient_board(board, board_size, move):
    if move == 'right':
        return board
    if move == 'left':
        return reverse_rows(board, board_size)
    if move == 'up':
        board = transpose_board(board, board_size)
        board = reverse_rows(board, board_size)
        return board
    if move == 'down':
        board = transpose_board(board, board_size)
        return board

def reverse_columns(board, board_size):
    return list(reversed(board))

def reverse_rows(board, board_size):
    new_board = []
    for i in range(board_size):
        new_board.append(list(reversed(board[i])))
    return new_board

def transpose_board(board, board_size):
    new_board = [[0]*board_size for _ in range(board_size)]
    for i in range(board_size):
        for j in range(board_size):
            new_board[i][j] = board[j][i]
    return new_board

def process_instance(instance):
    board_size = instance['board_size']
    board = instance['board']
    move = instance['move']

    board = orient_board(board, board_size, move)

    for line in board:
        line_with_no_zeros = [x for x in line if x != 0]

        j = len(line_with_no_zeros) - 1
        for i in reversed(range(0 , board_size)):
            if j < 0:
                line[i] = 0
                continue

            if j > 0 and line_with_no_zeros[j] == line_with_no_zeros[j-1]:
                line[i] = 2 * line_with_no_zeros[j]
                j -= 2
            else:
                line[i] = line_with_no_zeros[j]
                j -= 1

    board = revert_board(board, board_size, move)
    output = board_to_string(board, board_size)
    return output

def board_to_string(board, board_size):
    board = [' '.join([str(x) for x in line]) for line in board]
    string = '\n' + '\n'.join(board)
    return string

def parse_file(file_name):
    with open(file_name, mode = 'r', encoding='utf-8') as file_:
        number_of_instances = int(file_.readline())

        instances = []
        for i in range(number_of_instances):
            board_size, move = file_.readline().split()
            board_size = int(board_size)

            board = []
            for j in range(board_size):
                line = [int(x) for x in file_.readline().split()]
                board.append(line)
            instance = {
                    'board_size' : board_size,
                    'board' : board,
                    'move' : move,
                    }
            instances.append(instance)

    return (number_of_instances, instances)

def clean_solution(i, solution):
    solution = 'Case #{}: {}'.format(i, solution)
    print(solution)
    return solution

def get_output_from_solutions(file_name, solutions):
    lines = [clean_solution(i+1, solution) + '\n'
             if i != len(solutions) - 1
             else
             clean_solution(i+1, solution)
             for i, solution in enumerate(solutions)
            ]
    with open(file_name, 'w', encoding='utf-8') as file_:
        file_.writelines(lines)

def print_status(i, total):
    print_string = '\rProcessing {}/{} instances '.format(i+1, total)
    sys.stdout.write(print_string)
    sys.stdout.flush()

if __name__ == '__main__':
    description='Process Problem Name'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_file_name', type=str, help='File to process')
    parser.add_argument('--output_file_name', type=str,
                        help='File to output', default='output')
    args = parser.parse_args()

    number_of_instances, instances = parse_file(args.input_file_name)

    if number_of_instances != len(instances):
        error = 'Expected {} instances | parsed {} instances'
        error = error.format(number_of_instances, len(instances))
        raise Exception(error)

    solutions = []
    for i, instance in enumerate(instances):
        print_status(i, number_of_instances)
        solution = process_instance(instance)
        solutions.append(solution)
    print('\nFinished Processing!')

    get_output_from_solutions(args.output_file_name, solutions)

    print('Done!')
