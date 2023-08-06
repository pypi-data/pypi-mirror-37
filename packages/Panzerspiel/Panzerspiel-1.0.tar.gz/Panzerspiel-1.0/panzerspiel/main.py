import pygame
from os.path import join
from panzerspiel import menu
from panzerspiel.global_settings import (SCREEN_DIMENSION, MUSIC_VOLUME,
        MUSIC_VOLUME_PRESCALER, BASE_PATH)


def main():
    # Init the pygame mixer and pygame
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_DIMENSION)
    running = True
    clock = pygame.time.Clock()

    # As long as the programme is running a background track is looped
    pygame.mixer.music.load(join(BASE_PATH, "res2/music/mindmapthat_-_Transmutation.mp3"))
    pygame.mixer.music.set_volume(MUSIC_VOLUME * MUSIC_VOLUME_PRESCALER)
    pygame.mixer.music.play(-1)

    menu.build_menu()

    while running:
        events = pygame.event.get()
        # Further event handling happens in the game_scene
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Get user input
        mouse_keys = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        pressed_keys = pygame.key.get_pressed()
        # Update the game clock and get the timing factor
        clock.tick()
        timing_factor = clock.get_rawtime() / 1000.0
        # Update the menu and game_scene
        menu.MENU_LIST.update((mouse_keys, mouse_pos,
            pressed_keys, timing_factor, events))

        # Clear the screen
        screen.fill((0, 0, 0))
        # Render the game
        menu.MENU_LIST.draw(screen)

        # Flip the scene
        pygame.display.flip()
