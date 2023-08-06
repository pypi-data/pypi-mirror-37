import pygame
from os.path import join
from panzerspiel import menu
from panzerspiel import menu_list
from panzerspiel import collision
from panzerspiel.global_settings import BASE_PATH
from panzerspiel.own_sprite import own_sprite
from panzerspiel.animated_sprite import animated_sprite
from panzerspiel.animator import animator
from panzerspiel.event_definitions import (TANK_SHOT_EVENT)
from panzerspiel.health_bar import health_bar


class one_vs_one(menu_list.sub_menu):
    """
    A gamescene inherits from sub_menu. This way it can be part
    of the menu_list. Its the representation of the actuall game to play.
    Therefor it defines own necessary variables like the tanks, the controller
    of the tanks and the arena to play in and ovverides the update and
    draw function of the sub_menu class
    """
    def __init__(self, tanks, controllers, arena):
        super().__init__()
        self.tanks = tanks
        self.controllers = controllers
        self.arena = arena
        self.animator = animator()
        # Two animated sprites to display if a tank is ready to shoot
        self.reload_sprite1 = animated_sprite(join(BASE_PATH, "res2/TReload.png"),
                (10, 100), pygame.Rect(0, 0, 24, 48), 0)
        self.reload_sprite2 = animated_sprite(join(BASE_PATH, "res2/TReload.png"),
                (1010, 100), pygame.Rect(0, 0, 24, 48), 0)
        # Two healthbars to display the health of the tanks
        self.health_bar1 = health_bar(join(BASE_PATH, "res2/TFrameRed.png"),
            join(BASE_PATH, "res2/THealthbar.png"), (10, 50),
            self.tanks[0], lambda x: x.health / x.max_health)
        self.health_bar2 = health_bar(join(BASE_PATH, "res2/TFrameBlue.png"),
            join(BASE_PATH, "res2/THealthbar.png"), (914, 50), self.tanks[1],
            lambda x: x.health / x.max_health)
        # A background image
        self.background = own_sprite(join(BASE_PATH, "res2/TTankMapGreen.png"), (0, 0))
        # The after life delay and counter is used to add a small delay
        # between the death of a tank and the switch to the winning menu
        # This way the last explosion animation and sound is played
        self.after_life_delay = 0.5
        self.after_life_counter = 0.0

    def update(self, args):
        # mouse_keys = args[0]
        # mouse_pos = args[1]
        keys_pressed = args[2]
        timing_factor = args[3]
        events = args[4]
        # If the esc button is pressed pause the game
        # by displaying the pause button
        if keys_pressed[pygame.K_ESCAPE]:
            menu.MENU_LIST.append(menu.PAUSE_MENU)
        # Controll the tanks by controll functions
        # this assumes their is an equal amount of tanks and controll
        # functions
        for i in range(0, len(self.controllers)):
            # Reassamble the args structure and add a reference to the
            # controlled tank to args. This way the controller function
            # can use every given user input and controll the tank directly
            # by calling its controlling functions
            self.controllers[i]((args[0], args[1], args[2],
                args[3], self.tanks[i]))

        # Update the tanks
        for t in self.tanks:
            t.update(args)
            collision.handle_tank_arena_collision(t, self.arena)
            collision.handle_tank_tank_collision(t, self.tanks)

        # If the tank is not reloaded set the reload sprite step to one
        if self.tanks[0].reload_timer < self.tanks[0].reload_time:
            self.reload_sprite1.set_step(1)
        else:
            self.reload_sprite1.set_step(0)
        if self.tanks[1].reload_timer < self.tanks[1].reload_time:
            self.reload_sprite2.set_step(1)
        else:
            self.reload_sprite2.set_step(0)

        # Update the tank health bars
        self.health_bar1.update()
        self.health_bar2.update()

        # Update the animator
        self.animator.update(args)

        # Update the arena
        self.arena.update()

        # Query the events for a tank-shot-event
        for e in events:
            if e.type == TANK_SHOT_EVENT:
                collision.handle_tank_shot(e.tank, self.arena + self.tanks)

        # If tank1 is dead tank2 has won
        if self.tanks[0].dead:
            if self.after_life_counter > self.after_life_delay:
                menu.MENU_LIST.append(menu.WINNING_MENUS[1])
            self.after_life_counter += timing_factor
        if self.tanks[1].dead:
            if self.after_life_counter > self.after_life_delay:
                menu.MENU_LIST.append(menu.WINNING_MENUS[0])
            self.after_life_counter += timing_factor

    def draw(self, screen):
        self.background.draw(screen)
        for t in self.tanks:
            t.draw(screen)
        self.arena.draw(screen)
        self.animator.draw(screen)
        self.reload_sprite1.draw(screen)
        self.reload_sprite2.draw(screen)
        self.health_bar1.draw(screen)
        self.health_bar2.draw(screen)
