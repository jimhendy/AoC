import os
import re


class Reindeer:
    def __init__(self, speed, time, rest) -> None:
        self.run_speed = int(speed)
        self.run_time = int(time)
        self.rest_time = int(rest)
        self.run_distance = 0
        self.is_resting = False
        self.run_steps = 0
        self.rest_steps = 0
        self.points = 0

    def increment_step(self):
        if self.is_resting:
            self.rest_steps += 1
            if self.rest_steps == self.rest_time:
                self.is_resting = False
                self.rest_steps = 0
        else:
            self.run_steps += 1
            self.run_distance += self.run_speed
            if self.run_steps == self.run_time:
                self.is_resting = True
                self.run_steps = 0


def run(inputs):
    reg = re.compile(
        r"(\D+) can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds\.",
    )

    deer = {}
    for match in reg.findall(inputs.replace(os.linesep, "")):
        deer[match[0]] = Reindeer(match[1], match[2], match[3])

    for _step in range(2503):
        [d.increment_step() for d in deer.values()]

        max_distance = max([d.run_distance for d in deer.values()])
        for d in deer.values():
            if d.run_distance == max_distance:
                d.points += 1

    best_deer = sorted(deer.items(), key=lambda x: x[1].points)[-1][1]

    return best_deer.points
