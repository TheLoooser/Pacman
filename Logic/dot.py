import pygame


class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surf, (255, 255, 255), (30 // 2, 30 // 2), 2)
        self.rect = self.surf.get_rect(center=(x + 1.5, y + 1.5))
