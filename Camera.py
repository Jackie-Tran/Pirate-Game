
from Objects import *
class Camera:

    def __init__(self, playState):
        self.worldPosition = 0
        self.playState = playState

    def update(self, player):
        if player.rect.right >= 500: #Constrains the player
            diff = player.rect.right - 500 #This difference is what offsets the whole world (Ex. If the playerX is 502, it would shift the world 2 pixels)
            player.rect.right = 500
            self.moveWorld(-diff)

        if player.rect.left <= 120: #Constrains the player
            diff = 120 - player.rect.left #This difference is what offsets the whole world (Ex. If the playerX is 110, it would shift the world 10 pixels)
            player.rect.left = 120
            self.moveWorld(diff)

    def moveWorld(self, velX):
        #Keeps track of where we are in the world
        self.worldPosition += velX

        #Moves everything in the map
        for gameObject in self.playState.allObjectList:
            if isinstance(gameObject, (Grass, Dirt, Sand, Crab, Coin, Chest, EnemyAIBox, Map)):
                gameObject.rect.x += velX


