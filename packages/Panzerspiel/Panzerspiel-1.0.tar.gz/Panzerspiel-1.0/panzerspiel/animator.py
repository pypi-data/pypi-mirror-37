import pygame
from os.path import join
from panzerspiel import global_settings
from panzerspiel.animated_sprite import animated_sprite
from panzerspiel.event_definitions import TANK_HIT_EVENT


class animator():
    """
    This class will be used to query on events and play animations
    and sound effects.
    The only event handled by the animator is the TANK_HIT_EVENT
    which is thrown by the handle_tank_shot function of collision.py.
    """
    def __init__(self):
        self.animations = []
        self.shot_sound = pygame.mixer.Sound(join(global_settings.BASE_PATH,
            "res2/explosion.wav"))

    def update(self, args):
        # mouse_keys = args[0]
        # mouse_pos = args[1]
        # keys_pressed = args[2]
        timing_factor = args[3]
        events = args[4]

        # Set the sound effect volume
        self.shot_sound.set_volume(global_settings.SOUND_EFFECT_VOLUME)

        for e in events:
            if e.type == TANK_HIT_EVENT:
                # Play the shot sound
                self.shot_sound.play(loops=0, maxtime=0, fade_ms=0)

                animation = animated_sprite(join(global_settings.BASE_PATH,
                    "res2/explosion.png"),
                    e.collision_point.as_int_tupel(),
                    pygame.Rect(0, 0, 128, 128), 1.0, True)
                self.animations.append(animation)
        for a in self.animations:
            a.update((timing_factor, ))

    def draw(self, screen):
        for a in self.animations:
            a.draw(screen)
