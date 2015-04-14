#!/usr/bin/env python3
import sys
import argparse

def process_instance(instance):
    print()
    number_of_cases = instance['number_of_cases']
    cases = instance['cases']

    possible_next_numbers = []
    for mask in reversed(range(2**7)):
        for i in range(10):
            guess = list((x - i) % 10 for x in reversed(range(number_of_cases)))
            masked_guess = [mask_number(x, mask) for x in guess]

            match = [masked_guess[i] == cases[i] for i in range(number_of_cases)]
            if all(match):
                last_number = guess[-1]
                next_number = (last_number - 1) % 10
                masked_next_number = mask_number(next_number, mask)
                possible_next_numbers.append(masked_next_number)

    possible_next_numbers = list(set(possible_next_numbers))
    if len(possible_next_numbers) == 1:
        return possible_next_numbers[0]

    return 'ERROR!'

def mask_number(number, mask):
    string = string_to_number(number, from_type='number')
    binary_number = int(string, 2)
    masked_number = binary_number & mask
    return '{:07b}'.format(masked_number)

def string_to_number(key, from_type='string'):
    string_to_number_map = {
            '1111011' : 9,
            '1111111' : 8,
            '1110000' : 7,
            '1011111' : 6,
            '1011011' : 5,
            '0110011' : 4,
            '1111001' : 3,
            '1101101' : 2,
            '0110000' : 1,
            '1111110' : 0,
            }

    if from_type == 'string':
        if key in string_to_number_map:
            return string_to_number_map[key]
        else:
            return None
    elif from_type == 'number':
        number_to_string_map = {v:k for k,v in string_to_number_map.items()}
        if key in number_to_string_map:
            return number_to_string_map[key]
        else:
            raise('Invalid number {} (must be 0-9)'.format(key))
    else:
        print("from_type must be 'string' | 'number'")
        raise Exception("Invalid from_type={}".format(from_type))

def parse_line(line):
    line = line.strip()
    instance = {}
    line_array = line.split()
    number_of_cases = line_array[0]
    cases = line_array[1:]

    # cleanup number_of_cases
    number_of_cases = int(number_of_cases)
    instance['number_of_cases'] = number_of_cases

    # cleanup cases
    instance['cases'] = cases

    cases_length = len(cases)
    if number_of_cases != cases_length:
        print("num cases= {}|list = {}".format(number_of_cases, cases_length))
        raise Exception("Number of cases does not match cases list")
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
    print_string = "\rProcessing {}/{} instances ".format(i+1, total)
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
