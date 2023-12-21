import pygame
import os

class Costume:
    def __init__(self, name, image_path, width=100, height=100, x=0, y=0):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        filename_with_extension = os.path.basename(image_path)
        self.image_filename = os.path.splitext(filename_with_extension)[0]  # Get the filename without any extension

        # Save the costume name without extension to selected_costume.txt
        self.save_selected_costume()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def save_selected_costume(self):
        base_filename = os.path.splitext(self.name)[0]
        selected_costume_path = "selected_costume.txt"
        with open(selected_costume_path, "w") as file:
            file.write(base_filename)
