import pygame


class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, is_pellet=False):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0, 0, 0))
        radius = 2 if not is_pellet else 5
        pygame.draw.circle(self.surf, (255, 255, 255), (30 // 2, 30 // 2), radius)
        self.rect = self.surf.get_rect(center=(x + 1.5, y + 1.5))

        self.is_pellet = is_pellet
