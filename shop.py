import pygame
import sys
import subprocess

class Costume:
    def __init__(self, name, image_path, width=100, height=100, x=0, y=0):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image_filename = image_path.split("/")[-1]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
def select_costume(screen,screen_width,screen_height):
# Load a background image
    background_image = pygame.image.load("images/feed.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    costumes = [
        Costume("Costume 1", "images/candy1.png", x=0.072*screen_width, y=0.188*screen_height),
        Costume("Costume 2", "images/candy2.png", x=0.252*screen_width, y=0.188*screen_height),
        Costume("Costume 3", "images/candy3.png", x=0.438*screen_width, y=0.188*screen_height),
        Costume("Costume 4", "images/candy4.png", x=0.416*screen_width, y=0.438*screen_height),
    ]

    selected_costume = None

    # Button parameters
    button_width = 280
    button_height = 180
    button_x = 0.322*screen_width
    button_y = 0.708*screen_height


    play_button_image = pygame.image.load("images/igrat_pixian_ai.png")
    play_button_image = pygame.transform.scale(play_button_image, (button_width, button_height))
    play_button_rect = play_button_image.get_rect(topleft=(button_x, button_y))
    playing=False
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for costume in costumes:
                    if costume.rect.collidepoint(event.pos):
                        selected_costume = costume

                if play_button_rect.collidepoint(event.pos) and selected_costume:
                    # Запустить файл perehod.py
                    playing=True
                    running=False

        screen.blit(background_image, (0, 0))

        for costume in costumes:
            costume.draw(screen)

        if selected_costume:
            pygame.draw.rect(screen, (0, 255, 0), selected_costume.rect, 2)

        screen.blit(play_button_image, play_button_rect.topleft)

        pygame.display.flip()
    return playing,selected_costume.image_filename
