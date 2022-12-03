import os
import re


class Reindeer:
    def __init__(self, speed, time, rest):
        self.run_speed = int(speed)
        self.run_time = int(time)
        self.rest_time = int(rest)
        self.run_distance = 0
        self.is_resting = False
        self.run_steps = 0
        self.rest_steps = 0
        self.points = 0
        pass

    def increment_step(self):
        if self.is_resting:
            self.rest_steps += 1
            if self.rest_steps == self.rest_time:
                self.is_resting = False
                self.rest_steps = 0
                pass
            pass
        else:
            self.run_steps += 1
            self.run_distance += self.run_speed
            if self.run_steps == self.run_time:
                self.is_resting = True
                self.run_steps = 0
                pass
            pass
        pass

    pass


def run(inputs):

    reg = re.compile(
        "(\D+) can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds\."
    )

    deer = {}
    for match in reg.findall(inputs.replace(os.linesep, "")):
        deer[match[0]] = Reindeer(match[1], match[2], match[3])
        pass

    for step in range(2503):
        [d.increment_step() for d in deer.values()]
        pass

    best_deer = sorted(deer.items(), key=lambda x: x[1].run_distance)[-1][1]

    return best_deer.run_distance
