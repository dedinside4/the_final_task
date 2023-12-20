import pygame
from objects import *
def read_level(name):
    candies=pygame.sprite.Group()
    amnyams=pygame.sprite.Group()
    stars=pygame.sprite.Group()
    pins=pygame.sprite.Group()
    with open('levels/'+name) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0]
            if object_type == "Star":
                star=parse_star_parameters(line)
                stars.add(star)
            elif object_type == "Candy":
                candy,pins1=parse_candy_parameters(line)
                candies.add(candy)
                for pin in pins1:
                    pins.add(pin)
            elif object_type == "Amnyam":
                amnyam=parse_amnyam_parameters(line)
                amnyams.add(amnyam)
    return candies,pins,stars,amnyams
def parse_star_parameters(line):
    a=line.split()
    pos=eval(a[1])
    return Star(pos)
def parse_amnyam_parameters(line):
    a=line.split()
    pos=eval(a[1])
    return Amnyam(pos)
def parse_candy_parameters(line):
    a=line.split()
    candy=Candy(eval(a[1]))
    pins=[]
    for i in range(1,(len(a))//2):
        pos=eval(a[i*2])
        l=int(a[1+i*2])
        pin=Pin(pos)
        candy.bind(pin,l)
        pins.append(pin)
    return candy,pins
pygame.init()
