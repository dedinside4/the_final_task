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
def draw_collected(screen,candies_eaten, all_stars):
    draw_text(str(all_stars),(10,10),14)
    screen.blit()
    draw_text(str(candies_eaten),(10,30),14)
def start_level(number):
    global running
    candies,pins,stars,amnyams,bubbles=read_level(f'level_{number}.txt')
    Roukanken=False
    last_pos=(None,None)
    all_stars=0
    candies_eaten=0
    ongoing=True
    while ongoing:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                ongoing=False
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
                for bubble in bubbles.sprites():
                    bubble.pop(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                Roukanken=False
                last_pos=(None,None)
        bubbles.update()
        candies.update()
        candies_eaten+=len(pygame.sprite.groupcollide(candies, amnyams, True, False, collided = pygame.sprite.collide_rect_ratio(60/100)))
        catches=pygame.sprite.groupcollide(bubbles, candies, False, False)
        for bubble in catches:
            for candy in catches[bubble]:
                bubble.catch(candy)
        all_stars+=len(pygame.sprite.groupcollide(stars, candies, True, False))
        if len(candies.sprites())==0:
            ongoing=False
        screen.blit(level_background,(0,0))
        for candy in candies.sprites():
            if candy.rect.centerx<0 or candy.rect.centerx>WIDTH or candy.rect.centery<0 or candy.rect.centery>HEIGHT:
                candy.kill()
            for rope in candy.ropes:
                rope.draw(screen)
        stars.draw(screen)
        candies.draw(screen)
        bubbles.draw(screen)
        pins.draw(screen)
        amnyams.draw(screen)
        #draw_collected(screen,candies_eaten, all_stars)
        pygame.display.flip()
    return candies_eaten, all_stars
SCALE=0.01
G=np.array([0,9.8])
FPS=500
WIDTH,HEIGHT=600,700
pygame.init()
running=True
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Это и есть амням')
level_background=pygame.image.load('images/level_background.png').convert()
level_background=pygame.transform.scale(level_background, ((WIDTH,HEIGHT)))
menu_background=pygame.image.load('images/menu_background.png').convert()
menu_background=pygame.transform.scale(menu_background, ((WIDTH,HEIGHT)))
clock=pygame.time.Clock()
start_level(1)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    
    screen.blit(menu_background,(0,0))
    pygame.display.flip()
pygame.quit()


    
