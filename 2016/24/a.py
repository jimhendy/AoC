import a_star
import maze


class MazeState(a_star.State):
    def __init__(
        self, maze, current_number, previous_steps=0, collected_numbers=None,
    ) -> None:
        self.maze = maze
        self.current_number = current_number
        self.collected_numbers = [] if collected_numbers is None else collected_numbers
        self.collected_numbers += [current_number]
        self.previous_steps = previous_steps
        super().__init__()

    def is_valid(self):
        return True

    def is_complete(self):
        return len(self.collected_numbers) == len(self.maze.number_locations())

    def __lt__(self, other):
        return self.previous_steps < other.previous_steps

    def all_possible_next_states(self):
        for next_number in self.maze.number_locations():
            if next_number in self.collected_numbers:
                continue
            yield MazeState(
                self.maze,
                next_number,
                self.previous_steps
                + self.maze.steps_between(self.current_number, next_number),
                self.collected_numbers[:],
            )


def run(inputs):
    m = maze.Maze(inputs)
    initial_state = MazeState(m, 0)
    best_route = a_star.a_star(
        initial_state,
        tag_func=lambda x: str(x.collected_numbers),
    )

    return best_route.previous_steps
