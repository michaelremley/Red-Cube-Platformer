"""
Platformer keyboard controller code
"""
import pygame, sys
import pygame.locals

class PyGameKeyboardController(object):
    """ Handles keyboard input for platformer """
    def __init__(self,model):
        # Tells the controller where to send inputs to
        self.model = model

    def handle_keys(self,keys):
        """ Key presses are passed to the model avatar to be handled """
        # Move left if left arrow or a are pressed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.model.avatar.addinput('LEFT')
        else:
            self.model.avatar.removeinput('LEFT')
        # Move right if right arrow or d are pressed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.model.avatar.addinput('RIGHT')
        else:
            self.model.avatar.removeinput('RIGHT')
        # Jump if space, up arrow, or w are pressed
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.model.avatar.addinput('JUMP')
        else:
            self.model.avatar.removeinput('JUMP')
        # Quits the game if q or p are pressed
        if keys[pygame.K_q] or keys[pygame.K_p]:
            self.model.avatar.addinput('QUIT')
        else:
            self.model.avatar.removeinput('QUIT')
