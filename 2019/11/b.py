import emergency_hull_painting_robot
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

def run(inputs):

    robot = emergency_hull_painting_robot.EhpRobot(inputs, start_color=emergency_hull_painting_robot.Color.WHITE)
    robot.run()

    xy = np.array(
        [
            np.array([int(i) for i in k[1:-1].split()])
            for k,v in robot._colors.items() if v == emergency_hull_painting_robot.Color.WHITE ]
    ).T

    plt.scatter( xy[0], xy[1], s=50 )
    plt.show()

    import code
    code.interact(local=locals())

    result = input('What does it say: ')
    
    return result
