import emergency_hull_painting_robot
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

def run(inputs):

    robot = emergency_hull_painting_robot.EhpRobot(inputs)
    robot.run()

    xy = np.array(
        [
            np.array([int(i) for i in k[1:-1].split()])
            for k,v in robot._colors.items() if v == emergency_hull_painting_robot.Color.WHITE ]
    ).T

    ##sns.heatmap(xy)
    #plt.show()
    
    import code
    code.interact(local=locals())
    
    return len(robot._colors)
