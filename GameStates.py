import os

from Camera import Camera
from HUD import HUD
from PIL import Image
import Color
from Background import Background
from Objects import *
from SpriteSheet import SpriteSheet

pygame.init()

# Initializes music
pygame.mixer.music.load(os.path.join("res", "Sound", "music.wav"))  # Loads  the background music
pygame.mixer.music.play(-1, 0.0)  # Plays the music. -1 means the mmusic loops forever.


class MenuState:
    def __init__(self, gsm):
        print("MenuState initialized")
        # GameStateManager reference
        self.gsm = gsm

        # Background Image
        # FIND A WAY TO ADD ANIMATION TIME SO THAT IT DOESNT PLAY TOO FAST
        self.bgSpriteSheet = SpriteSheet(os.path.join("res", "MapState", "menu background.png"), 4)
        self.bgImage = None
        self.bgIndex = 1

        # Menu Option
        self.currentOption = 0
        self.maxOptions = 3
        self.boat = pygame.image.load(os.path.join("res", "MapState", "menu boat.png"))
        self.boatX = 175
        self.boatY = 0

        self.animationTimer = 0
        self.animationTime = 10

    def update(self):

        #Runs the animation for the background
        self.bgImage = self.bgSpriteSheet.grabImage(1, self.bgIndex, 800, 600)
        if self.animationTimer >= self.animationTime:
            if self.bgIndex < self.bgSpriteSheet.amountOfSprites:
                self.bgIndex += 1
                self.animationTimer = 0
            else:
                self.bgIndex = 1
                self.animationTimer = 0
        else:
            self.animationTimer += 1

        # Calculates the position of the boat according to the current option
        if self.currentOption == 0:
            self.boatY = 150 + (100 * self.currentOption)
        if self.currentOption == 1:
            self.boatY = 150 + (100 * self.currentOption)
        if self.currentOption == 2:
            self.boatY = 150 + (100 * self.currentOption)

    def draw(self, window):

        window.blit(self.bgImage, (0, 0))
        window.blit(self.boat, (self.boatX, self.boatY))

        # Text
        # Title
        font = pygame.font.Font(os.path.join("res", "arcade.ttf"), 50)
        title = font.render("Treasure Hunter", True, Color.RED)
        titleLocationRect = title.get_rect()
        titleLocationRect.center = (800 / 2, 50)
        window.blit(title, titleLocationRect)

        # Menu Options
        for option in range(self.maxOptions):
            if option == 0:
                play = font.render("Play", True, Color.AQUA)
                playLocationRect = play.get_rect()
                playLocationRect.center = (800 / 2, 200 + (100 * option))
                window.blit(play, playLocationRect)
            if option == 1:
                help = font.render("Help", True, Color.AQUA)
                helpLocationRect = help.get_rect()
                helpLocationRect.center = (800 / 2, 200 + (100 * option))
                window.blit(help, helpLocationRect)
            if option == 2:
                quit = font.render("Quit", True, Color.AQUA)
                quitLocationRect = quit.get_rect()
                quitLocationRect.center = (800 / 2, 200 + (100 * option))
                window.blit(quit, quitLocationRect)

    def keyHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.currentOption == self.maxOptions - 1:
                        self.currentOption = 0
                    else:
                        self.currentOption += 1
                if event.key == pygame.K_UP:
                    if self.currentOption == 0:
                        self.currentOption = self.maxOptions - 1
                    else:
                        self.currentOption -= 1

                if event.key == pygame.K_RETURN:
                    if self.currentOption == 0:
                        self.gsm.setState(self.gsm.MAPSTATE)
                    if self.currentOption == 1:
                        self.gsm.setState(self.gsm.HELPSTATE)
                    if self.currentOption == 2:
                        pygame.quit()
                        quit()


class HelpState:
    def __init__(self, gsm):
        self.gsm = gsm
        self.currentPage = 0
        #Setup for the images
        self.page1 = pygame.image.load(os.path.join("res", "HelpState", "help1.png"))
        self.page2 = pygame.image.load(os.path.join("res", "HelpState", "help2.png"))
        self.pages = [self.page1, self.page2]

        self.maxPages = len(self.pages) - 1

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.pages[self.currentPage], (0,0))

    def keyHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.currentPage > 0:
                        self.currentPage -= 1

                if event.key == pygame.K_DOWN:
                    if self.currentPage < self.maxPages:
                        self.currentPage += 1
                    elif self.currentPage == self.maxPages:
                        self.gsm.setState(self.gsm.MENUSTATE)
                if event.key == pygame.K_ESCAPE:
                    self.gsm.setState(self.gsm.MENUSTATE)

