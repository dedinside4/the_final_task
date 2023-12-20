import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Магазин костюмов")

font = pygame.font.Font(pygame.font.match_font('arial'), 36)

class Costume:
    def __init__(self, name, image_path):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        screen.blit(self.image, self.rect.topleft)


background_image = pygame.image.load("images/feed.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))



costumes = [
    Costume("Costume 1", "images/fpfe_pixian_ai.png"),
    Costume("Costume 2", "images/fbmf_pixian_ai.png"),
    Costume("Costume 3", "images/frct_pixian_ai.png"),
]

selected_costume = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for costume in costumes:
                if costume.rect.collidepoint(event.pos):
                    selected_costume = costume

    # Draw the background image
    screen.blit(background_image, (0, 0))

    for i, costume in enumerate(costumes):
        costume.draw(screen, 100 * i + 50, 200)

    if selected_costume:
        pygame.draw.rect(screen, (0, 255, 0), selected_costume.rect, 2)

    pygame.display.flip()
