from math import atan2
from panzerspiel.vector import vector


# Global tank settings
MIN_SPEED = 0
MAX_SPEED = 512
MIN_ACCELERATION = 0
MAX_ACCELERATION = 5120
MIN_HEALTH = 1
MAX_HEALTH = 5000
MIN_DPS = 1
MAX_DPS = 700
MIN_FIRE_RATE = 0.1
MAX_FIRE_RATE = 5
MAX_CREDITS = 100
SURGE_FACTOR = 0.9


# This function maps the interval 0 to 1 onto 0 to 0.5 times MAX_CREDITS
# in a squared way
def calculate_upgrade_costs(tank, _min, _max, current):
    x = (current - _min) / (_max - _min)
    tank.credits -= MAX_CREDITS * SURGE_FACTOR * x**1.6
    return tank.credits


# calculate the credit points of the tank
def calculate_credit_points(tank):
    tank.credits = MAX_CREDITS
    calculate_upgrade_costs(tank, MIN_SPEED, MAX_SPEED, tank.max_speed)
    calculate_upgrade_costs(tank, MIN_ACCELERATION, MAX_ACCELERATION, tank.acceleration)
    calculate_upgrade_costs(tank, MIN_HEALTH, MAX_HEALTH, tank.max_health)
    calculate_upgrade_costs(tank, MIN_DPS, MAX_DPS, tank.dps)
    calculate_upgrade_costs(tank, MIN_FIRE_RATE, MAX_FIRE_RATE, tank.fire_rate)


# calculate the steering force
def calculate_steering_force(tank):
    """
    This function is based on some vector geometry, but the correction
    factors 1000 and 100 are made up
    """
    dv = vector(tank.rect.width * 1000, 2 * tank.acceleration)
    phi = atan2(dv.y, dv.x) * 50
    if tank.speed < 0:
        return -phi
    return phi
