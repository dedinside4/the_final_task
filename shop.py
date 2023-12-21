import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Магазин костюмов")

font = pygame.font.Font(pygame.font.match_font('arial'), 36)

class Costume:
    def __init__(self, name, image_path, width=100, height=100, x=0, y=0):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Load a background image
background_image = pygame.image.load("images/feed.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

costumes = [
    Costume("Costume 1", "images/candy1.png", x=95, y=115),
    Costume("Costume 2", "images/candy2.png", x=240, y=115),
    Costume("Costume 3", "images/candy3.png", x=385, y=115),
    Costume("Costume 4", "images/candy4.png", x=350, y=255),
]

selected_costume = None

# Button parameters
button_width = 280
button_height = 180
button_x = 325
button_y = 395

play_button_image = pygame.image.load("images/igrat_pixian_ai.png")
play_button_image = pygame.transform.scale(play_button_image, (button_width, button_height))
play_button_rect = play_button_image.get_rect(topleft=(button_x, button_y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for costume in costumes:
                if costume.rect.collidepoint(event.pos):
                    selected_costume = costume
            if play_button_rect.collidepoint(event.pos) and selected_costume:
                # Redirect to perehod.py
                with open("selected_costume.txt", "w") as file:
                    file.write(selected_costume.name)
                sys.exit()

    # Draw the background image
    screen.blit(background_image, (0, 0))

    for costume in costumes:
        costume.draw(screen)

    if selected_costume:
        pygame.draw.rect(screen, (0, 255, 0), selected_costume.rect, 2)

    # Draw the play button
    screen.blit(play_button_image, play_button_rect.topleft)

    pygame.display.flip()
