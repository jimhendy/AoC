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
parser.add_argument('solver_file',help='File containing "run(inputs)" function to solve the problem')
parser.add_argument('--submit',action='store_true',help='Submit this solution')
parser.add_argument('--test_input',nargs='*',type=str,help='Test input to pass to solver')
args = parser.parse_args()

if __name__ == '__main__':

    # Extract data form the requested solver file
    solver_file = args.solver_file
    year, day, file_name = solver_file.split(os.path.sep)
    puzzle_code = os.path.splitext(file_name)[0]

    is_test = args.test_input is not None
    
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
        soln = solver.run(os.linesep.join(args.test_input))
    else:
        soln = solver.run(puzzle.input_data)

    print(f'Calculated solution for {solver_file}: "{soln:,.0f}"')

    if args.submit:
        # Submit the answer
        if is_test:
            raise('Not submitting answer as we used the test_input data')
        setattr( puzzle, f'answer_{puzzle_code}', int(soln) )
    
    pass
