import pygame
import sys
import os
import subprocess
from utils import change_state
# Создание кнопок
def next_image():
    global current_image_index,images,WIDTH,HEIGHT
    current_image_index = (current_image_index + 1) % len(images)
    update_background()

def previous_image():
    global current_image_index,images,WIDTH,HEIGHT
    current_image_index = (current_image_index - 1) % len(images)
    update_background()

def update_background():
    global background_image,images,WIDTH,HEIGHT
    background_image = pygame.image.load(os.path.join("images", images[current_image_index]))
    background_image = pygame.transform.scale(background_image, (WIDTH,HEIGHT))

def start_game():
    global current_image_index,chosen_level,running
    chosen_level=current_image_index+1
    running=False
def select_level(screen,Button,screen_width,screen_height):
    global current_image_index,images,WIDTH,HEIGHT,background_image,running,chosen_level
# Загрузка изображений
    images = ["urovenperehod.png", "levl2_pixian_ai.png", "levl3_pixian_ai.png"]
    current_image_index = 0
    WIDTH,HEIGHT=screen_width,screen_height
    # Загрузка изображения для фона
    background_image = pygame.image.load(os.path.join("images", images[current_image_index]))
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Шрифт для текста на кнопках
    font = pygame.font.Font(None, 36)

    next_button = Button(screen_width - 50, screen_height // 2, "images/right_pixian_ai.png", scale_factor=0.1, action=next_image)
    previous_button = Button(50, screen_height // 2, "images/left_pixian_ai.png", scale_factor=0.1, action=previous_image)
    start_game_button = Button(screen_width // 2, screen_height - 50, "images/play_pixian_ai.png", scale_factor=0.2, action=start_game)

    buttons = [next_button, previous_button, start_game_button]

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
        screen.blit(background_image, (0, 0))

        # Отрисовка кнопок
        for button in buttons:
            button.draw(screen)

        # Обновление экрана
        pygame.display.flip()
    return chosen_level
current_image_index=0
images=None
WIDTH,HEIGHT=0,0
background_image=None
running=True
chosen_level=None
