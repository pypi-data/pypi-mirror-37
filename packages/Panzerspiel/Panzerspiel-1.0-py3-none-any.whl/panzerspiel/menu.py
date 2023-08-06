import pygame
from os.path import join
from panzerspiel import tank
from panzerspiel import tank_config as tc
from panzerspiel import game_scene
from panzerspiel import arena
from panzerspiel import global_settings
from panzerspiel.menu_list import sub_menu
from panzerspiel.menu_list import menu_list
from panzerspiel.button import button
from panzerspiel.h_slider import h_slider
from panzerspiel.textbox import textbox
from panzerspiel.own_sprite import own_sprite
from panzerspiel.controller import player1_controller
from panzerspiel.controller import player2_controller
from math import pi

# The main menu
MAIN_MENU = sub_menu()
# The option menu where the user can set game options
OPTION_MENU = sub_menu()
# The customization menu, this will be shown
# before the match starts to allow two players to customize
# their tanks
CUSTOMIZE_TANK_MENU = sub_menu()
# The pause menu if someon pauses the match
PAUSE_MENU = sub_menu()
# A list of winning submenus for every possible winner
WINNING_MENUS = []
# The one and only menu_list to hold the current menus
MENU_LIST = menu_list()
# The arena to play in
ARENA = None
# Get the basepath from global settings
BASE_PATH = global_settings.BASE_PATH

# The actuall match to play
MATCH = None


# Switch to the customize tank menu
def start_game_cb(args):
    global MENU_LIST
    global CUSTOMIZE_TANK_MENU
    MENU_LIST.append(CUSTOMIZE_TANK_MENU)


# Switch to the option menu
def option_button_cb(args):
    global MENU_LIST
    global OPTION_MENU
    MENU_LIST.append(OPTION_MENU)


# Throw a pygame QUIT event to leave the game loop
def leave_game_cb(args):
    pygame.event.post(pygame.event.Event(pygame.QUIT))


# Switch to the match
def start_match_cb(args):
    global ARENA
    global MATCH
    global MENU_LIST

    # It is only allowed to start the match if no tanks
    # has negativ credits
    for t in tank.TANKS:
        if t.credits < 0:
            return

    ARENA = arena.random_arena()
    # Initialise every tank
    for t in tank.TANKS:
        t.reset()
    MATCH = game_scene.one_vs_one(tank.TANKS,
            [player1_controller, player2_controller], ARENA)
    MENU_LIST.append(MATCH)


# Return to parent menu
def return_cb(args):
    MENU_LIST.pop()


# Return to customize menu
def return_to_customize_cb(args):
    global MENU_LIST
    MENU_LIST.clear()
    MENU_LIST.append(MAIN_MENU)
    MENU_LIST.append(CUSTOMIZE_TANK_MENU)


# The following callback functions will connect current slider with the
# matching values of the tank
def max_speed1_cb(args):
    tank.TANKS[0].max_speed = args[0].value
    tc.calculate_credit_points(tank.TANKS[0])


def acc1_cb(args):
    tank.TANKS[0].acceleration = args[0].value
    tc.calculate_credit_points(tank.TANKS[0])


def health1_cb(args):
    tank.TANKS[0].max_health = args[0].value
    tank.TANKS[0].health = tank.TANKS[0].max_health
    tc.calculate_credit_points(tank.TANKS[0])


def dps1_cb(args):
    tank.TANKS[0].dps = args[0].value
    tc.calculate_credit_points(tank.TANKS[0])


def fire_rate1_cb(args):
    tank.TANKS[0].set_fire_rate(args[0].value)
    tc.calculate_credit_points(tank.TANKS[0])


def max_speed2_cb(args):
    tank.TANKS[1].max_speed = args[0].value
    tc.calculate_credit_points(tank.TANKS[1])


def acc2_cb(args):
    tank.TANKS[1].acceleration = args[0].value
    tc.calculate_credit_points(tank.TANKS[1])


def health2_cb(args):
    tank.TANKS[1].max_health = args[0].value
    tank.TANKS[1].health = tank.TANKS[1].max_health
    tc.calculate_credit_points(tank.TANKS[1])


def dps2_cb(args):
    tank.TANKS[1].dps = args[0].value
    tc.calculate_credit_points(tank.TANKS[1])


def fire_rate2_cb(args):
    tank.TANKS[1].set_fire_rate(args[0].value)
    tc.calculate_credit_points(tank.TANKS[1])


def surge_factor_cb(args):
    # Set the surge factor aka the powerlevel of the tanks
    tc.SURGE_FACTOR = args[0].value


