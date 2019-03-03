#!/usr/bin/python3
import pygame
from pygame.locals import *
import configparser
import config
window = None
screen = Rect(0, 0, config.width, config.height)

rect_guess = Rect(0, 0, config.width * 0.75, config.height)
rect_feedback = Rect(config.width * 0.75, 0, config.width * 0.25, config.height)
surface_guess = pygame.Surface(rect_guess.size)
surface_guess.fill(config.background1)
surface_feedback = pygame.Surface(rect_feedback.size)
surface_feedback.fill(config.background2)

class GameException(BaseException):
    pass

def init():
    global window
    window = pygame.display.set_mode(screen.size)
    pygame.display.set_caption('N-digits')

def loop():
    # game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise GameException()
    
    # draw
    window.blits(((surface_guess, rect_guess), (surface_feedback, rect_feedback)))
    pygame.display.update()

import sys
if __name__ == '__main__':
    init()
    try:
        while True:
            loop()
    except GameException as e:
        pass
    pygame.quit()