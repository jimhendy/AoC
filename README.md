# Advent Of Code

My python based stumble through AoC.

Using the great [`advent-of-code-data`](https://github.com/wimglenn/advent-of-code-data) module for automation of inputs and submissions.

Usage:
```
python main.py 2015/01/a.py
```

Solutions can be submitted with the `--submit` flag and test data can be directly used (`--test_input XXX`) or passed through a file (`--test_file test.txt`).
Problems are solved in one file per part (a & b separately) and located with structure `YYYY/DD/PART.py`. The problem code should contain a `run` function which is passed the problem's inputs as a single string. The solution should be returned from the `run` function.

The [`main.py`](main.py) file imports the requested problem code, passes the inputs and submits the solution if requested.

Some commonly used tools are available in [`tools/`](tools/).
