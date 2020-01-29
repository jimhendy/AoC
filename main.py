import os
import sys
import aocd
import logging
import argparse
import importlib

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

usage = 'python main.py <YYYY>/<DD>/<P>.py \n e.g. python main.py 2019/01/a.py'

parser = argparse.ArgumentParser(usage=usage)
parser.add_argument(
    'solver_file', help='File containing "run(inputs)" function to solve the problem')
parser.add_argument('--submit', action='store_true',
                    help='Submit this solution')
parser.add_argument('--test_input', nargs='*', type=str,
                    help='Test input to pass to solver')
parser.add_argument('--test_file', help='Use the data store in the passed filename to test the problem')
args = parser.parse_args()

if __name__ == '__main__':

    # Extract data form the requested solver file
    solver_file = args.solver_file
    year, day, file_name = solver_file.split(os.path.sep)
    puzzle_code = os.path.splitext(file_name)[0]

    is_test = (args.test_input is not None) or (args.test_file is not None)

    # Construct the puzzle from aocd
    puzzle = aocd.models.Puzzle(
        year=int(year),
        day=int(day)
    )

    # Add the solver file location to the path
    sys.path.append(os.path.split(solver_file)[0])

    # Import the solver file as "solver"
    solver = importlib.import_module(
        puzzle_code
    )

    # Run the solver with the input_data
    if is_test:
        if args.test_input is not None:
            inputs = os.linesep.join(args.test_input)
        elif args.test_file is not None:
            with open(args.test_file) as f:
                inputs = ''.join(f.readlines())[:-1]
                pass
            pass
        else:
            raise NotImplementedError
        soln = solver.run(inputs)
    else:
        soln = solver.run(puzzle.input_data)
        pass

    is_int = type(soln) == int
    try:
        if int(soln) == soln:
            is_int = True
            pass
        pass
    except:
        pass

    if is_int:
        soln = int(soln)

    print_soln = f'{soln:,.0f}' if is_int else soln
    print(f'Calculated solution for {solver_file}: "{print_soln}"')

    if args.submit:
        # Submit the answer
        if is_test:
            raise('Not submitting answer as we used the test_input data')
        setattr(puzzle, f'answer_{puzzle_code}', soln)

    pass
