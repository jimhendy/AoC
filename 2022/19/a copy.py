import re
from collections import Counter
from functools import lru_cache

from tools.a_star import State, a_star

TIME = 24

ROBOT_REG = re.compile(r"Each (\w+) robot costs (?:(\d+) (\w+))(?: and (\d+) (\w+))?")
BLUEPRINT_REG = re.compile(r"^Blueprint (\d+)")
TARGET_RESOURCE = "geode"


class Config(State):
    __slots__ = ("robots", "resources", "elapsed_time", "chose_not_to_build")

    blueprint: dict[str, Counter[str, int]]  # output_resource: {input_resource: num}
    threshold: int = 0

    def __init__(
        self,
        robots: Counter[str, int],
        resources: Counter[str, int] | None = None,
        elapsed_time: int = 0,
        chose_to_not_build: set[str] | None = None,
    ) -> None:
        self.elapsed_time = elapsed_time
        self.resources = resources or Counter()
        self.robots = robots
        self.chose_to_not_build = chose_to_not_build or set()

    def __str__(self) -> str:
        return f"{self.robots}, {self.resources}, {self.elapsed_time}"

    def is_valid(self) -> bool:
        return Config.would_be_valid(
            robots=self.robots,
            resources=self.resources,
            time_left=self.time_left,
        )

    @staticmethod
    def would_be_valid(
        robots: Counter,
        resources: dict[str, Counter],
        time_left: int,
    ) -> bool:
        assured = resources[TARGET_RESOURCE] + time_left * robots[TARGET_RESOURCE]
        Config.threshold = max(Config.threshold, assured)
        estimate = max(0, time_left - 1)
        return (assured + estimate) >= Config.threshold

    def is_complete(self) -> bool:
        return self.elapsed_time == TIME

    def __lt__(self, other: "Config") -> bool:
        if self.elapsed_time == other.elapsed_time:
            return self.resources[TARGET_RESOURCE] > other.resources[TARGET_RESOURCE]
        return self.elapsed_time < other.elapsed_time

    @property
    @lru_cache(maxsize=1)
    def time_left(self):
        return TIME - self.elapsed_time

    def all_possible_next_states(self):
        new_time = self.elapsed_time + 1
        time_left = TIME - new_time
        could_build = [
            resource
            for resource, required_items in self.blueprint.items()
            if all(self.resources[k] >= v for k, v in required_items.items())
        ]

        spend_nothing = True
        if TARGET_RESOURCE in could_build:
            spend_nothing = False
            could_build = [TARGET_RESOURCE]

        for resource in could_build:
            if resource in self.chose_to_not_build:
                continue

            new_robots = self.robots + Counter({resource: 1})
            new_resources = self.resources + self.robots - self.blueprint[resource]

            if not Config.would_be_valid(
                robots=new_robots,
                resources=new_resources,
                time_left=time_left,
            ):
                continue

            yield Config(
                robots=new_robots,
                resources=new_resources,
                elapsed_time=new_time,
                chose_to_not_build=set(),
            )

        if spend_nothing:
            # Spend nothing this time

            new_resources = self.resources + self.robots

            if Config.would_be_valid(
                robots=self.robots,
                resources=new_resources,
                time_left=time_left,
            ):
                yield Config(
                    robots=self.robots.copy(),
                    resources=new_resources,
                    elapsed_time=new_time,
                    chose_to_not_build=set(could_build) | self.chose_to_not_build,
                )


def run(inputs):
    blueprints = {
        int(BLUEPRINT_REG.findall(bp)[0]): {
            d[0]: Counter({d[i + 1]: int(d[i]) for i in range(1, 5, 2) if d[i]})
            for d in ROBOT_REG.findall(bp)
        }
        for bp in inputs.splitlines()
    }

    total = 0
    for bp_id, bp in blueprints.items():
        print(bp_id)
        # raise
        Config.blueprint = bp
        Config.threshold = 0
        initial_state = Config(robots=Counter({"ore": 1}))
        best_option = a_star(initial_state)  # , tag_func=lambda x: uuid.uuid4())
        total += bp_id * best_option.resources[TARGET_RESOURCE]
        print(best_option.resources)
        # raise
    return total