def music_volume_cb(args):
    # Set the music volume of the game
    global_settings.MUSIC_VOLUME = args[0].value
    pygame.mixer.music.set_volume(global_settings.MUSIC_VOLUME)


def sound_effects_volume_cb(args):
    # Set the sound effect volume of the game
    # This global variable will be used in the update function
    # of the animator class as there is no acces to the animator class
    # from this point
    global_settings.SOUND_EFFECT_VOLUME = args[0].value


# Build up the main menu
def build_main_menu():
    global MAIN_MENU
    background = own_sprite(join(BASE_PATH, "res2/TCover.png"), (0, 0))
    start_game_button = button(join(BASE_PATH, "res2/TStart.png"), (200, 568),
            start_game_cb)
    option_button = button(join(BASE_PATH, "res2/TOptions.png"), (450, 568),
            option_button_cb)
    leave_game_button = button(join(BASE_PATH, "res2/TLeave.png"), (700, 568),
            leave_game_cb, True)
    MAIN_MENU.add(background)
    MAIN_MENU.add(start_game_button)
    MAIN_MENU.add(option_button)
    MAIN_MENU.add(leave_game_button)


# Build the option menu
def build_option_menu():
    global OPTION_MENU
    # Add a background to the menu
    background = own_sprite(join(BASE_PATH, "res2/TCover.png"), (0, 0))
    # Navigate button to return
    return_button = button(join(BASE_PATH, "res2/TBack.png"), (450, 568), return_cb)

    # Names of the slides
    font = pygame.font.FontType(pygame.font.get_default_font(), 13)
    white = (255, 255, 255)
    surge_factor_tb = textbox(font, pygame.Rect(100, 200, 100, 100),
            white, "Surge Factor")
    music_volume_tb = textbox(font, pygame.Rect(100, 250, 100, 100),
            white, "Music Volume")
    sound_effect_tb = textbox(font, pygame.Rect(100, 300, 100, 100),
            white, "Sound Volume")
    # Slides
    surge_factor_slider = h_slider(join(BASE_PATH, "res2/TSlider.png"),
            join(BASE_PATH, "res2/TKnob.png"), (200, 200), 0, 1, surge_factor_cb)
    music_volume_slider = h_slider(join(BASE_PATH, "res2/TSlider.png"),
            join(BASE_PATH, "res2/TKnob.png"), (200, 250), 0, 1, music_volume_cb)
    sound_volume_slider = h_slider(join(BASE_PATH, "res2/TSlider.png"),
            join(BASE_PATH, "res2/TKnob.png"), (200, 300), 0, 1, sound_effects_volume_cb)

    # Set the slides standard values
    surge_factor_slider.set_value(tc.SURGE_FACTOR),
    music_volume_slider.set_value(global_settings.MUSIC_VOLUME)
    sound_volume_slider.set_value(global_settings.SOUND_EFFECT_VOLUME)

    # Value textboxes
    surge_factor_value_tb = textbox(font, pygame.Rect(310, 200, 100, 100),
            white, "", surge_factor_slider, lambda x: x.value)
    music_volume_value_tb = textbox(font, pygame.Rect(310, 250, 100, 100),
            white, "", music_volume_slider, lambda x: x.value)
    sound_effect_value_tb = textbox(font, pygame.Rect(310, 300, 100, 100),
            white, "", sound_volume_slider, lambda x: x.value)

    # Add all elements to the OPTION_MENU
    OPTION_MENU.add(background)
    OPTION_MENU.add(return_button)
    OPTION_MENU.add(surge_factor_tb)
    OPTION_MENU.add(music_volume_tb)
    OPTION_MENU.add(sound_effect_tb)
    OPTION_MENU.add(surge_factor_slider)
    OPTION_MENU.add(music_volume_slider)
    OPTION_MENU.add(sound_volume_slider)
    OPTION_MENU.add(surge_factor_value_tb)
    OPTION_MENU.add(music_volume_value_tb)
    OPTION_MENU.add(sound_effect_value_tb)


