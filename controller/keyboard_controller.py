"""
Platformer keyboard controller code
"""

import pygame.locals

class PyGameKeyboardController(object):
    """ Handles keyboard input for platformer """
    def __init__(self,model):
        self.model = model
        self.sensitivity = 0.1

    def handle_keys(self,keys):
        """ Left and right presses modify the x velocity of the avatar """
        if keys[pygame.K_LEFT]:
            self.model.avatar.vx += -self.sensitivity
        if keys[pygame.K_RIGHT]:
            self.model.avatar.vx += self.sensitivity
        if keys[pygame.K_a]:
            self.model.avatar.vx += -self.sensitivity
        if keys[pygame.K_d]:
            self.model.avatar.vx += self.sensitivity
        if keys[pygame.K_SPACE] and self.model.avatar.onsurfacex == True:
            self.model.avatar.onsurfacex = False
            self.model.avatar.vy = -2
