import pygame

"""
The controller functions are used to controll tanks.
Their are part of the game_scenes.
"""


def player1_controller(args):
    """
    Controll a tank by w, a, s, d and alt left
    """
    # mouse_keys = args[0]
    # mouse_pos = args[1]
    keys_pressed = args[2]
    timing_factor = args[3]
    tank = args[4]

    if keys_pressed[pygame.K_w]:
        tank.accelerate(timing_factor)
    if keys_pressed[pygame.K_s]:
        tank.deccelerate(timing_factor)
    if keys_pressed[pygame.K_a]:
        tank.rotate_left(timing_factor)
    if keys_pressed[pygame.K_d]:
        tank.rotate_right(timing_factor)
    if keys_pressed[pygame.K_LALT]:
        tank.shoot(timing_factor)

    # If neither w nor s is pressed the tank should slow down
    if not keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_s]:
        tank.slow_down(timing_factor)


def player2_controller(args):
    """
    Controll a tank by i, k, j, l and space
    """
    # mouse_keys = args[0]
    # mouse_pos = args[1]
    keys_pressed = args[2]
    timing_factor = args[3]
    tank = args[4]

    if keys_pressed[pygame.K_i]:
        tank.accelerate(timing_factor)
    if keys_pressed[pygame.K_k]:
        tank.deccelerate(timing_factor)
    if keys_pressed[pygame.K_j]:
        tank.rotate_left(timing_factor)
    if keys_pressed[pygame.K_l]:
        tank.rotate_right(timing_factor)
    if keys_pressed[pygame.K_SPACE]:
        tank.shoot(timing_factor)

    # If neither i nor k is pressed the tank should slow down
    if not keys_pressed[pygame.K_i] and not keys_pressed[pygame.K_k]:
        tank.slow_down(timing_factor)
