"""
Platformer keyboard controller code
"""

import pygame.locals

class PyGameKeyboardController(object):
    """ Handles keyboard input for platformer """
    def __init__(self,model):
        self.model = model
        self.sensitivity = 2.0

    def handle_event(self,event):
        """ Left and right presses modify the x velocity of the avatar """
        if event.type != pygame.locals.KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.avatar.vx += -self.sensitivity
        if event.key == pygame.K_RIGHT:
            self.model.avatar.vx += self.sensitivity
        if event.key == pygame.K_a:
            self.model.avatar.vx += -self.sensitivity
        if event.key == pygame.K_d:
            self.model.avatar.vx += self.sensitivity
        if event.key == pygame.K_SPACE and self.model.avatar.onsurfacex == True:
            self.model.avatar.onsurfacex = False
            self.model.avatar.vy = -2
