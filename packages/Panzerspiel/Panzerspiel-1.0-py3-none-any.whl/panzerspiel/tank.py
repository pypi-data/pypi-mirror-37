import pygame
from panzerspiel import vector
from panzerspiel import tank_config as tc
import random
from math import pi
from math import sin
from math import cos
from panzerspiel.global_settings import (SCREEN_DIMENSION, BOX_SIZE)
from panzerspiel.event_definitions import TANK_SHOT_EVENT

# This list will hold all tanks in play
TANKS = []


class tank(pygame.sprite.Sprite):
    """
    The tank class is fully configurable by the customizable menu
    Tanks are controlled by controller instances which process user input
    """
    def __init__(self, image, rect, rotation):
        super().__init__()
        # Configurable parameters
        self.max_speed = tc.MIN_SPEED
        self.acceleration = tc.MIN_ACCELERATION
        self.max_health = tc.MIN_HEALTH
        self.dps = tc.MIN_DPS
        self.fire_rate = tc.MIN_FIRE_RATE
        self.reload_time = 1.0 / self.fire_rate
        # Current state variables
        self.speed = 0
        self.health = self.max_health
        self.credits = tc.MAX_CREDITS
        self.dead = False
        self.reload_timer = 0.0
        self.velocity = vector.vector(0, 0)
        # The rotation is in rad
        self.rotation = rotation
        self.angle = self.rotation
        self.position = vector.vector(rect.x, rect.y)
        # Functional variables
        self.image = image
        self.rect = rect
        self.angle_in_deg = (self.angle / pi) * 180.0
        # Render variables
        # As the rotation is in rad but the transform module deals with
        # degree the rotation has to be converted
        self.rotated_image = pygame.transform.rotate(self.image,
                (self.angle / (2 * pi)) * 180.0)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)

    def reset(self):
        """
        This function is used to reset the state variables
        to the configurable parameters
        This functions has to be called before every match
        """
        self.health = self.max_health
        self.speed = 0.0
        self.angle = self.rotation
        self.dead = False
        self.reload_timer = 0.0
        # Place the tank at a random position inside the screen dimensions
        self.position.x = random.randint(BOX_SIZE[0], SCREEN_DIMENSION[0] - BOX_SIZE[0])
        self.position.y = random.randint(BOX_SIZE[1], SCREEN_DIMENSION[1] - BOX_SIZE[1])

    def update(self, args):
        timing_factor = args[3]
        if self.dead is False:
            # Add ellipsed time to reload_timer
            self.reload_timer += timing_factor
            # Update the position
            self.velocity = vector.vector(cos(self.angle), sin(self.angle))
            self.velocity = vector.mul(self.velocity, self.speed)
            self.velocity = vector.mul(self.velocity, timing_factor)
            self.position = vector.add(self.position, self.velocity)
            # Update the unrotated rectangle
            self.rect.center = (self.position.x, self.position.y)
            # Rotate the image and update the rotated rectangle
            self.rotated_image = pygame.transform.rotate(self.image,
                    (-self.angle / pi) * 180.0)
            self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rotated_rect)

    def accelerate(self, timing_factor):
        self.speed += self.acceleration * timing_factor
        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def deccelerate(self, timing_factor):
        self.speed -= self.acceleration * timing_factor
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

    def slow_down(self, timing_factor):
        if self.speed > self.acceleration * timing_factor:
            self.speed -= self.acceleration * timing_factor
        elif self.speed < -self.acceleration * timing_factor:
            self.speed += self.acceleration * timing_factor
        else:
            self.speed *= 0.9

    def rotate_left(self, timing_factor):
        steering_force = tc.calculate_steering_force(self)
        self.angle -= steering_force * timing_factor
        self.angle_in_deg = (self.angle / pi) * 180.0

    def rotate_right(self, timing_factor):
        steering_force = tc.calculate_steering_force(self)
        self.angle += steering_force * timing_factor
        self.angle_in_deg = (self.angle / pi) * 180.0

    def shoot(self, timing_factor):
        if self.reload_timer > self.reload_time:
            self.reload_timer = 0.0
            event = pygame.event.Event(TANK_SHOT_EVENT, tank=self)
            # This event will be handeld by the update function of
            # the game_scene
            pygame.event.post(event)

    def set_fire_rate(self, fire_rate):
        self.fire_rate = fire_rate
        self.reload_time = 1.0 / self.fire_rate

    def decrease_health(self, damage):
        """
        Decrease the health of the tank by damage and check if
        the tank is dead. This function will be invoked from controller.py
        by a handling tank shot function.
        """
        self.health -= damage
        if self.health <= 0:
            self.dead = True
