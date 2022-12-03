import heapq
import os


def run(input_data):
    heap = []
    this_total = 0
    for line in input_data.split(os.linesep):
        if line := line.strip():
            this_total += int(line)
        else:
            heapq.heappush(heap, this_total)
            this_total = 0
    return sum(heapq.nlargest(3, heap))