class MapState:
    global amountOfLevels
    global highestLevelComplete
    global currentLevel
    amountOfLevels = 5
    highestLevelComplete = 0
    currentLevel = 4

    def __init__(self, gsm):
        self.gsm = gsm
        self.HUD = HUD(self.gsm)
        global currentLevel
        global highestLevelComplete

        # If you beat all the levels
        if  highestLevelComplete == 5:
            self.gsm.setState(self.gsm.VICTORYSTATE)

        # Level Images
        self.levelImgRed = pygame.image.load(os.path.join("res", "MapState", "map level red.png"))
        self.levelImgRed = pygame.transform.scale(self.levelImgRed, (50, 50))

        self.levelImgBlue = pygame.image.load(os.path.join("res", "MapState", "map level blue.png"))
        self.levelImgBlue = pygame.transform.scale(self.levelImgBlue, (50, 50))

        self.levelImgGray = pygame.image.load(os.path.join("res", "MapState", "map level gray.png"))
        self.levelImgGray = pygame.transform.scale(self.levelImgGray, (50, 50))

        # Level Locations
        # Level1
        self.level1X = 100
        self.level1Y = 500

        # Level2
        self.level2X = 450
        self.level2Y = 425

        # Level 3
        self.level3X = 275
        self.level3Y = 325

        # Level 4
        self.level4X = 600
        self.level4Y = 250

        # Level 5
        self.level5X = 350
        self.level5Y = 125

        # Player boat (navigator)

        self.player = pygame.image.load(os.path.join("res", "MapState", "menu boat.png"))
        self.playerX = 90
        self.playerY = 450

    def update(self):
        if currentLevel == 1:
            self.playerX = self.level1X
            self.playerY = self.level1Y
        elif currentLevel == 2:
            self.playerX = self.level2X
            self.playerY = self.level2Y
        elif currentLevel == 3:
            self.playerX = self.level3X
            self.playerY = self.level3Y
        elif currentLevel == 4:
            self.playerX = self.level4X
            self.playerY = self.level4Y
        elif currentLevel == 5:
            self.playerX = self.level5X
            self.playerY = self.level5Y

    def draw(self, window):

        window.fill(Color.TEAL)

        # Levels
        # Level 1
        if highestLevelComplete == 0:  # if you have not completed any level
            window.blit(self.levelImgRed, (self.level1X, self.level1Y))
        elif highestLevelComplete > 0:  # if you have the level
            window.blit(self.levelImgBlue, (self.level1X, self.level1Y))
        else:
            window.blit(self.levelImgGray, (self.level1X, self.level1Y))

        # Level 2
        if highestLevelComplete == 1:  # if you have beat level 1
            window.blit(self.levelImgRed, (self.level2X, self.level2Y))
        elif highestLevelComplete > 1:  # if you have beat the level
            window.blit(self.levelImgBlue, (self.level2X, self.level2Y))
        else:
            window.blit(self.levelImgGray, (self.level2X, self.level2Y))

        # Level 3
        if highestLevelComplete == 2:  # if you have beat level 2
            window.blit(self.levelImgRed, (self.level3X, self.level3Y))
        elif highestLevelComplete > 2:  # if you have beat the level
            window.blit(self.levelImgBlue, (self.level3X, self.level3Y))
        else:
            window.blit(self.levelImgGray, (self.level3X, self.level3Y))

        # Level 4
        if highestLevelComplete == 3:  # if you have beat level 3
            window.blit(self.levelImgRed, (self.level4X, self.level4Y))
        elif highestLevelComplete > 2:  # if you have beat the level
            window.blit(self.levelImgBlue, (self.level4X, self.level4Y))
        else:
            window.blit(self.levelImgGray, (self.level4X, self.level4Y))

        # Level 5
        if highestLevelComplete == 4:  # if you have beat level 4
            window.blit(self.levelImgRed, (self.level5X, self.level5Y))
        elif highestLevelComplete > 3:  # if you have beat the level
            window.blit(self.levelImgBlue, (self.level5X, self.level5Y))
        else:
            window.blit(self.levelImgGray, (self.level5X, self.level5Y))

        # Draw Lines
        pygame.draw.line(window, Color.RED, (self.level1X + 50, self.level1Y + 25),
                         (self.level2X, self.level2Y + 25))
        pygame.draw.line(window, Color.RED, (self.level2X, self.level2Y + 25),
                         (self.level3X + 50, self.level3Y + 25))
        pygame.draw.line(window, Color.RED, (self.level3X + 50, self.level3Y + 25),
                         (self.level4X, self.level4Y + 25))
        pygame.draw.line(window, Color.RED, (self.level4X, self.level4Y + 25),
                         (self.level5X + 50, self.level5Y + 25))

        # Player
        window.blit(self.player, (self.playerX, self.playerY))
        self.HUD.draw(window)
    def keyHandler(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.gsm.setState(self.gsm.MENUSTATE)

                if event.key == pygame.K_UP:
                    self.moveUp()

                if event.key == pygame.K_DOWN:
                    self.moveDown()

                if event.key == pygame.K_RETURN:
                    self.gsm.setState(self.gsm.PLAYSTATE)

    def moveUp(self):
        global currentLevel
        if currentLevel <= highestLevelComplete:
            currentLevel += 1

    def moveDown(self):
        global currentLevel
        if currentLevel > 1:
            currentLevel -= 1

    def nextLevel(self):
        global highestLevelComplete
        highestLevelComplete += 1


class PlayState():
    def __init__(self, gsm):
        self.gsm = gsm
        self.background = Background(os.path.join("res", "PlayState", "background.png"))
        self.camera = Camera(self)
        self.HUD = HUD(self.gsm)
        # Key handling
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False

        self.spriteSheet = SpriteSheet(os.path.join("res", "PlayState", "Spritesheet.png"), 1)

        # Holds all the objects in the game
        self.allObjectList = pygame.sprite.Group()
        self.activeObjectList = pygame.sprite.Group()
        self.terrainList = pygame.sprite.Group()
        self.interactableList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.enemyAIList = pygame.sprite.Group()
        self.player = None

        self.level = currentLevel  # Sets the current level
        self.loadLevel(self.level)  # Loads the level

    def update(self):
        # Fixes the bug where if you instantly switch directions you will stop moving

        if self.leftKeyDown:
            self.player.moveLeft()
        if self.rightKeyDown:
            self.player.moveRight()
        self.camera.update(self.player)
        self.HUD.update()

        # PERFORMANCE FIX
        # This block  makes it so that only the objects that are within a  certain range of the player will it update it and draw it.
        # Runs through all the objects in the game and if it is within the range of the camera then add it to the active objects list.
        for object in self.allObjectList:
            if object.rect.right > -160 and object.rect.left < 960:
                self.activeObjectList.add(object)
            else:
                self.activeObjectList.remove(object)
        self.activeObjectList.update()  # Updates all the active objects
        self.background.update()

    def draw(self, window):
        window.fill(Color.CYAN)
        self.background.draw(window)
        self.activeObjectList.draw(window)  # Draws all the active objects
        self.HUD.draw(window)

    def keyHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.leftKeyDown = True

                if event.key == pygame.K_RIGHT:
                    self.rightKeyDown = True

                if event.key == pygame.K_UP:
                    self.player.jump(9.5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.stopMoving()
                    self.leftKeyDown = False

                if event.key == pygame.K_RIGHT:
                    self.player.stopMoving()
                    self.rightKeyDown = False

    def loadLevel(self, level):  # Reads the pixels of an image for their RGB Values and depending on these values, create a object at that position
        if level == 1:
            mapData = Image.open(os.path.join("res", "PlayState", "Level1Map(sand).png"))  # Loads level1
        elif level == 2:
            mapData = Image.open(os.path.join("res", "PlayState", "Level2Map(sand).png"))
        elif level == 3:
            mapData = Image.open(os.path.join("res", "PlayState", "Level3Map.png"))
        elif level == 4:
            mapData = Image.open(os.path.join("res", "PlayState", "Level4Map.png"))
        elif level == 5:
            mapData = Image.open(os.path.join("res", "PlayState", "Level5Map.png"))
        mapWidth, mapHeight = mapData.size  # Gets the width and height of the image

        print("WIDTH: " + str(mapWidth) + " HEIGHT: " + str(mapHeight))  # For debugging
        for x in range(mapWidth):  # Runs through all the colomns
            for y in range(mapHeight):  # Runs through all the rows

                currentPixel = mapData.getpixel((x, y))
                red = currentPixel[0]  # RED VALUE
                green = currentPixel[1]  # GREEN VALUE
                blue = currentPixel[2]  # BLUE VALUE
                alpha = currentPixel[3]  # ALPHA VALUE

                # Checks for player spawner
                if red == 255 and green == 0 and blue == 255 and alpha == 255:
                    self.player = Player(x * 32, y * 32, self, self.gsm, self.spriteSheet, )
                    self.allObjectList.add(self.player)

                # Check for Grass blocks
                if red == 0 and green == 255 and blue == 0 and alpha == 255:
                    self.terrainList.add(Grass(x * 32, y * 32, self.spriteSheet))

                # Checks for dirt blocks
                if red == 222 and green == 144 and blue == 61 and alpha == 255:
                    self.terrainList.add(Dirt(x * 32, y * 32, self.spriteSheet))

                # Checks for sand blocks
                if red == 243 and green == 225 and blue == 179 and alpha == 255:
                    self.terrainList.add(Sand(x * 32, y * 32, self.spriteSheet))

                # Check for coin blocks
                if red == 255 and green == 255 and blue == 0 and alpha == 255:
                    self.interactableList.add(Coin(x * 32, y * 32, self.spriteSheet))

                # Checks for enemy AI detection
                if red == 0 and green == 0 and blue == 0 and alpha == 255:
                    self.enemyAIList.add(EnemyAIBox(x * 32, y * 32, self))

                # Checks for Crab enemy
                if red == 255 and green == 0 and blue == 0 and alpha == 255:
                    self.enemyList.add(Crab(x * 32, y * 32, self, self.spriteSheet))

                # Checks for map piece
                if red == 0 and green == 0 and blue == 255 and alpha == 255:
                    self.interactableList.add(Map(x * 32, y * 32, self.spriteSheet))

                if red == 0 and green == 255 and blue == 255 and alpha == 255:
                    self.interactableList.add(Chest(x * 32, y * 32, self, self.spriteSheet))
                    print("Chest addded")

        # Adds all the groups into one master group
        self.allObjectList.add(self.terrainList)
        self.allObjectList.add(self.interactableList)
        self.allObjectList.add(self.enemyList)
        self.allObjectList.add(self.enemyAIList)

    def removeObject(self, object):
        # Removes a game object from the game
        self.allObjectList.remove(object)
        self.activeObjectList.remove(object)

    def nextLevel(self):
        global highestLevelComplete
        global currentLevel

        # This makes it so that if you play a level you already beat, it doesn't unlock a new level
        if currentLevel > highestLevelComplete:
            highestLevelComplete += 1

    def reset(self):
        global highestLevelComplete
        global currentLevel

        highestLevelComplete = 0
        currentLevel = 1
        self.HUD.reset()


class VictoryState():
    def __init__(self, gsm):
        self.gsm = gsm

    def update(self):
        pass

    def draw(self, window):
        window.fill(0)

        # Dras the Congratulations texxt
        titleFont = pygame.font.Font(os.path.join("res", "arcade.ttf"), 72)
        gameOver = titleFont.render("YOU WIN", True, Color.WHITE)
        gameOverLocation = gameOver.get_rect()
        gameOverLocation.center = (400, 300)
        window.blit(gameOver, gameOverLocation)

        # Draws the instructions for the user
        subFont = pygame.font.Font(os.path.join("res", "arcade.ttf"), 16)
        instructions = subFont.render("Press enter to go to the menu", True, Color.WHITE)
        instructionsLocation = instructions.get_rect()
        instructionsLocation.center = (400, 400)
        window.blit(instructions, instructionsLocation)

    def keyHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.gsm.setState(self.gsm.MENUSTATE)

class GameOverState():
    def __init__(self, gsm):
        self.gsm = gsm

    def update(self):
        pass

    def draw(self, window):
        window.fill(0)

        # Dras the GAMEOVER texxt
        titleFont = pygame.font.Font(os.path.join("res", "arcade.ttf"), 72)
        gameOver = titleFont.render("GAME OVER", True, Color.WHITE)
        gameOverLocation = gameOver.get_rect()
        gameOverLocation.center = (400, 300)
        window.blit(gameOver, gameOverLocation)

        # Draws the instructions for the user
        subFont = pygame.font.Font(os.path.join("res", "arcade.ttf"), 16)
        instructions = subFont.render("Press enter to go to the menu", True, Color.WHITE)
        instructionsLocation = instructions.get_rect()
        instructionsLocation.center = (400, 400)
        window.blit(instructions, instructionsLocation)

    def keyHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    self.gsm.setState(self.gsm.MENUSTATE)

