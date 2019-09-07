"""
Name: Jackie Tran
Date: May 21, 2016
Program: Treasure Hunter (IDLE VERSION)
Description: ICS20 final assignment. This game is a 2D platformer where you play as a pirate that follows a map to find the treasure.
The game requires you to have python 3.4, the Pygame library and the Pillow library(PIL) or you can run the executable.
THIS VERSION OF THE GAME DOES NOT NEED PYCHARM
It is best if you read the help menu first so you understand how the game works.
"""

import pygame, os

import Color
from GameStateManager import GameStateManager

pygame.init()
print(pygame.display.get_driver())

# Window Variables
WIDTH = 800
HEIGHT = 600
TITLE = "Treasure Hunter"
ICON = pygame.image.load(os.path.join("res", "MapState","menu boat.png"))
ICON = pygame.transform.scale(ICON, (32, 32))

# Setup window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
pygame.display.set_icon(ICON)

# Game Variables
running = True
clock = pygame.time.Clock()
FPS = 60

gsm = GameStateManager()


def update():
    gsm.update()


def draw():
    gsm.draw(window)
    pygame.display.update()


def keyHandler():
    # IMPORTANT! There has to be code running here or else the game will crash
    gsm.keyHandler()


while running:
    window.fill(Color.WHITE)
    update()
    draw()
    keyHandler()
    clock.tick(FPS)
    pygame.display.set_caption(TITLE + str(clock))  # For debugging. Sets titel of window to show FPS
