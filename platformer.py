# -*- coding: utf-8 -*-
"""
This is a platformer game based on keyboard contol for our Software Design project.

@author: Michael Remley and Skye Ozga
"""

import time
import pygame
from model import PlatformerModel
from view import PyGameWindowView
from controller.keyboard_controller import PyGameKeyboardController


def start_game(size):
    """
    Given screen 'size' as (x,y) tuple, start platformer game
    """
    pygame.init()

    model = PlatformerModel(size)
    print(model)
    view = PyGameWindowView(model, size)
    controller = PyGameKeyboardController(model)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()

if __name__ == '__main__':
    size = (900, 900)
    start_game(size)
