import pygame, os, Color


class HUD:
    global lives
    lives = 5
    global score
    score = 0
    def __init__(self, gsm):
        self.gsm = gsm

    def update(self):
        pass

    def draw(self, window):
        font = pygame.font.Font(os.path.join("res", "arcade.ttf"), 32)
        livesText = font.render("Lives: " + str(lives), False, Color.WHITE)
        scoreText = font.render("Score: " + str(score), False, Color.WHITE)

        window.blit(livesText, (0, 0))
        window.blit(scoreText, (0, 50))

    def increaseScore(self, amount):
        global score
        score += amount

    def decreaseScore(self, amount):
        global score
        score -= amount
    def reset(self):
        global lives
        global score
        lives = 5
        score = 0

    def getLives(self):
        global lives
        return lives

    def decreaseLives(self):
        global lives
        lives -= 1

    def increaseLives(self):
        global lives
        lives += 1