# Build up the customize tank menu
def build_customize_tank_menu():
    global CUSTOMIZE_TANK_MENU

    # Again add a background
    background = own_sprite(join(BASE_PATH, "res2/TCover.png"), (0, 0))
    # Both tanks have to be initialised here as this menu will be used
    # to configure them
    tank.TANKS.append(tank.tank(pygame.image.load(join(BASE_PATH, "res2/TTankRed.png")),
        pygame.Rect(50, 364, 25, 25), 0))
    tank.TANKS.append(tank.tank(pygame.image.load(join(BASE_PATH, "res2/TTankBlue.png")),
        pygame.Rect(949, 364, 25, 25), pi))

    # Navigate buttons to enter other sub-menus
    start_match_button = button(join(BASE_PATH, "res2/TStart.png"), (200, 568),
            start_match_cb)
    return_button = button(join(BASE_PATH, "res2/TBack.png"), (700, 568), return_cb)

    # Names of the slides
    font = pygame.font.FontType(pygame.font.get_default_font(), 13)
    white = (255, 255, 255)
    max_speed_tb = textbox(font, pygame.Rect(450, 200, 100, 100),
            white, "======= Speed ====")
    acc_tb = textbox(font, pygame.Rect(450, 250, 100, 100),
            white, "=== Acceleration ===")
    health_tb = textbox(font, pygame.Rect(450, 300, 100, 100),
            white, "===== Health =====")
    dps_tb = textbox(font, pygame.Rect(450, 350, 100, 100),
            white, "====== DPS ======")
    fire_rate_tb = textbox(font, pygame.Rect(450, 400, 100, 100),
            white, "==== Fire Rate ====")

    # Customization slides for tank1
    max_speed_slider1 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (200, 200),
        tc.MIN_SPEED, tc.MAX_SPEED, max_speed1_cb)
    acc_slider1 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (200, 250),
        tc.MIN_ACCELERATION, tc.MAX_ACCELERATION, acc1_cb)
    health_slider1 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (200, 300),
        tc.MIN_HEALTH, tc.MAX_HEALTH, health1_cb)
    dps_slider1 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (200, 350),
        tc.MIN_DPS, tc.MAX_DPS, dps1_cb)
    fire_rate_slider1 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (200, 400),
        tc.MIN_FIRE_RATE, tc.MAX_FIRE_RATE, fire_rate1_cb)

    # Value textboxes for tank1
    t1_max_speed_tb = textbox(font, pygame.Rect(310, 200, 100, 100),
            white, "", max_speed_slider1, lambda x: x.value)
    t1_acc_tb = textbox(font, pygame.Rect(310, 250, 100, 100),
            white, "", acc_slider1, lambda x: x.value)
    t1_health_tb = textbox(font, pygame.Rect(310, 300, 100, 100),
            white, "", health_slider1, lambda x: x.value)
    t1_dps_tb = textbox(font, pygame.Rect(310, 350, 100, 100),
            white, "", dps_slider1, lambda x: x.value)
    t1_fire_rate_tb = textbox(font, pygame.Rect(310, 400, 100, 100),
            white, "", fire_rate_slider1, lambda x: x.value)

    # Customization slides for tank2
    max_speed_slider2 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (700, 200),
        tc.MIN_SPEED, tc.MAX_SPEED, max_speed2_cb)
    acc_slider2 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (700, 250),
        tc.MIN_ACCELERATION, tc.MAX_ACCELERATION, acc2_cb)
    health_slider2 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (700, 300),
        tc.MIN_HEALTH, tc.MAX_HEALTH, health2_cb)
    dps_slider2 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (700, 350),
        tc.MIN_DPS, tc.MAX_DPS, dps2_cb)
    fire_rate_slider2 = h_slider(join(BASE_PATH, "res2/TSlider.png"),
        join(BASE_PATH, "res2/TKnob.png"), (700, 400),
        tc.MIN_FIRE_RATE, tc.MAX_FIRE_RATE, fire_rate2_cb)

    # Value textboxes for tank2
    t2_max_speed_tb = textbox(font, pygame.Rect(810, 200, 100, 100),
            white, "", max_speed_slider2, lambda x: x.value)
    t2_acc_tb = textbox(font, pygame.Rect(810, 250, 100, 100),
            white, "", acc_slider2, lambda x: x.value)
    t2_health_tb = textbox(font, pygame.Rect(810, 300, 100, 100),
            white, "", health_slider2, lambda x: x.value)
    t2_dps_tb = textbox(font, pygame.Rect(810, 350, 100, 100),
            white, "", dps_slider2, lambda x: x.value)
    t2_fire_rate_tb = textbox(font, pygame.Rect(810, 400, 100, 100),
            white, "", fire_rate_slider2, lambda x: x.value)

    # Textbox to display the credit points of player one and two
    # The formular to calculate the credit points returns a slightly
    # complex number (why ever) so the getter function just uses
    # the real component
    t1_credit_tb = textbox(font, pygame.Rect(250, 150, 100, 100),
            white, "", tank.TANKS[0], lambda x: x.credits.real)
    t2_credit_tb = textbox(font, pygame.Rect(750, 150, 100, 100),
            white, "", tank.TANKS[1], lambda x: x.credits.real)

    # Add all the gui elements to the sprite group
    CUSTOMIZE_TANK_MENU.add(background)
    CUSTOMIZE_TANK_MENU.add(start_match_button)
    CUSTOMIZE_TANK_MENU.add(return_button)
    CUSTOMIZE_TANK_MENU.add(max_speed_slider1)
    CUSTOMIZE_TANK_MENU.add(acc_slider1)
    CUSTOMIZE_TANK_MENU.add(health_slider1)
    CUSTOMIZE_TANK_MENU.add(dps_slider1)
    CUSTOMIZE_TANK_MENU.add(fire_rate_slider1)
    CUSTOMIZE_TANK_MENU.add(max_speed_slider2)
    CUSTOMIZE_TANK_MENU.add(acc_slider2)
    CUSTOMIZE_TANK_MENU.add(health_slider2)
    CUSTOMIZE_TANK_MENU.add(dps_slider2)
    CUSTOMIZE_TANK_MENU.add(fire_rate_slider2)
    CUSTOMIZE_TANK_MENU.add(max_speed_tb)
    CUSTOMIZE_TANK_MENU.add(acc_tb)
    CUSTOMIZE_TANK_MENU.add(health_tb)
    CUSTOMIZE_TANK_MENU.add(dps_tb)
    CUSTOMIZE_TANK_MENU.add(fire_rate_tb)
    CUSTOMIZE_TANK_MENU.add(t1_fire_rate_tb)
    CUSTOMIZE_TANK_MENU.add(t1_max_speed_tb)
    CUSTOMIZE_TANK_MENU.add(t1_acc_tb)
    CUSTOMIZE_TANK_MENU.add(t1_health_tb)
    CUSTOMIZE_TANK_MENU.add(t1_dps_tb)
    CUSTOMIZE_TANK_MENU.add(t2_fire_rate_tb)
    CUSTOMIZE_TANK_MENU.add(t2_max_speed_tb)
    CUSTOMIZE_TANK_MENU.add(t2_acc_tb)
    CUSTOMIZE_TANK_MENU.add(t2_health_tb)
    CUSTOMIZE_TANK_MENU.add(t2_dps_tb)
    CUSTOMIZE_TANK_MENU.add(t2_fire_rate_tb)
    CUSTOMIZE_TANK_MENU.add(t1_credit_tb)
    CUSTOMIZE_TANK_MENU.add(t2_credit_tb)


