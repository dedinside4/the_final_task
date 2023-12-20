import pygame
import sys
import os
from utils import change_state  # Import the change_state function

pygame.init()

# Определение размеров окна
screen_width = 800
screen_height = 600

# Создание объекта для отображения
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Листание картинок")

# Загрузка изображений
images = ["urovenperehod.png", "levl2_pixian_ai.png", "levl3_pixian_ai.png"]
current_image_index = 0

# Загрузка изображения для фона
background_image = pygame.image.load(os.path.join("images", images[current_image_index]))
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Шрифт для текста на кнопках
font = pygame.font.Font(None, 36)

# Класс для кнопок
class Button:
    def __init__(self, x, y, image_path, scale_factor=0.5, action=None):
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * scale_factor),
                                                             int(original_image.get_height() * scale_factor)))
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Создание кнопок
def next_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(images)
    update_background()

def previous_image():
    global current_image_index
    current_image_index = (current_image_index - 1) % len(images)
    update_background()

def update_background():
    global background_image
    background_image = pygame.image.load(os.path.join("images", images[current_image_index]))
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def start_game1():
    # Change the state to main.py
    change_state("main.py")

next_button = Button(screen_width - 50, screen_height // 2, "images/right_pixian_ai.png", scale_factor=0.1, action=next_image)
previous_button = Button(50, screen_height // 2, "images/left_pixian_ai.png", scale_factor=0.1, action=previous_image)
start_game_button = Button(screen_width // 2, screen_height - 50, "images/play_pixian_ai.png", scale_factor=0.2, action=start_game1)

buttons = [next_button, previous_button, start_game_button]

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                next_image()
            elif event.key == pygame.K_LEFT:
                previous_image()

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка кнопок
    for button in buttons:
        button.draw(screen)

    # Обновление экрана
    pygame.display.flip()
