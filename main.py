import pygame
import numpy as np
from scipy.optimize import root_scalar
from objects import *
from level_reader import *
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
candies,pins,stars,amnyams=read_level('level_6.txt')
background=pygame.image.load('images/background.png').convert()
background=pygame.transform.scale(background, ((WIDTH,HEIGHT)))
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
    for candy in candies.sprites():
        for rope in candy.ropes:
            rope.draw(screen)
    stars.draw(screen)
    candies.draw(screen)
    pins.draw(screen)
    amnyams.draw(screen)
    pygame.display.flip()
pygame.quit()


    
