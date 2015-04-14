#!/usr/bin/env python3
import sys
import argparse

def process_instance(instance):
    omino_size = instance['omino_size']
    number_of_columns = instance['number_of_columns']
    number_of_rows = instance['number_of_rows']
    
    # With more than 7 peices you can make a donut
    if omino_size >= 7:
        return 'RICHARD'

    # Check if any configuration can fill the board
    if (number_of_columns * number_of_rows) % omino_size != 0:
        return 'RICHARD'

    # Choose the 1 x omino_size omino
    if omino_size > max(number_of_columns, number_of_rows):
        return 'RICHARD'

    # The L shape which maximizes the minimum dimension of the omino is larger
    # than the smaller dimension of the grid
    if -(-omino_size // 2) > min(number_of_columns, number_of_rows):
        return 'RICHARD'

    # Pick the s shaped omino to create a repeating pattern that cannot be
    # filled when minimum dimension is 2
    if omino_size == 4 and min(number_of_columns, number_of_rows) == 2:
        return 'RICHARD'

    # w shape for omino size of 5 cannot fit in 3 x 5
    if (omino_size == 5 and min(number_of_columns, number_of_rows) == 3
                        and max(number_of_columns, number_of_rows) == 5):
        return 'RICHARD'

    # Lopsided T shape with the top having 4 and the body having 3
    if omino_size==6 and min(number_of_columns,number_of_rows)==3:
        return "RICHARD"

    return 'GABRIEL'

def parse_line(line):
    line = line.strip().split(' ')
    omino_size, number_of_rows, number_of_columns = [int(x) for x in line]

    instance = {}
    instance['omino_size'] = omino_size
    instance['number_of_rows'] = number_of_rows
    instance['number_of_columns'] = number_of_columns
    return instance

def clean_solution(i, solution):
    solution = "Case #{}: {}".format(i, solution)
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

def parse_file(file_name):
    with open(file_name, mode = 'r', encoding='utf-8') as file_:
        number_of_instances = int(file_.readline())
        instances = tuple(parse_line(line) for line in file_)
    return (number_of_instances, instances)

def print_status(i, total):
    print_string = "\rProcessing {}/{} instances".format(i+1, total)
    sys.stdout.write(print_string)
    sys.stdout.flush()

if __name__ == '__main__':
    description='Process standing ovation problem'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_file_name', type=str, help='File to process')
    parser.add_argument('--output_file_name', type=str, help='File to output',
                        default='output')
    args = parser.parse_args()

    number_of_instances, instances = parse_file(args.input_file_name)

    if number_of_instances != len(instances):
        print("number of instances != number of instances parsed")
        raise Exception('Invalid number of instances')

    solutions = []
    for i, instance in enumerate(instances):
        print_status(i, number_of_instances)
        solution = process_instance(instance)
        solutions.append(solution)
    print("\nFinished Processing!")

    get_output_from_solutions(args.output_file_name, solutions)

    print("Done!")
