import pygame
class Background:

    def __init__(self, image):
        self.AMOUNTOFIMAGES = 3
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (800, 600))
        self.playerIsMoving = False
        self.velX = -0.5
        self.x = [0, 800, 1600]
        self.y = 0

    def update(self):
        for i in range(self.AMOUNTOFIMAGES):
            if self.x[i] + 800 < 0: # When the image passes the screen we will move it to the right side outside the screen
                self.x[i] = 1600 - 5
            self.x[i] += self.velX

    def draw(self, window):
        #Draws 3 background images
        for i in range(self.AMOUNTOFIMAGES):
            window.blit(self.image, (self.x[i], self.y))



