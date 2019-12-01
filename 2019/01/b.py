import common
import a
import logging

logger = logging.getLogger()

iteration = 0

def log_new_fuel(total_new_fuel):
    global iteration
    iteration += 1
    logger.info(f'Iteration: {iteration:02d}, extra fuel: {total_new_fuel:,.2f}')
    pass

def run(inputs):
    
    fuel_for_modules = a.run(inputs)
    previous_iteration = fuel_for_modules
    total_fuel = previous_iteration.sum()
    log_new_fuel(total_fuel)
    
    while True:
        new_fuel = common.calculate_fuel(previous_iteration)
        total_new_fuel = new_fuel.sum()
        if total_new_fuel == 0:
            break
        log_new_fuel(total_new_fuel)
        total_fuel += total_new_fuel
        previous_iteration = new_fuel
        pass
    
    return total_fuel

    
