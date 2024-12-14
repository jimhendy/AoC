import sympy


def run(inputs: str) -> int:
    particles = []
    velocities = []
    for line in inputs.splitlines():
        p, v = line.split("@")
        particles.append(list(map(int, p.split(","))))
        velocities.append(list(map(int, v.split(","))))

    particles = particles[:10]

    # Define the unknowns for the rock's initial position (rx, ry, rz) and velocity (vx, vy, vz)
    rx, ry, rz, vx, vy, vz = sympy.symbols("rx ry rz vx vy vz", real=True, integer=True)
    interception_times = sympy.symbols(
        f"t:{len(particles)}",
        real=True,
        integer=True,
        positive=True,
    )

    # List to store the system of equations
    equations = []

    # For each hailstone, calculate the system of equations for each dimension (x, y, z)
    for h in range(len(particles)):
        t = interception_times[h]

        eq_x = sympy.Eq(rx + t * vx, particles[h][0] + t * velocities[h][0])
        eq_y = sympy.Eq(ry + t * vy, particles[h][1] + t * velocities[h][1])
        eq_z = sympy.Eq(rz + t * vz, particles[h][2] + t * velocities[h][2])

        # Add the equations to the system
        equations.extend([eq_x, eq_y, eq_z])

    initial_guess = (0, 0, 0, 1, 1, 1) + tuple(range(1, len(particles) + 1))

    # Solve the system of equations to find the initial position and velocity of the rock
    solution = sympy.solve(equations, (rx, ry, rz, vx, vy, vz) + interception_times)[
        0
    ]  # , initial_guess)

    # Display the solution
    print("Solution for the initial position and velocity of the rock:", solution)

    # Calculate the sum of the x, y, z coordinates of the initial position if the solution exists
    if solution:
        total_position_sum = solution[0] + solution[1] + solution[2]
        print("Sum of the initial position coordinates (x, y, z):", total_position_sum)

        return total_position_sum
