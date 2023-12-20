import pygame
import re
import os
from objects import *
class PlaceButton(pygame.sprite.Sprite):
    def __init__(self,object_name,pos):
        pygame.sprite.Sprite.__init__(self)  
        self.object_name=object_name
        self.image=pygame.transform.scale(eval(object_name+'((0,0)).image'),((100,40)))
        self.rect=self.image.get_rect()
        self.rect.center=pos
    def activate(self,pos):
        placing=None
        changed=False
        if self.rect.collidepoint(pos):
            placing=self.object_name
            changed=True
        return placing, changed
def place_candy(pos):
    candy=Candy(pos)
    all_sprites.add(candy)
def place_amnyam(pos):
    amnyam=Amnyam(pos)
    all_sprites.add(amnyam)
def place_star(pos):
    star=Star(pos)
    all_sprites.add(star)
def place_pin(pos):
    pin=Pin(pos)
    all_sprites.add(pin)
    editing=True
    stage=0
    length=''
    while editing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                editing=False
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    for sprite in all_sprites.sprites():
                        if type(sprite)==type(Candy((0,0))) and sprite.rect.collidepoint(pygame.mouse.get_pos()) and not stage:
                            stage+=1
                            candy=sprite
            if event.type == pygame.TEXTINPUT and stage:
                res=re.findall('\d', event.text)
                for s in res:
                    length+=s
            if event.type == pygame.KEYDOWN and stage:
                if event.key == pygame.K_BACKSPACE:
                    length=length[:-1]
                if event.key == pygame.K_RETURN:
                    editing=False
                    x1,y1=candy.rect.center
                    x2,y2=pos
                    candy.bind(pin,max(int(length),((x1-x2)**2+(y1-y2)**2)**0.5+1))
        screen.blit(background,(0,0))
        all_sprites.draw(screen)
        if stage and len(length)>0:
            pygame.draw.circle(screen,(0,0,0),pos,int(length), width=3)
        draw_text('Длина веревки: ' + length,(50,50),13)
        pygame.display.flip()
def draw_text(text,c,size,color=(0,0,0)):
    font=pygame.font.Font(pygame.font.match_font('arial'),size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.center=c
    screen.blit(text_surface,text_rect) 
def create_level():
    files=[]
    for filename in os.listdir('levels'):
        files.append(filename)
    i=1
    while files.count(f'level_{i}.txt')>0:
        i+=1
    name=f'levels\level_{i}.txt'
    file=open(name,'w')
    for sprite in all_sprites.sprites():
        if type(Amnyam((0,0)))==type(sprite):
            x,y=sprite.rect.center
            file.write('Amnyam ('+str(x)+','+str(y)+')\n')
        elif type(Star((0,0)))==type(sprite):
            x,y=sprite.rect.center
            file.write('Star ('+str(x)+','+str(y)+')\n')
        elif type(Candy((0,0)))==type(sprite):
            x,y=sprite.rect.center
            s='Candy ('+str(x)+','+str(y)+') '
            for rope in sprite.ropes:
                x,y=rope.one_end
                l=int(rope.length/SCALE)+1
                s+='('+str(x)+','+str(y)+') '+str(l)+' '
            file.write(s+'\n')
    file.close()
    print('saved')
            
            











SCALE=0.01
G=np.array([0,9.8])
FPS=500
WIDTH,HEIGHT=600,700
pygame.init()
running=True     
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Классная игра амням и пророк санбой солнецебой певец')
all_sprites=pygame.sprite.Group()
buttons=pygame.sprite.Group()
available_objects=['Candy','Amnyam','Star','Pin']
for i in range(len(available_objects)):
    button=PlaceButton(available_objects[i],(50+101*i,650))
    buttons.add(button)
background=pygame.image.load('images/background.png').convert()
background=pygame.transform.scale(background, ((WIDTH,HEIGHT)))
clock=pygame.time.Clock()
placing=None
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                changed=False
                for button in buttons.sprites():
                    thing,changed=button.activate(pygame.mouse.get_pos())
                    if changed:
                        placing=thing
                        break
                if not changed and not (placing is None):
                    exec('place_'+placing.lower()+'(pygame.mouse.get_pos())')
            if event.button==3:
                for sprite in all_sprites.sprites():
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        if type(sprite)==type(Pin((0,0))):
                            candy,rope=sprite.bound
                            candy.ropes.remove(rope)
                        sprite.kill()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            create_level()
    screen.blit(background,(0,0))
    for candy in all_sprites.sprites():
        try:
            for rope in candy.ropes:
                rope.draw(screen)
        except:
            pass
    all_sprites.draw(screen)
    buttons.draw(screen)
    pygame.display.flip()
pygame.quit()
