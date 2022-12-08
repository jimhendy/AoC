def run(input_data):
    return max(sum(map(int, e.splitlines())) for e in input_data.split("\n\n"))