# Build up the pause menu
def build_pause_menu():
    global PAUSE_MENU
    customize_menu = button(join(BASE_PATH, "res2/TCustom.png"),
            (200, 568), return_to_customize_cb)
    options_menu = button(join(BASE_PATH, "res2/TOptions.png"),
            (450, 568), option_button_cb)
    return_button = button(join(BASE_PATH, "res2/TBack.png"),
            (700, 568), return_cb)
    PAUSE_MENU = sub_menu([customize_menu, options_menu, return_button], True)


def build_winning_menus():
    global WINNING_MENUS
    winning_menu1 = sub_menu()
    restart_button = button(join(BASE_PATH, "res2/TRetry.png"),
            (200, 568), start_match_cb)
    customize_menu = button(join(BASE_PATH, "res2/TCustom.png"),
            (700, 568), return_to_customize_cb)
    back_ground1 = own_sprite(join(BASE_PATH, "res2/tank1_won.png"), (0, 0))
    winning_menu1.add(back_ground1)
    winning_menu1.add(restart_button)
    winning_menu1.add(customize_menu)
    winning_menu2 = sub_menu()
    restart_button = button(join(BASE_PATH, "res2/TRetry.png"),
            (200, 568), start_match_cb)
    customize_menu = button(join(BASE_PATH, "res2/TCustom.png"),
            (700, 568), return_to_customize_cb)
    back_ground2 = own_sprite(join(BASE_PATH, "res2/tank2_won.png"), (0, 0))
    winning_menu2.add(back_ground2)
    winning_menu2.add(restart_button)
    winning_menu2.add(customize_menu)
    WINNING_MENUS.append(winning_menu1)
    WINNING_MENUS.append(winning_menu2)


# Build all sub menus and push the main menu onto the menu list
def build_menu():
    global MENU_LIST
    build_main_menu()
    build_option_menu()
    build_customize_tank_menu()
    build_pause_menu()
    build_winning_menus()
    MENU_LIST.append(MAIN_MENU)
