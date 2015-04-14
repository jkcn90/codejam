#!/usr/bin/env python3
import sys
import argparse

def process_instance(instance):
    input(instance)
    return 'Solution'

def parse_instance(line):
    line = line.strip()
    instance = {}
    number_of_values, list_of_values = line.split()

    # cleanup number_of_values
    number_of_values = int(number_of_values)
    instance['number_of_values'] = number_of_values

    # cleanup list of values
    list_of_values = [int(x) for x in list(list_of_values)]
    instance['list_of_values'] = list_of_values

    list_of_values_length = len(list_of_values)
    if number_of_values != list_of_values_length:
        error = 'Expected {} values | {} values parsed'
        error = error.format(number_of_values, list_of_values_length)
        raise Exception(error)
    return instance

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

def parse_file(file_name):
    with open(file_name, mode = 'r', encoding='utf-8') as file_:
        number_of_instances = int(file_.readline())
        lines = [line for line in file_]

        # Allows for cases where one instances can span multiple lines
        instances = [parse_instance(lines[i])
                     for i in range(number_of_instances)]
    return (number_of_instances, instances)

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
