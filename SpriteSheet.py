import pygame

pygame.init()


class SpriteSheet:
    def __init__(self, path, amountOfSprites):
        self.spriteSheet = pygame.image.load(path)
        self.image = None
        self.amountOfSprites = amountOfSprites

    #Images start counting from 1. If want to start counting from 1 (width * col - width, height * row - height)
    def grabImage(self, col, row, width, height):
        #pygame.Surface.subsurface grabs a rectangle of the image you want to use
        image = self.spriteSheet.subsurface((width * col - width, height * row - height, width, height))
        return image.convert()
