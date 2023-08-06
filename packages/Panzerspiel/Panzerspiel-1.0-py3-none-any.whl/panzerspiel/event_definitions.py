import pygame

"""
This file contains all user defined events
"""

# The event to throw if a tank shoots. It is thrown by the tank instance
# and handled by the handle_tank_shot function of collision.py
TANK_SHOT_EVENT = pygame.USEREVENT + 1
# This event is thrown by the handle_tank_shot function of collision.py
# and handled by the animator instance inside animator.py
TANK_HIT_EVENT = pygame.USEREVENT + 2
