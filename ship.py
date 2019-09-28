import pygame,random
from consts import WIDTH, HEIGHT,G
from missile import Missile

MAXHYPERSPACEENERGY=1
HYPERSPACEENERGY=1
HENERGYPERTICK=0.001
MLAUNCHENERGY=2
MAXSENERGY=100.0
MAXMENERGY=10.0
SENERGYPERTICK=0.2
MENERGYPERTICK=0.2
ACCEL=0.1
ROTATEANGLE=3
MISSILEHIT=10
PLANETHIT=80

class Ship(pygame.sprite.Sprite):
    def __init__(self,image,startpos,startdir):
        super().__init__()
        self.orig_image = pygame.image.load(image)
        self.vel = pygame.math.Vector2(0, 0)
        self.dir = pygame.math.Vector2(startdir)
        self.image = pygame.transform.rotozoom(self.orig_image, 0, 0.15)
        self.rect = self.image.get_rect(center=startpos)
        self.pos = pygame.math.Vector2(self.rect.center)

        self.s_energy = MAXSENERGY
        self.m_energy = MAXMENERGY
        self.h_energy=MAXHYPERSPACEENERGY
        self.thrustSprite=Thrust(self)

    def update(self):
        #energy updates
        if self.s_energy<MAXSENERGY and self.s_energy>0:
            self.s_energy+=SENERGYPERTICK
        if self.m_energy<MAXMENERGY:
            self.m_energy+=MENERGYPERTICK
        if self.h_energy<MAXHYPERSPACEENERGY:
            self.h_energy+=HENERGYPERTICK

        #accel due to planet
        g = pygame.math.Vector2((WIDTH / 2 - self.pos[0]), (HEIGHT / 2 - self.pos[1]))
        self.vel += G * g.magnitude() * g.normalize()

        v = pygame.math.Vector2(-1, 0)  # todo, move out
        self.image = pygame.transform.rotozoom(self.orig_image, -(v.angle_to(self.dir)), 0.15)
        self.pos += self.vel
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        if self.pos[0] > WIDTH:
            self.pos[0] = self.pos[0] - WIDTH
        if self.pos[0] < 0:
            self.pos[0] = WIDTH - self.pos[0]
        if self.pos[1] > HEIGHT:
            self.pos[1] = self.pos[1] - HEIGHT
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT - self.pos[1]

    def hyperspace(self):
        if self.h_energy-HYPERSPACEENERGY>=0:
            self.h_energy-=HYPERSPACEENERGY
            self.pos=(random.randint(0,WIDTH),random.randint(0,HEIGHT))
            #self.rect.center=(random.randint(0,WIDTH),random.randint(0,HEIGHT))

    def thrust(self):
        self.vel+=self.dir*ACCEL
        self.thrustSprite.visible=1

    def missile_launch(self):
        if self.m_energy-MLAUNCHENERGY>0:
            self.m_energy-=MLAUNCHENERGY
            if self.m_energy<0:
                self.m_energy=0
            return Missile(self)
        return None

    def left(self):
        self.dir.rotate_ip(-ROTATEANGLE)

    def right(self):
        self.dir.rotate_ip(ROTATEANGLE)

    def missile_hit(self):
        self.s_energy-=MISSILEHIT

    #def ship_hit(self,other):
    #    if other.s_energy>0:
    #        self.s_energy-=other.s_energy

    def planet_hit(self):
        self.s_energy-=PLANETHIT

    def destroyed(self):
        return self.s_energy<0

    def senergy_percent(self):
        se=int(100*(float(self.s_energy)/MAXSENERGY))
        return 0 if se<0 else se

    def menergy_percent(self):
        me=int(100*(float(self.m_energy)/MAXMENERGY))
        return 0 if me < 0 else me

    def henergy_percent(self):
        return int(100 * (float(self.h_energy) / MAXHYPERSPACEENERGY))


class Thrust(pygame.sprite.DirtySprite):
    def __init__(self, ship):
        super().__init__()
        self.orig_image = pygame.image.load("thrust.png")
        self.image = pygame.transform.rotozoom(self.orig_image, 0, 0.15)
        ship_pos = pygame.math.Vector2(ship.rect.center)
        self.pos = ship_pos + ship.dir * (-20)
        self.rect = self.image.get_rect(center=self.pos)
        self.visible = 0
        self.ship = ship
        self.vel = 0

    def update(self):
        if self.visible == 0:
            return
        else:
            ship_pos = pygame.math.Vector2(self.ship.rect.center)
            self.pos = ship_pos + self.ship.dir * (-20)
            self.image = pygame.transform.rotozoom(self.orig_image,
                                                   -(pygame.math.Vector2(-1, 0).angle_to(self.ship.dir)), 0.15)
            self.rect = self.image.get_rect(center=self.pos)
