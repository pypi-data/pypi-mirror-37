import pygame


class animated_sprite(pygame.sprite.Sprite):
    """
    The animated sprite class can be used to play an ongoing animation
    or to display specific subtiles of a sprite.
    This animated sprite class is restricted to sprite_sheets with equally
    sized subtiles.
    """
    def __init__(self, img_path, position, tile_rect, duration_sec, oneshot=False):
        """
        The tile_rect specifies the size of the subtiles and determines
        the horizontal_steps and vertical_steps.
        The delay_per_step is calculated from the the number of sub_tiles
        and the duration_sec.
        """
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.tile_rect = tile_rect
        self.rect.x = position[0] - self.tile_rect.width // 2
        self.rect.y = position[1] - self.tile_rect.height // 2
        self.horizontal_steps = self.rect.width // self.tile_rect.width
        self.vertical_steps = self.rect.height // self.tile_rect.height
        self.delay_per_step = duration_sec / (self.horizontal_steps * self.vertical_steps)
        self.delay_counter = 0
        self.oneshot = oneshot
        self.finished = False

    def update(self, args):
        """
        Update the step according to the dimension of the tile and the
        delay_per_step. Play the animations once and set the the finished
        flag to True if the this object was instanciated as a oneshot.
        This flag can be used to remove the animation from a list of
        current animations.
        """
        timing_factor = args[0]
        self.delay_counter += timing_factor
        if self.delay_counter > self.delay_per_step:
            self.delay_counter = 0
            self.tile_rect.x += self.tile_rect.width
            if self.tile_rect.x > self.rect.width - self.tile_rect.width:
                self.tile_rect.x = 0
                self.tile_rect.y += self.tile_rect.height
            if self.tile_rect.y > self.rect.height - self.tile_rect.height:
                if self.oneshot:
                    self.finished = True
                else:
                    self.tile_rect.x = 0
                    self.tile_rect.y = 0

    def step(self):
        """
        This function is used to make on step in the animation not depending
        on the ellipsed time or the animation duration
        """
        self.tile_rect.x += self.tile_rect.width
        if self.tile_rect.x > self.rect.width - self.tile_rect.width:
            self.tile_rect.x = 0
            self.tile_rect.y += self.tile_rect.height
        if self.tile_rect.y > self.rect.height - self.tile_rect.height:
            if self.oneshot:
                self.finished = True
            else:
                self.tile_rect.x = 0
                self.tile_rect.y = 0

    def set_step(self, step):
        """
        Set the tile_rect to the chosen subtile. The subtiles are numbered
        linear from left to right and top to bottom
        """
        stepx = step % self.horizontal_steps
        stepy = 0
        if self.vertical_steps != 0:
            stepy = step // self.horizontal_steps
        self.tile_rect.x = stepx * self.tile_rect.width
        self.tile_rect.y = stepy * self.tile_rect.height

    def draw(self, screen):
        """
        Simply draw the tile_rect
        """
        screen.blit(self.image, self.rect, area=self.tile_rect)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    running = True
    clock = pygame.time.Clock()

    anim = animated_sprite("res/explosion.png", (100, 100),
            pygame.Rect(0, 0, 62, 62), 1, False)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        clock.tick()
        timing_factor = clock.get_rawtime() / 1000.0
        # Update the anim sprite
        anim.update((timing_factor,))

        # Clear the screen
        screen.fill((255, 255, 255))
        # Render the game
        anim.draw(screen)

        # Flip the scene
        pygame.display.flip()
