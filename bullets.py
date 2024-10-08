import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class that manages bullets fired from the ship"""
    def __init__(self,ai_game):
        """Create a bullet object at ship's current location"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet a position (0,0) and then set its correct position
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store Bullet's y postion in decimal values
        self.y = float(self.rect.y)

    def update(self):
        """Move bullets up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position 
        self.rect.y = self.y


    def Draw_bullet(self):
        """Draw the bulltes on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)