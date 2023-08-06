"""
This file defines global settings used all over the place.
Their are not necessarily constants.
"""

from os.path import (dirname, realpath)

SCREEN_DIMENSION = (1024, 728)
MUSIC_VOLUME = 1.0
# The prescaler defines the max music volume as the music should be
# background music
MUSIC_VOLUME_PRESCALER = 0.25
SOUND_EFFECT_VOLUME = 1.0
BOX_SIZE = (25, 25)
BASE_PATH = dirname(realpath(__file__))
