import pygame


class h_slider(pygame.sprite.Sprite):
    """
    The h_slider is an animated gui element. It represents a horizontal
    scrollbar. The value of the h_slider is always element of [min, max]
    and passed to the callback function on every change.
    """
    def __init__(self, slider_img_path, knob_img_path, position, _min, _max, callback):
        super().__init__()
        self.slider_image = pygame.image.load(slider_img_path)
        self.slider_rect = self.slider_image.get_rect()
        self.slider_rect.x = position[0]
        self.slider_rect.y = position[1]
        self.knob_image = pygame.image.load(knob_img_path)
        self.knob_rect = self.knob_image.get_rect()
        self.knob_rect.centerx = position[0]
        self.knob_rect.y = position[1]
        self.position = position
        self.min = _min
        self.max = _max
        self.value = _min
        self.old_value = _min
        self.callback = callback
        self.toggle = False

    def update(self, args):
        mouse_keys = args[0]
        mouse_pos = args[1]
        # Not used here
        # pressed_keys = args[2]
        if (mouse_keys[0] and self.knob_rect.collidepoint(mouse_pos)) or self.toggle:
            self.slide(args)
            self.toggle = True
        if not mouse_keys[0] and self.toggle:
            self.toggle = False

    def draw(self, surface):
        surface.blit(self.slider_image, self.slider_rect)
        surface.blit(self.knob_image, self.knob_rect)

    def slide(self, args):
        mouse_pos = args[1]
        self.knob_rect.centerx = mouse_pos[0]
        if self.knob_rect.centerx < self.slider_rect.x:
            self.knob_rect.centerx = self.slider_rect.x
        if self.knob_rect.centerx > self.slider_rect.x + self.slider_rect.width:
            self.knob_rect.centerx = self.slider_rect.x + self.slider_rect.width
        f = (self.knob_rect.centerx - self.slider_rect.x) / self.slider_rect.width
        self.value = self.min + (self.max - self.min) * f
        if self.value != self.old_value:
            self.callback((self, args[3:]))
            self.old_value = self.value

    def set_value(self, value):
        # Do nothing if value is illegal
        if value < self.min or value > self.max:
            return
        # Else update the value and position the knob
        self.value = value
        f = (self.value - self.min) / (self.max - self.min)
        self.knob_rect.centerx = self.slider_rect.x + f * self.slider_rect.width


def cb(args):
    print(args[0].value)


if __name__ == "__main__":
    """
    This test programme contains one h_slider called s1. On every change
    on the slider the function "cb" is invoked which prints the current
    value of the slider on the console. If the right mouse button is clicked
    the slider value is set to 150 (max) which is displayed properly.
    """
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    running = True

    s1 = h_slider("res/slider.png", "res/knob.png", (100, 100), 50, 150, cb)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Update
        mouse_keys = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        s1.update((mouse_keys, mouse_pos))

        # On right mouse click set the value to max
        if mouse_keys[2]:
            print("A")
            s1.set_value(150)

        # Clear the screen
        screen.fill((0, 0, 0))
        s1.draw(screen)

        # Flip the surface
        pygame.display.flip()
