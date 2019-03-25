"""
BrickBreaker keyboard controller code
"""

import pygame.locals

class PyGameKeyboardController(object):
    """ Handles keyboard input for platformer """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Left and right presses modify the x velocity of the player """
        if event.type != pygame.locals.KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.player.vx += -1.0
        if event.key == pygame.K_RIGHT:
            self.model.player.vx += 1.0
        if event.key == pygame.K_a:
            self.model.player.vx += -1.0
        if event.key == pygame.K_d:
            self.model.player.vx += 1.0
        if event.key == pygame.K_SPACE:
            self.model.player.jumping = True
