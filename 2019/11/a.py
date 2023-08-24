import emergency_hull_painting_robot as ehpr


def run(inputs):

    robot = ehpr.EhpRobot(inputs)
    robot.run()

    return len(robot._colors)
