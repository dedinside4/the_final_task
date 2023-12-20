import pygame
import numpy as np
import random
import time
import levels
import perehod
from scipy.optimize import root_scalar
from objects import *
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
stars=pygame.sprite.Group()
amnyams=pygame.sprite.Group()
background=pygame.image.load('images/background.png').convert()
background=pygame.transform.scale(background, ((WIDTH,HEIGHT)))
candy=Candy((WIDTH/2-30,HEIGHT/2-40))
pin=candy.bind((WIDTH/2+70,HEIGHT/2+70),280)
pins.add(pin)
pin=candy.bind((WIDTH/2+100,HEIGHT/2+40),170)
pins.add(pin)
candies.add(candy)
amnyam=Amnyam((WIDTH/2+190,HEIGHT/2+240))
amnyams.add(amnyam)
star=Star(((WIDTH/2+150,HEIGHT/2+210)))
stars.add(star)
star=Star(((WIDTH/2+100,HEIGHT/2+220)))
stars.add(star)
star=Star(((WIDTH/2+10,HEIGHT/2+170)))
stars.add(star)
clock=pygame.time.Clock()
Roukanken=False
last_pos=(None,None)
all_stars=0
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if Roukanken:
            x,y=pygame.mouse.get_pos()
            x1,y1=last_pos
            if not(x1 is None):
                for candy in candies.sprites():
                    for rope in candy.ropes:
                        rope.CUT_THROUGH_THE_ROPE(x1*SCALE,y1*SCALE,x*SCALE,y*SCALE)
            last_pos=x,y
        if event.type == pygame.MOUSEBUTTONDOWN:
            Roukanken=True
        if event.type == pygame.MOUSEBUTTONUP:
            Roukanken=False
            last_pos=(None,None)
    candies.update()
    pygame.sprite.groupcollide(amnyams, candies, False, True, collided = pygame.sprite.collide_rect_ratio(80/100))
    all_stars+=len(pygame.sprite.groupcollide(stars, candies, True, False))
    screen.blit(background,(0,0))
    stars.draw(screen)
    candies.draw(screen)
    for candy in candies.sprites():
        for rope in candy.ropes:
            rope.draw(screen)
    pins.draw(screen)
    amnyams.draw(screen)
    pygame.display.flip()
pygame.quit()


    
