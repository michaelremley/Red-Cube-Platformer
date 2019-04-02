# -*- coding: utf-8 -*-
"""
This is a platformer game based on keyboard contol for our Software Design project.

@author: Michael Remley and Skye Ozga
"""

import time
import pygame, sys
from model import PlatformerModel
from view import PyGameWindowView
from controller.keyboard_controller import PyGameKeyboardController


def start_game(size):
    """
    Given screen 'size' as (x,y) tuple, start platformer game
    """
    # Initialize pygame with held key repeats and a clock for physics
    pygame.init()
    pygame.key.set_repeat(50,1)
    clock = pygame.time.Clock()
    # Make a model using window size and the pygame clock
    model = PlatformerModel(size, clock)
    print(model)
    # Make a controller and view from the model and window size
    view = PyGameWindowView(model, size)
    controller = PyGameKeyboardController(model)

    # Running can be changed to stop execution when the game is over
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.locals.QUIT:
                running = False
            if controller.handle_keys(pygame.key.get_pressed()):
                running = False
        # Stop the loop if update fails or requests a quit
        if model.update():
            running = False
        # Draw the view
        view.draw()
        # Delay to regulate framerate
        time.sleep(.001)

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    # Standard resolution for Olin laptop screens
    size = (1920, 1080)
    start_game(size)
