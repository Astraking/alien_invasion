import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Load the ship image and get its rect
        self.image = pygame.image.load('images/spaceship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Trying to include up and down movement

        # Store a decimal value for the ship's center
        # Originalx and y stor the original position
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)


        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.centery -= self.ai_settings.ship_speed_factor

        # Update rect object from self.centerx and self.centery
        if self.moving_up or self.moving_down:
            self.rect.centery = self.centery
        if self.moving_left or self.moving_right:
            self.rect.centerx = self.centerx


    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # Restore ship to unchanged, original position
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom