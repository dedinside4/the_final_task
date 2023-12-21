import pygame
import numpy as np
from scipy.optimize import root_scalar
from objects import *
from level_reader import *
from perehod import *
from shop import *
class Button:
    def __init__(self, x, y, image_path, scale_factor=0.2, action=None):
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * scale_factor),
                                                             int(original_image.get_height() * scale_factor)))
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
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
def start_level(number,skin):
    global running
    candies,pins,stars,amnyams,bubbles=read_level(f'level_{number}.txt')
    if not (skin is None):
        for candy in candies.sprites():
            change_accordingly(skin,candy)
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
        candies_eaten+=len(pygame.sprite.groupcollide(candies, amnyams, True, False, collided = pygame.sprite.collide_rect_ratio(50/100)))
        catches=pygame.sprite.groupcollide(bubbles, candies, False, False)
        for bubble in catches:
            for candy in catches[bubble]:
                bubble.catch(candy)
        all_stars+=len(pygame.sprite.groupcollide(stars, candies, True, False, collided = pygame.sprite.collide_circle_ratio(45/100)))
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
def choose_level(skin=None):
    global running
    level=select_level(screen,Button,WIDTH,HEIGHT)
    if level is None:
        running=False
    else:
        start_level(level,skin)
def choose_costume():
    global running
    playing,costume=select_costume(screen,WIDTH,HEIGHT)
    if playing:
        choose_level(skin=costume)
    else:
        running=False
def quit_the_game():
    global running
    running=False
def change_accordingly(skin,candy):
    candy.image = pygame.transform.scale(pygame.image.load('images/'+skin), ((55, 55)))   
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
background=pygame.image.load('images/menu_background.png').convert()
background=pygame.transform.scale(background, ((WIDTH,HEIGHT)))
clock=pygame.time.Clock()
font = pygame.font.Font(pygame.font.match_font('arial'), 36)

start_button = Button(WIDTH // 2, 200, "images/play_pixian_ai.png", scale_factor=0.3, action=choose_level)
character_button = Button(WIDTH // 2, 300, "images/om_nom_pixian_ai.png", scale_factor=0.3, action=choose_costume)
exit_button = Button(WIDTH // 2, 400, "images/exit_pixian_ai.png", scale_factor=0.3, action=quit_the_game)

buttons = [start_button, character_button, exit_button]

def change_state(new_state=None):
    global current_state, current_level

    if current_state == "main_menu":
        current_state = "perehod.py"
    elif current_state == "perehod.py":
        if new_state is None:
            current_level += 1
            new_state = f"level_{current_level}.py"  # Adjust this according to your level naming convention
        current_state = new_state

# Основной цикл игры
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    if button.action:
                        button.action()

    # Отрисовка фона
    screen.blit(background, (0, 0))

    # Отрисовка кнопок
    for button in buttons:
        button.draw(screen)

    # Обновление экрана
    pygame.display.flip()
pygame.quit()

    
