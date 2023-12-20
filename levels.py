import pygame
import sys
import os
from utils import change_state  # Import the change_state function

pygame.init()

screen_width = 1360
screen_height = 860

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Уровень 1")  # Set the level title

background_image = pygame.image.load("images/background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

font = pygame.font.Font(pygame.font.match_font('arial'), 36)

class Button:
    def __init__(self, x, y, image_path, scale_factor=0.2, action=None):
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * scale_factor),
                                                             int(original_image.get_height() * scale_factor)))
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Создание кнопок
start_button = Button(screen_width // 2, 200, "images/play_pixian_ai.png", scale_factor=0.3, action=lambda: change_state())
character_button = Button(screen_width // 2, 300, "images/om_nom_pixian_ai.png", scale_factor=0.3, action=lambda: change_state("shop.py"))
exit_button = Button(screen_width // 2, 400, "images/exit_pixian_ai.png", scale_factor=0.3, action=sys.exit)

buttons = [start_button, character_button, exit_button]

current_state = "main_menu"
current_level = 1

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
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    if button.action:
                        button.action()

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка кнопок
    for button in buttons:
        button.draw(screen)

    # Обновление экрана
    pygame.display.flip()

    # Переключение между экранами
    if current_state.endswith(".py"):
        os.system("python " + current_state)
