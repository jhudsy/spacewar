import pygame
from consts import *

class Missile(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()
        v = pygame.math.Vector2(-1, 0)  # todo, move out
        self.dir = pygame.math.Vector2(ship.dir)
        self.orig_image = pygame.image.load("missile.png")
        self.image = pygame.transform.rotozoom(self.orig_image, -(v.angle_to(self.dir)), 0.35)
        ship_pos = pygame.math.Vector2(ship.rect.center)
        self.pos = ship_pos + ship.dir * (16)
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pygame.math.Vector2(ship.vel + 8 * ship.dir)
        self.fuel = 120
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos+=self.vel
        g = pygame.math.Vector2((WIDTH / 2 - self.pos[0]), (HEIGHT / 2 - self.pos[1]))
        self.vel += G * g.magnitude() * g.normalize()

        self.rect = self.image.get_rect(center=self.pos)
        if self.pos[0] > WIDTH:
            self.pos[0] = self.pos[0] - WIDTH
        if self.pos[0] < 0:
            self.pos[0] = WIDTH - self.pos[0]
        if self.pos[1] > HEIGHT:
            self.pos[1] = self.pos[1] - HEIGHT
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT - self.pos[1]

        self.fuel -= 1