import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surf, (255, 255, 0), (30 // 2, 30 // 2), 7)
        self.rect = self.surf.get_rect()

        self.pos = pygame.math.Vector2((190, 345))
        self.vel = pygame.math.Vector2(0, 0)
        self.dir = -1

    def move(self, direction, speed, width):
        if direction == 3:
            self.vel.x = -speed
            self.vel.y = 0
        if direction == 1:
            self.vel.x = speed
            self.vel.y = 0
        if direction == 0:
            self.vel.y = -speed
            self.vel.x = 0
        if direction == 2:
            self.vel.y = speed
            self.vel.x = 0

        self.pos += self.vel

        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width
        self.rect.midbottom = self.pos

    def stop(self):
        self.vel = pygame.math.Vector2(0, 0)

    def get_current_cell(self):
        return int(self.pos.x / 20) % 19, int((self.pos.y - 15) / 20) % 22

    def set_direction(self, pressed_keys, next_move, old_direction):
        if pressed_keys[K_LEFT]:
            self.dir = 3
        if pressed_keys[K_RIGHT]:
            self.dir = 1
        if pressed_keys[K_UP]:
            self.dir = 0
        if pressed_keys[K_DOWN]:
            self.dir = 2
        if self.dir != old_direction:
            return True, self.dir
        else:
            return False | next_move, old_direction

    def get_direction(self):
        return self.dir
