import argparse
import importlib
import logging
import os
import sys
from pathlib import Path

import aocd

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

usage = "python main.py <YYYY>/<DD>/<P>.py \n e.g. python main.py 2019/01/a.py"

parser = argparse.ArgumentParser(usage=usage)
parser.add_argument(
    "solver_file",
    help='File containing "run(inputs)" function to solve the problem',
    type=Path,
)
parser.add_argument("--submit", action="store_true", help="Submit this solution")
parser.add_argument(
    "--test_input",
    nargs="*",
    type=str,
    help="Test input to pass to solver",
)
parser.add_argument(
    "--test_file",
    help="Use the data store in the passed filename to test the problem",
    type=Path,
)
args = parser.parse_args()

if __name__ == "__main__":
    # Extract data form the requested solver file
    year, day, _ = args.solver_file.parts
    puzzle_code = args.solver_file.stem

    is_test = (args.test_input is not None) or (args.test_file is not None)

    # Construct the puzzle from aocd
    puzzle = aocd.models.Puzzle(year=int(year), day=int(day))

    # Add the solver file location to the path
    sys.path.append(str(args.solver_file.parent))

    # Import the solver file as "solver"
    solver = importlib.import_module(puzzle_code)

    # Run the solver with the input_data
    if is_test:
        if args.test_input is not None:
            inputs = os.linesep.join(args.test_input)
        elif args.test_file is not None:
            with args.test_file.open("r") as f:
                inputs = "".join(f.readlines()).rstrip(os.linesep)
        else:
            raise NotImplementedError
        soln = solver.run(inputs)
    else:
        soln = solver.run(puzzle.input_data)

    is_int = isinstance(soln, int)
    try:
        if int(soln) == soln:
            is_int = True
    except ValueError:
        pass

    if is_int:
        soln = int(soln)

    print_soln = f"{soln:,.0f}" if is_int else soln
    info = f'Calculated solution for {args.solver_file}: "{print_soln}"'
    logger.info(info)

    if args.submit:
        # Submit the answer
        if is_test:
            error = "Unable to submit answer as we used the test_input data"
            raise AttributeError(error)
        setattr(puzzle, f"answer_{puzzle_code}", soln)
