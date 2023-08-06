import pygame
from copy import copy


class box_template():
    """
    A box template is used to match an image with a max_health
    value. This way it is made shure that similar boxes always break
    after the same amount of hits
    """
    def __init__(self, image, max_health):
        self.image = image
        self.max_health = max_health


class box(pygame.sprite.Sprite):
    """
    A box is an extended sprite providing an update, draw
    and a decrease_health function.
    The update function updates the flag death, which specifies
    if the current health of a box is less-equal than zero.
    This way a list of boxes (an arena) can be walked through and every
    dead box can be removes. This provides the possibility of a
    destructable arena. If a max_health less than zero is specified
    the box is set to be instructable
    """
    def __init__(self, rect, template):
        super().__init__()
        self.image = template.image
        self.rect = pygame.Rect(rect)
        self.indestructable = False
        self.max_health = template.max_health
        if template.max_health <= 0:
            self.max_health = 1
            self.indestructable = True
        else:
            self.max_health = template.max_health
            self.indestructable = False
        self.health = self.max_health
        self.death = False

    def update(self):
        if self.health <= 0:
            self.death = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def decrease_health(self, damage):
        """
        Decrease health by damage as long as the box is not
        indestructable. This function will be invoked from within
        the controller.py by a handling tank shot function.
        """
        if self.indestructable is False:
            self.health -= damage

    def position(self, position):
        self.rect.center = position

    def copy(self):
        imag = copy(self.image)
        return box((self.rect.x, self.rect.y), (self.rect.width, self.rect.height),
                imag, self.max_health)
