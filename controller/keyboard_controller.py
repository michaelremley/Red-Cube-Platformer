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
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.model.avatar.addinput('LEFT')
        else:
            self.model.avatar.removeinput('LEFT')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.model.avatar.addinput('RIGHT')
        else:
            self.model.avatar.removeinput('RIGHT')
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.model.avatar.addinput('JUMP')
        else:
            self.model.avatar.removeinput('JUMP')
