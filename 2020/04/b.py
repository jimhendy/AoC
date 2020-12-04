import os
import re


def check_int(value, min_value, max_value):
    value = int(value)
    assert value <= max_value
    assert value >= min_value


def is_valid(passport):
    try:
        check_validity(passport)
        return True
    except:
        return False


def check_validity(passport):
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    assert all([f in passport.keys() for f in fields])

    check_int(passport["byr"], 1920, 2002)
    check_int(passport["iyr"], 2010, 2020)
    check_int(passport["eyr"], 2020, 2030)

    hgt_reg = re.findall(r"^(\d+)(in|cm)$", passport["hgt"])[0]
    if hgt_reg[1] == "cm":
        check_int(hgt_reg[0], 150, 193)
    else:
        check_int(hgt_reg[0], 59, 76)

    assert re.match(r"^#[0-9a-f]{6}$", passport["hcl"])
    assert passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    assert re.match(r"^\d{9}$", passport["pid"])


def run(inputs):
    total = 0
    data = {}
    for line in inputs.split(os.linesep):
        if not line.strip():
            if is_valid(data):
                total += 1
            data = {}
            continue
        for d in line.split():
            data[d.split(":")[0].strip()] = d.split(":")[1].strip()

    if is_valid(data):
        total += 1

    return total
