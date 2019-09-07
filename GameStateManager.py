from GameStates import *

class GameStateManager:
    def __init__(self):
        self.STATES_IN_GAME = 6
        # A list that will contain all the gamestates in the game
        self.gameStates = [None] * self.STATES_IN_GAME

        # Assigns a number to the different gamestates in the game
        self.MENUSTATE = 0
        self.HELPSTATE = 1
        self.MAPSTATE = 2
        self.PLAYSTATE = 3
        self.GAMEOVERSTATE = 4
        self.VICTORYSTATE = 5
        self.currentState = None

        # Sets the current state of the game
        self.currentState = self.MENUSTATE
        self.loadState(self.currentState)
        print(self.gameStates)

    def update(self):
        self.gameStates[self.currentState].update()

    def draw(self, window):
        self.gameStates[self.currentState].draw(window)

    def keyHandler(self):
        self.gameStates[self.currentState].keyHandler()

    # Sets the element in the "gameStates" list to a gamestate class
    def loadState(self, state):

        if state == self.MENUSTATE:  # Menu
            self.gameStates[state] = MenuState(self)

        if state == self.HELPSTATE:  # Help
            self.gameStates[state] = HelpState(self)

        if state == self.MAPSTATE:  # Map selector
            self.gameStates[state] = MapState(self)

        if state == self.PLAYSTATE: # Ingame
            self.gameStates[state] = PlayState(self)

        if state == self.GAMEOVERSTATE:
            self.gameStates[state] = GameOverState(self)

        if state == self.VICTORYSTATE:
            self.gameStates[state] = VictoryState(self)


    # Sets the element in the "gameStates" to nothing. For optimization
    def unloadState(self, state):
        self.gameStates[state] = None

    # Sets the currentState to a gamestate
    def setState(self, state):
        self.unloadState(self.currentState)  # unloads the current gamestate
        self.currentState = state  # sets the current gamestate to the state we want to change to
        self.loadState(self.currentState)  # loads the new gamestate according to what our currentState is
