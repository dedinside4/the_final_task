import pygame
import numpy as np
from model import *
class Candy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)                                    
        self.image = pygame.transform.scale(candy_img, ((25,25)))
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.ropes=[]
        self.mass=1
        self.viscosity=0.09
        self.velocity=np.array([0,0])
        self.pos=np.array(self.rect.center)*SCALE
    def update(self):
        time=1/FPS
        force=self.mass*G
        for rope in self.ropes:
            f=rope.take_force()
            f_norm=np.linalg.norm(f)
            if f_norm>0:
                force-=(force@f)*f/(f_norm**2)
                force+=f
                if f@self.velocity<0:
                    self.velocity-=(self.velocity@f)*f/(f_norm**2)
        force-=self.viscosity*self.velocity
        #print(pos,'before')
        self.pos=self.pos+self.velocity*time+force*(time**2)/(2*self.mass)
        #print(pos, 'after')
        self.velocity=self.velocity+force*time/self.mass
        self.rect.center=(self.pos[0]/SCALE,self.pos[1]/SCALE)
    def bind(self,pin_pos,length):
        rope=Rope(pin_pos,length,self)
        pin=Pin(pin_pos)
        pins.add(pin)
        self.ropes.append(rope)
    def draw_vectors(self):
        force=self.mass*G
        for rope in self.ropes:
            force+=rope.take_force()
        x,y=self.rect.center
        pygame.draw.line(screen,(255,0,0),self.rect.center,(x+force[0]/SCALE,y+force[1]/SCALE),width=3)
        pygame.draw.line(screen,(0,0,255),self.rect.center,(x+self.velocity[0]/SCALE,y+self.velocity[1]/SCALE),width=3)
class Rope:
    def __init__(self,static_end,length,candy):
        self.candy=candy
        self.length=length*SCALE
        self.static_end=np.array(static_end)*SCALE
        self.one_end=static_end
        self.resilience=200
        #self.count=300
        #self.elements=np.array([[x1+i*(x2-x1)/(self.count-1),y1+i*(y2-y1)/(self.count-1)] for i in range(self.count)])
        #self.velocities=np.array([[0,0]]*self.count)
        #self.l=np.sqrt(((x2-x1)/(self.count-1))**2+((y2-y1)/(self.count-1))**2)
        #self.last_update=pygame.time.get_ticks()
    def take_force(self):
        candy_end=self.candy.pos
        l=self.static_end-candy_end
        l_norm=np.linalg.norm(l)
        if l_norm>self.length:
            force=l/l_norm*(l_norm-self.length)*self.resilience
            return force
        return np.array([0,0])
    def draw(self):
        pygame.draw.line(screen,(0,0,0),self.one_end,self.candy.rect.center,width=3)
        
class Pin(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)                                    
        self.image = pygame.transform.scale(candy_img, ((10,10)))
        self.rect=self.image.get_rect()
        self.rect.center=pos
def draw_text(text,c,size,color=(0,0,0)):
    font=pygame.font.Font(pygame.font.match_font('arial'),size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.center=c
    screen.blit(text_surface,text_rect)               














SCALE=0.01
G=np.array([0,9.8])
FPS=500
WIDTH,HEIGHT=600,700
pygame.init()
running=True
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Это и есть амням')
candies=pygame.sprite.Group()
pins=pygame.sprite.Group()
pin_img=pygame.image.load('pin.png')
candy_img=pygame.image.load('candy.png').convert()
background=pygame.image.load('background.png').convert()
background=pygame.transform.scale(background, ((WIDTH,HEIGHT)))
candy=Candy(WIDTH/2-30,HEIGHT/2-40)
candy.bind((WIDTH/2+70,HEIGHT/2+70),250)
candies.add(candy)
clock=pygame.time.Clock()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    candies.update()
    screen.blit(background,(0,0))
    draw_text(str(clock.get_fps()),(70,70),15)
    candies.draw(screen)
    for rope in candy.ropes:
        rope.draw()
    pins.draw(screen)
    #candy.draw_vectors()
    pygame.display.flip()
pygame.quit()


    
