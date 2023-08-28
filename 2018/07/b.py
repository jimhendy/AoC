import re

N_WORKERS = 5


class Worker:
    worker_num = 0

    def __init__(self) -> None:
        self.worker_id = Worker.worker_num
        Worker.worker_num += 1
        self.active_task = None

    def busy(self):
        return self.active_task is not None

    def start_task(self, task):
        assert self.active_task is None
        self.active_task = task
        self.active_task.active = True

    def step(self):
        if self.active_task is not None:
            self.active_task.step()
            if self.active_task.complete:
                self.active_task = None


class Task:
    def __init__(self, task_id) -> None:
        self.task_id = task_id
        self.total_time = 60 + ord(self.task_id) - 64
        self.remaining_time = self.total_time
        self.active = False
        self.complete = False
        self.pre_tasks = []

    def step(self):
        if self.active:
            self.remaining_time -= 1
            if self.remaining_time == 0:
                self.complete = True
                self.active = False

    def pre_tasks_complete(self):
        return len(self.pre_tasks) == 0 or all(t.complete for t in self.pre_tasks)

    def add_pre(self, other):
        self.pre_tasks.append(other)

    def __repr__(self) -> str:
        return self.task_id

    def __lt__(self, other):
        return self.task_id < other.task_id

    def __gt__(self, other):
        return not self.__lt__(other)


def run(inputs):
    tasks = {}

    for i in re.findall(
        r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.",
        inputs,
    ):
        for t_id in i:
            if t_id not in tasks:
                tasks[t_id] = Task(t_id)
        tasks[i[1]].add_pre(tasks[i[0]])

    workers = [Worker() for _ in range(N_WORKERS)]
    tasks = list(tasks.values())

    time = -1
    while not all(t.complete for t in tasks):
        [w.step() for w in workers]
        time += 1
        if all(w.busy() for w in workers):
            continue
        # Some space for new tasks if any available
        available = sorted(
            [
                t
                for t in tasks
                if not t.complete and not t.active and t.pre_tasks_complete()
            ],
        )
        if not len(available):
            continue
        available_i = 0
        for w in workers:
            if not w.busy():
                w.start_task(available[available_i])
                available_i += 1
                if available_i == len(available):
                    break

    return time
