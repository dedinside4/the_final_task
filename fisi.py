import pygame
import numpy as np
import random
import time
from scipy.optimize import root_scalar
import os
import sys

# Initialize pygame and set display mode
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Costume:
    def __init__(self, name, image_path, width=100, height=100, x=0, y=0):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        filename_with_extension = os.path.basename(image_path)
        self.image_filename = os.path.splitext(filename_with_extension)[0] + ".png"  # Add ".png" to the filename

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Candy(pygame.sprite.Sprite):
    def __init__(self, x, y, costume_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(costume_image, (25, 25))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.ropes = []
        self.mass = 1
        self.viscosity = 0.09
        self.velocity = np.array([0, 0])
        self.pos = np.array(self.rect.center) * SCALE

    def update(self):
        time = 1 / FPS
        force = self.mass * G
        for rope in self.ropes:
            f = rope.take_force()
            f_norm = np.linalg.norm(f)
            if f_norm > 0:
                force -= (force @ f) * f / (f_norm ** 2)
                force += f
                if f @ self.velocity < 0:
                    self.velocity -= (self.velocity @ f) * f / (f_norm ** 2)
        force -= self.viscosity * self.velocity
        self.pos = self.pos + self.velocity * time + force * (time ** 2) / (2 * self.mass)
        self.velocity = self.velocity + force * time / self.mass
        self.rect.center = (self.pos[0] / SCALE, self.pos[1] / SCALE)

    def bind(self, pin_pos, length):
        rope = Rope(pin_pos, length, self)
        pin = Pin(pin_pos)
        pins.add(pin)
        self.ropes.append(rope)

    def draw_vectors(self):
        force = self.mass * G
        for rope in self.ropes:
            force += rope.take_force()
        x, y = self.rect.center
        pygame.draw.line(screen, (255, 0, 0), self.rect.center, (x + force[0] / SCALE, y + force[1] / SCALE), width=3)
        pygame.draw.line(screen, (0, 0, 255), self.rect.center, (x + self.velocity[0] / SCALE, y + self.velocity[1] / SCALE), width=3)

class Rope:
    def __init__(self, static_end, length, candy):
        self.candy = candy
        self.length = length * SCALE
        self.static_end = np.array(static_end) * SCALE
        self.one_end = static_end
        self.resilience = 200
        self.a = None
        self.b = None

    def CUT_THROUGH_THE_ROPE(self, x1, y1, x2, y2):
        beheaded = False
        candy_end = self.candy.pos
        r = candy_end - self.static_end
        x1 -= self.static_end[0]
        x2 -= self.static_end[0]
        y1 -= self.static_end[1]
        y2 -= self.static_end[1]
        if self.length - np.linalg.norm(r) <= self.length * 0.001:
            k = r[1] / r[0]
            if (k * x1 - y1) * (k * x2 - y2) < 0:
                beheaded = True
        elif not (self.a is None):
            if (self.a * x1**2 + self.b * x1 - y1) * (self.a * x2**2 + self.b * x2 - y2) < 0:
                beheaded = True
        if beheaded:
            self.kill_kill_kill()

    def kill_kill_kill(self):
        self.candy.ropes.remove(self)

    def take_force(self):
        candy_end = self.candy.pos
        l = self.static_end - candy_end
        l_norm = np.linalg.norm(l)
        if l_norm > self.length:
            force = l / l_norm * (l_norm - self.length) * self.resilience
            return force
        return np.array([0, 0])

    def draw(self):
        candy_end = self.candy.pos
        if self.length - np.linalg.norm(self.static_end - candy_end) > self.length * 0.004:
            self.draw_unstreched(candy_end)
        else:
            pygame.draw.line(screen, (0, 0, 0), self.one_end, self.candy.rect.center, width=2)

    def draw_unstreched(self, candy_end):
        res = root_scalar(self.find_coeffs, args=(candy_end), x0=1, x1=3, rtol=0.00001)
        a = -abs(res.root)
        r = -self.static_end + candy_end
        x2, y2 = r[0], r[1]
        b = (y2 - a * x2**2) / x2
        self.draw_parabole(a, b, x2, y2)
        self.a = a
        self.b = b

    def draw_parabole(self, a, b, x2, y2):
        x_0, y_0 = self.one_end
        for x in np.linspace(0, x2, 1000):
            y = a * x**2 + b * x
            y_screen = y / SCALE
            x_screen = x / SCALE
            pygame.draw.circle(screen, (0, 0, 0), (x_0 + x_screen, y_0 + y_screen), 1)

    def find_coeffs(self, a, candy_end):
        r = -self.static_end + candy_end
        x2, y2 = r[0], r[1]
        b = (y2 - a * x2**2) / x2
        if x2 < 0:
            L = self.integral(0, a, b) - self.integral(x2, a, b)
        else:
            L = -self.integral(0, a, b) + self.integral(x2, a, b)
        return L - self.length

    def integral(self, x, a, b):
        t = (2 * a * x + b)
        s = np.sqrt(t**2 + 1) * t + np.arcsinh(t)
        s /= 4 * a
        return s

class Pin(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(candy_img, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = pos

def draw_text(text, c, size, color=(0, 0, 0)):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = c
    screen.blit(text_surface, text_rect)

def read_selected_costume():
    selected_costume_path = "selected_costume.txt"
    if os.path.exists(selected_costume_path):
        with open(selected_costume_path, "r") as file:
            return file.read().strip()
    return "candy"  # Default costume if file not found

def save_selected_costume(filename):
    base_filename = os.path.splitext(filename)[0]
    with open("selected_costume.txt", "w") as file:
        file.write(base_filename)

# Read selected costume from file
selected_costume = read_selected_costume()
costume_img_path = f'images/{selected_costume}.png'
costume_img = pygame.image.load(costume_img_path).convert()

# Scale the candy_img to match the pin size
candy_img = pygame.transform.scale(candy_img, (10, 10))

SCALE = 0.01
G = np.array([0, 9.8])
FPS = 500
candies = pygame.sprite.Group()
pins = pygame.sprite.Group()
background = pygame.image.load('images/background.png').convert()
background = pygame.transform.scale(background, ((WIDTH, HEIGHT)))
candy = Candy(WIDTH / 2 - 30, HEIGHT / 2 - 40, costume_img)
candy.bind((WIDTH / 2 + 70, HEIGHT / 2 + 70), 280)
candy.bind((WIDTH / 2 + 100, HEIGHT / 2 + 40), 170)
candies.add(candy)
clock = pygame.time.Clock()
Roukanken = False
last_pos = (None, None)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Roukanken = True
        elif event.type == pygame.MOUSEBUTTONUP:
            Roukanken = False
            last_pos = (None, None)

    if Roukanken:
        x, y = pygame.mouse.get_pos()
        x1, y1 = last_pos
        if not (x1 is None):
            for rope in candy.ropes:
                rope.CUT_THROUGH_THE_ROPE(x1 * SCALE, y1 * SCALE, x * SCALE, y * SCALE)
        last_pos = x, y

    candies.update()
    screen.blit(background, (0, 0))
    candies.draw(screen)
    for rope in candy.ropes:
        rope.draw()
    pins.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
