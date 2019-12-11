import emergency_hull_painting_robot as ehpr
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

def run(inputs):

    robot = ehpr.EhpRobot(inputs)
    robot.run()
    
    return len(robot._colors)
