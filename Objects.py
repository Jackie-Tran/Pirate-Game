import pygame

pygame.init()

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, playState, gsm, spriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.playState = playState
        self.spawnX = x
        self.spawnY = y
        self.gsm = gsm
        self.velX = 0
        self.velY = 0
        self.width = 64
        self.height = 96
        self.canJump = False
        self.isRunningIntoBlock = False
        self.pirateRight = spriteSheet.grabImage(1,5,32, 32)
        self.pirateRight.set_colorkey((255, 0, 255))
        self.pirateRight = pygame.transform.scale(self.pirateRight, (self.width, self.height))
        self.pirateLeft = pygame.transform.flip(self.pirateRight, True, False)
        self.imageList = [self.pirateLeft, self.pirateRight]

        self.image = self.pirateRight
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        self.checkCollision()
        if self.playState.leftKeyDown:
            self.image = self.imageList[0]
        elif self.playState.rightKeyDown:
            self.image = self.imageList[1]

    def draw(self, window):
        window.blit(self.image, self.rect)

    def checkCollision(self):
        self.calculateGravity()

        #Checks if you fall through a hole
        if self.rect.y > 650:
            self.death()

        #Runs collision for all the objects

        #Moving left/right
        self.rect.x += self.velX
        # Checks for collision between player sprite and all the objects in the allObjectList group list
        objectCollisionList = pygame.sprite.spritecollide(self, self.playState.allObjectList, False)
        for gameObject in objectCollisionList:
            if isinstance(gameObject, (Coin)): # Collision with coin will increase score by 100
                self.playState.removeObject(gameObject)
                self.playState.HUD.increaseScore(100)
            if isinstance(gameObject, (Grass, Dirt, Sand)): #Collision with terrain objects (for x axis only)
                if self.velX > 0: #Moving right
                    self.rect.right = gameObject.rect.left
                    self.velX = 0
                elif self.velX < 0: #Moving left
                    self.rect.left = gameObject.rect.right
                    self.velX = 0

            #if isinstance(gameObject, (Crab)): # Collision with the crab. Will decrease lives and sends you back to map
                #self.death()


            if isinstance(gameObject, Map):
                self.playState.nextLevel()
                self.gsm.setState(self.gsm.MAPSTATE)
                self.playState.HUD.increaseScore(750)

            if isinstance(gameObject, Chest):
                self.playState.HUD.increaseScore(2500)
                self.playState.HUD.reset()
                self.playState.reset()
                self.gsm.setState(self.gsm.VICTORYSTATE)



        #Moving up/down
        self.rect.y += self.velY
        objectCollisionList = pygame.sprite.spritecollide(self, self.playState.allObjectList, False)
        for gameObject in objectCollisionList:
            if isinstance(gameObject, Coin): # Collision with coins
                self.playState.HUD.increaseScore(100)
                self.playState.removeObject(gameObject)
            if isinstance(gameObject, (Grass, Dirt, Sand)): # Collision with all terrain objects
                if self.velY > 0: # Falling down
                    self.rect.bottom = gameObject.rect.top
                    self.canJump = True
                elif self.velY < 0: # Jumping
                    self.rect.top = gameObject.rect.bottom
                #Stops any vertical movement
                self.velY = 0
            if isinstance(gameObject, (Crab)):
                if self.velY > 0:
                    self.playState.removeObject(gameObject)
                    self.velY = 0
                    self.canJump = True
                    self.jump(7)

    def death(self):
        self.playState.HUD.decreaseLives()
        if self.playState.HUD.getLives() > 0: #Checks if the player runs out of lives
            self.gsm.setState(self.gsm.MAPSTATE)
        else:
            self.playState.reset()
            self.gsm.setState(self.gsm.GAMEOVERSTATE)


    def calculateGravity(self):
        #Gradually increases the affects of gravity the longer you are in the air
        #self.velY += 0.35
        if self.velY == 0:
            self.velY = 1
        else:
            self.velY += 0.35

    #Player movement
    def moveLeft(self):
        self.velX = -5

    def moveRight(self):
        self.velX = 5

    def stopMoving(self):
        self.velX = 0

    def jump(self, jumpPower):
        if self.canJump:
            self.velY -= jumpPower
            self.canJump = False

class Dirt(pygame.sprite.Sprite):

    def __init__(self, x, y, spriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = spriteSheet.grabImage(2, 1, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Grass(pygame.sprite.Sprite):

    def __init__(self, x, y, spriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = spriteSheet.grabImage(1, 1, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Sand(pygame.sprite.Sprite):

    def __init__(self, x, y, spriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = spriteSheet.grabImage(3, 1, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y, spriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.spriteSheet = spriteSheet
        self.width = 32
        self.height = 32
        self.coinSprites = []

        self.image = spriteSheet.grabImage(1, 2, self.width, self.height)
        self.image.set_colorkey((255,0,255,255)) #Sets the color key to the pink background of the spritesheet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def draw(self, window):
        pass

class Crab(pygame.sprite.Sprite):
    def __init__(self, x, y, playState, spriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.playState = playState
        self.spawnX = x
        self.spawnY = y
        self.width = 32
        self.height = 32

        #AI
        self.velX = -2

        #Image
        self.image = spriteSheet.grabImage(1, 3, self.width, self.height)
        self.image.set_colorkey((255, 0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.checkCollision()

    def draw(self, window):
        window.blit(self.image, self.rect)

    def checkCollision(self):

        #Moving left/right
        self.rect.x += self.velX
        objectCollisionList = pygame.sprite.spritecollide(self, self.playState.allObjectList, False)
        for gameObject in objectCollisionList:
            if isinstance(gameObject, (Grass, Dirt, Sand)):
                if self.velX > 0: #Moving right
                    self.rect.right = gameObject.rect.left
                    self.velX = -self.velX
                elif self.velX < 0: #Moving left
                    self.rect.left = gameObject.rect.right
                    self.velX = -self.velX

    def respawn(self):
        self.rect.x = self.spawnX
        self.rect.y = self.spawnY
        self.velX = -2


class EnemyAIBox(pygame.sprite.Sprite):
    """
    This class is used for the movement of the enemies. It is placed at places where the enemy will fall off the map.
    When they collide, the velX of the enemy object is set to the opposite of the velX of the enemy so that it
    turns around.
    """


    def __init__(self, x, y, playState):
        pygame.sprite.Sprite.__init__(self)
        self.playState = playState
        self.width = 32
        self.height = 32
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Checks for collision with terrain
        enemyCollisionList = pygame.sprite.spritecollide(self, self.playState.enemyList, False)
        for enemy in enemyCollisionList:
            if enemy.velX > 0:  # Enemy is moving right
                enemy.rect.right = self.rect.left - 1#Stops a bug where the enemy would get glitched with the ai detection boxes
                enemy.velX = -enemy.velX
            elif enemy.velX < 0:  # Enemy is moving left
                enemy.rect.left = self.rect.right + 1#Stops a bug where the enemy would get glitched with the ai detection boxes
                enemy.velX = -enemy.velX


class Map(pygame.sprite.Sprite):

    def __init__(self, x, y, spriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = spriteSheet.grabImage(2, 2, self.width, self.height)
        self.image.set_colorkey((255,0,255,255)) #Sets the color key of the image to the pink of the spritesheet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, playState, spriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.playState = playState
        self.width = 64
        self.height = 32
        self.image = spriteSheet.grabImage(2, 2, self.width, self.height)
        self.image.set_colorkey((255,0,255,255)) #Sets the color key of the image to the pink of the spritesheet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y










