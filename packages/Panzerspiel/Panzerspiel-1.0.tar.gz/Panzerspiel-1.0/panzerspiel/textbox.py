import pygame


class textbox(pygame.sprite.Sprite):
    def __init__(self, font, rect, color, text, ref=None, getter=None):
        super().__init__()
        self.font = font
        self.image = self.font.render(text, False, color)
        self.rect = rect
        self.color = color
        self.text = text
        self.ref = ref
        self.getter = getter

    def update(self, args):
        if self.ref is not None and self.getter is not None:
            # Use a format string to represent the result of the
            # getter function invoked on the referenc as a float
            # with two decimal points
            self.text = "{0:.2f}".format(self.getter(self.ref))
            self.image = self.font.render(self.text, False, self.color)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def change_text(self, text):
        self.text = text
        self.image = self.font.render(self.text, False, self.color)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((512, 512))
    running = True

    font = pygame.font.FontType(pygame.font.get_default_font(), 13)
    print(font)
    t1 = textbox(font, pygame.Rect(100, 100, 200, 100), (255, 0, 0), "Hello")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))
        t1.draw(screen)

        # Draw the scene
        pygame.display.flip()
