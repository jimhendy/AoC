import os

MAX_IP = 4294967295


def run(inputs):
    ranges = (list(map(int, i.split("-"))) for i in inputs.split(os.linesep))
    ranges = sorted(ranges, key=lambda x: x[0])

    possible_start_good_ip = 0
    total = 0

    for r_min, r_max in ranges:
        if r_min > possible_start_good_ip:
            gap_size = r_min - possible_start_good_ip
            total += gap_size
        possible_start_good_ip = max(r_max + 1, possible_start_good_ip)

    if possible_start_good_ip < MAX_IP:
        total += MAX_IP - possible_start_good_ip

    return total
