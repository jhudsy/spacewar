import pygame,random
from ship import Ship
from consts import WIDTH,HEIGHT


class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("planet.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

if __name__=="__main__":
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    clock=pygame.time.Clock()

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    for i in range(0, 150):
        pygame.draw.circle(background, (255, 255, 255), (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 1)

    background=background.convert()
    screen.blit(background,(0,0))

    ship1=Ship("ship1.png",(WIDTH/4,HEIGHT/2),pygame.math.Vector2(0,1))
    ship2=Ship("ship2.png",(WIDTH-(WIDTH/4),HEIGHT/2),pygame.math.Vector2(0,-1))
    shipGroup=pygame.sprite.Group(ship1,ship2)
    planet=pygame.sprite.GroupSingle(Planet())
    missileGroup=pygame.sprite.Group()
    radius1=0
    radius2=0

    finished=False
    while not finished:
        clock.tick(60)
        events=pygame.event.get()
        for e in events:
            if e.type==pygame.QUIT:
                pygame.quit()
                finished=True

        key=pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            finished=True
        if key[pygame.K_x]:
            ship1.hyperspace()
        if key[pygame.K_w]:
            ship1.thrust()
            shipGroup.add(ship1.thrustSprite)
        else:
            shipGroup.remove(ship1.thrustSprite)
        if key[pygame.K_a]:
            ship1.left()
        if key[pygame.K_d]:
            ship1.right()
        if key[pygame.K_s]:
            m=ship1.missile_launch()
            if m!=None:
                missileGroup.add(m)

        if key[pygame.K_m]:
            ship2.hyperspace()
        if key[pygame.K_i]:
            ship2.thrust()
            shipGroup.add(ship2.thrustSprite)
        else:
            shipGroup.remove(ship2.thrustSprite)
        if key[pygame.K_j]:
            ship2.left()
        if key[pygame.K_l]:
            ship2.right()
        if key[pygame.K_k]:
            m=ship2.missile_launch()
            if m!=None:
                missileGroup.add(m)

        for m in missileGroup:
            if m.fuel<0:
              missileGroup.remove(m)

        #Collision detection
        pygame.sprite.spritecollide(planet.sprite,missileGroup,True)
        ship1hit=pygame.sprite.spritecollide(ship1,missileGroup,True,collided=pygame.sprite.collide_mask)
        ship2hit = pygame.sprite.spritecollide(ship2, missileGroup, True, collided=pygame.sprite.collide_mask)
        for m in ship1hit:
            ship1.missile_hit()
        for m in ship2hit:
            ship2.missile_hit()

        if len(list(pygame.sprite.spritecollide(ship1,planet,False,collided=pygame.sprite.collide_mask)))>0:
            ship1.planet_hit()
        if len(list(pygame.sprite.spritecollide(ship2,planet,False,collided=pygame.sprite.collide_mask)))>0:
            ship2.planet_hit()

        #handle ship collisions
        if pygame.sprite.collide_mask(ship1,ship2)!=None:
            se1=ship1.s_energy
            se2=ship2.s_energy
            if se1>0:
                ship2.s_energy-=se1
            if se2>0:
                ship1.s_energy-=se2



        #Render
        screen.blit(background,(0,0))
        shipGroup.update()
        missileGroup.update()
        missileGroup.draw(screen)
        shipGroup.draw(screen)
        planet.draw(screen)

        pygame.draw.rect(screen,(255,248,1,10),pygame.Rect(5,5,100,20),1)
        pygame.draw.rect(screen, (255, 248, 1, 10),  pygame.Rect(5, 5,  ship1.senergy_percent(),20),0)

        pygame.draw.rect(screen, (255, 248, 1, 10), pygame.Rect(5, 25, 100, 20), 1)
        pygame.draw.rect(screen, (255, 248, 1, 10), pygame.Rect(5, 25, ship1.menergy_percent(), 20), 0)

        pygame.draw.rect(screen, (255, 248, 1, 10), pygame.Rect(5, 45, 100, 20), 1)
        pygame.draw.rect(screen, (255, 248, 1, 10), pygame.Rect(5, 45, ship1.henergy_percent(), 20), 0)


        pygame.draw.rect(screen, (0, 191, 192, 10), pygame.Rect(WIDTH-105, 5, 100, 20), 1)
        pygame.draw.rect(screen, (0, 191, 192, 10), pygame.Rect(WIDTH-5-ship2.senergy_percent(), 5, ship2.senergy_percent(), 20), 0)

        pygame.draw.rect(screen, (0, 191, 192, 10), pygame.Rect(WIDTH - 105, 25, 100, 20), 1)
        pygame.draw.rect(screen, (0, 191, 192, 10), pygame.Rect(WIDTH-5-ship2.menergy_percent(), 25, ship2.menergy_percent(), 20), 0)

        pygame.draw.rect(screen, (0, 191, 192, 10), pygame.Rect(WIDTH - 105, 45, 100, 20), 1)
        pygame.draw.rect(screen, (0, 191, 192, 10),
                         pygame.Rect(WIDTH - 5 - ship2.henergy_percent(), 45, ship2.henergy_percent(), 20), 0)

        if ship1.senergy_percent()==0:
            radius1+=1
            pygame.draw.circle(screen, (255, 0, 0), ship1.rect.center, radius1, 0)
        if ship2.senergy_percent() == 0:
            radius2+=2
            pygame.draw.circle(screen, (0, 0, 255), ship2.rect.center, radius2, 0)

        if radius1>100 or radius2>100:
            finished=True
        pygame.display.flip()

    #display end of game message
    if ship1.senergy_percent()<=0 and ship2.senergy_percent()<=0:
        message="Draw"
    elif ship1.senergy_percent()<=0:
        message="Right player wins"
    elif ship2.senergy_percent()<=0:
        message="Left player wins"
    screen.blit(background, (0, 0))
    font = pygame.font.Font('freesansbold.ttf', 64)
    text=font.render(message,True,(255,255,255))
    text_rect=text.get_rect()
    text_rect.center=(WIDTH/2,HEIGHT/2)
    screen.blit(text,text_rect)
    pygame.display.flip()
    finished=False
    while not finished:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                finished = True
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            finished = True


