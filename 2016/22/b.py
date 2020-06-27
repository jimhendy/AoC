import re
import time
import os
import a_star
import numpy as np
import pandas as pd
from functools import lru_cache

# Cluster arrays indexed y,x

@lru_cache(maxsize=2048)
def _metric_calc(zp_0, zp_1, dp_0, dp_1):
    zp = np.array((zp_0, zp_1))
    dp = np.array((dp_0, dp_1))
    total = 0

    while not np.array_equal(dp, (0, 0)):
        #print_zp_dp(zp, dp)
        # if we can move the data into the space left or up then do it
        if zp[0] == dp[0] and zp[1] == dp[1] - 1:
            # left
            dp[1] -= 1
            zp[1] += 1
            total += 1
            continue
        elif zp[1] == zp[1] and zp[0] == dp[0] - 1:
            # up
            dp[0] -= 1
            zp[1] += 1
            total += 1
            continue

        # if space is either on the right or below then move to top or left respectivly
        if dp[1] and zp[0] == dp[0] + 1 and zp[1] == dp[1]:
            # Below, move to left and swap with data
            zp[0] -= 1
            dp[1] -= 1
            total += 3
            continue
        elif dp[0] and zp[1] == dp[1] + 1 and zp[0] == dp[0]:
            # Right, move above and swap
            zp[1] -= 1
            dp[0] -= 1
            total += 3
            continue

        # if data is on top row with space to the right
        if dp[0] == 0 and zp[0] == 0 and (dp[1] == (zp[1]-1)):
            total += 5 * dp[1]
            zp[1] = 1
            dp[1] = 0
            continue
        elif dp[1] == 0 and zp[1] == 0 and (dp[0] == (zp[0]-1)):
            total += 5 * dp[0]
            zp[0] = 1
            dp[0] = 0
            continue

        #If space is nearby data
        if np.array_equal(zp, dp + 1):
            # diagonally below & right
            if dp[0] == 0:
                # Top row
                zp[1] -= 1
                total += 1
                continue
            elif dp[1] != 0:
                # Not left column
                zp[0] -= 1
                total += 1
                continue

        # Else move the space towards to data
        if zp[0] > dp[0] + 1:
            # If far below, move space up
            zp[0] -= 1
            total += 1
            continue
        elif zp[1] < dp[1] - 1:
            # If far to the left, move space right
            zp[1] += 1
            total += 1
            continue
        elif zp[0] < dp[0] - 1:
            # If far above, move space down
            zp[0] += 1
            total += 1
            continue
        elif zp[1] > dp[1] + 1:
            # If far to the right, move space left
            zp[1] -= 1
            total += 1
            continue
        elif zp[0] == dp[0] + 1 and np.abs(zp[1] - dp[1]) == 1:
            # If below and diagonal move up
            zp[0] -= 1
            total += 1
            continue
        elif zp[0] == dp[0] - 1 and np.abs(zp[1] - dp[1]) == 1:
            zp[1] += np.sign(zp[1]-dp[1])
            total += 1
            continue

        print("Failed")
        print(zp)
        print(dp)
        print(total)

        import pdb

        pdb.set_trace()

    return total

def print_zp_dp(zp, dp):
    used = np.full((max((zp[0], dp[0]))+1, max((zp[1], dp[1]))+1), 40)
    used[zp[0], zp[1]] = 0
    print_grid(used, dp)


def print_grid(used, dp):
    out = ''
    for y,row in enumerate(used):
        for x,cell in enumerate(row):
            if np.array_equal((y,x), dp):
                c = 'X'
            elif cell == 0:
                c = '0'
            elif cell > 100:
                c = '#'
            else: c = '.'
            out += c
        out += '\n'
    os.system('clear')
    print(out)


class Status(a_star.State):
    def __init__(self, sizes, used, goal_data_loc, n_steps):
        super().__init__()
        #print_grid(used, goal_data_loc)
        self.sizes = sizes
        self.used = used
        self.goal_data_loc = goal_data_loc
        self.n_steps = n_steps

    def is_valid(self):
        return np.all(self.sizes >= self.used)

    def is_complete(self):
        return np.array_equal(self.goal_data_loc, (0, 0))

    def metric(self):
        # Potential moves to completion
        data_pos = self.goal_data_loc.copy()
        totals = [ 
            _metric_calc(zp[0], zp[1], data_pos[0], data_pos[1]) 
            for zp in np.argwhere(self.used == 0)
        ]
        return min(totals)

    def __lt__(self, other):
        m = self.metric() + self.n_steps
        om = other.metric() + other.n_steps
        return m < om

    def all_possible_next_states(self):
        print_grid(self.used, self.goal_data_loc)
        avail = self.sizes - self.used
        for y in range(self.sizes.shape[0]):
            for x in range(self.sizes.shape[1]):

                # loop over cells to move FROM
                if self.used[y][x] == 0:
                    continue

                for dx in (-1, 0, 1):
                    if dx == -1 and x == 0:
                        continue
                    if dx == 1 and x == self.sizes.shape[1] - 1:
                        continue

                    for dy in (-1, 0, 1):
                        if dx and dy:
                            continue
                        if dy == -1 and y == 0:
                            continue
                        if dy == 1 and y == self.sizes.shape[0] - 1:
                            continue

                        if avail[y + dy][x + dx] >= self.used[y][x]:

                            used_copy = self.used.copy()
                            used_copy[y + dy][x + dx] += used_copy[y][x]
                            used_copy[y][x] = 0

                            if np.array_equal(self.goal_data_loc, (y, x)):
                                new_goal_data_loc = np.array((y + dy, x + dx))
                            else:
                                new_goal_data_loc = self.goal_data_loc

                            yield Status(
                                self.sizes,
                                used_copy,
                                new_goal_data_loc,
                                self.n_steps + 1,
                            )


def run(inputs):

    reg = re.compile(
        r"\/dev\/grid\/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)\%"
    )
    data = []
    for m in reg.findall(inputs):
        data.append(
            {
                "x": int(m[0]),
                "y": int(m[1]),
                "size": int(m[2]),
                "used": int(m[3]),
                "avail": int(m[4]),
                "use": int(m[5]),
            }
        )
    df = pd.DataFrame(data)
    df_p = df.pivot_table(index="y", columns="x", values=["size", "used"])
    sizes = df_p["size"].values
    used = df_p.used.values

    initial_state = Status(sizes, used, np.array((df.y.min(), df.x.max())), 0)
    tag_func = lambda x: str(x.goal_data_loc) + '_' + str(np.argwhere(x.used==0))

    result = a_star.a_star(initial_state, tag_func)

    return result.n_steps
