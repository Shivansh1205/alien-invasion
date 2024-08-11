import pygame

class Ship:
    """A class to manage the ship"""
    
    def __init__(self, ai_game):
        """initialize the ship and its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        """load the ship and get its rect"""
        self.image = pygame.image.load('C:/Users/LENOVO/Desktop/python_work/alien-invasion-game/ship1.bmp')
        pygame.transform.scale(self.image, (50,30))
        self.rect = self.image.get_rect()
        
        """Start each new ship at the bottom of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = self.rect.x
        
        #movement flags
        self.moving_right = False
        self.moving_left =False

    def update(self):
        """update ship position based on movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        """Center the ship in the midbottom"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    
    def blit(self):
        self.screen.blit(self.image, self.rect)