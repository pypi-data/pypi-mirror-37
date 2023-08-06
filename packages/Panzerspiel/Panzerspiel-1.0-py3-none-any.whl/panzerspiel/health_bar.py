import pygame


class health_bar(pygame.sprite.Sprite):
    """
    The healthbar class contains two images and two rectangles.
    The getterfunction should calculate a value between [0, 1] from the
    reference "ref"
    """
    def __init__(self, frame_img_path, bar_img_path, position, ref, getter):
        self.image = pygame.image.load(frame_img_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.image2 = pygame.image.load(bar_img_path)
        self.rect2 = self.image2.get_rect()
        self.rect2_max_width = self.rect2.width
        self.rect2.topleft = position
        self.ref = ref
        self.getter = getter

    def update(self):
        # The getterfunction should return a value element of [0, 1]
        width = int(self.getter(self.ref) * self.rect2_max_width)
        height = int(self.rect2.height)
        if width >= 0:
            self.image2 = pygame.transform.scale(self.image2, (width, height))
        else:
            self.image2 = pygame.transform.scale(self.image2, (0, height))
        self.rect2 = self.image2.get_rect()
        self.rect2.topleft = self.rect.topleft

    def draw(self, screen):
        # Render the healthbar first so the frame wont be overdrawn
        screen.blit(self.image2, self.rect2)
        screen.blit(self.image, self.rect)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    running = True

    max_value = 1024
    current_value = [max_value]
    hb = health_bar("res/health_bar_frame.png", "res/health_bar.png",
            (100, 100), current_value, lambda x: x[0] / max_value)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Get user input
        mouse_keys = pygame.mouse.get_pressed()
        if mouse_keys[0]:
            print("A")
            current_value[0] -= 1

        hb.update()

        # Clear the screen
        screen.fill((100, 100, 100))
        # Render the game
        hb.draw(screen)

        # Flip the scene
        pygame.display.flip()
