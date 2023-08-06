import pygame


class own_sprite(pygame.sprite.Sprite):
    """
    The own sprite is nothing more than a pygame Sprite
    providing an empty update function as well as a draw funciton
    Adding an orignal pygame Sprite to a sub-menu ended up in endless
    recursion...whyever
    """
    def __init__(self, img_path, position):
        super().__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self, args):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
