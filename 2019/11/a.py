import emergency_hull_painting_robot as ehpr
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns


def run(inputs):

    robot = ehpr.EhpRobot(inputs)
    robot.run()

    return len(robot._colors)
