from Images import  *
import pygame
import time
import random
from  player import  *
from Images import *

START_STATE = 0
PLAYING_STATE = 1
GAME_OVER_STATE = 2
SCORE_DISPLAY_STATE = 3

class Game:
    def __init__(self):
        self.start = pygame.image.load("start.png")
        self.gameoverScreen = pygame.image.load("gameover.png")
        self.scoreboard = pygame.image.load("finish.png")
        self.start = pygame.transform.scale(self.start, (600, 650))
        self.scoreboard = pygame.transform.scale(self.scoreboard, (600, 650))
        self.gameoverScreen = pygame.transform.scale(self.gameoverScreen, (600, 650))
        self.startgame()
        pygame.init()
        self.screen = pygame.display.set_mode((600, 650))
    def handleevent(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == START_STATE:
                if event.key == pygame.K_s:
                    self.state = PLAYING_STATE
                elif event.key == pygame.K_s:
                    self.state = SCORE_DISPLAY_STATE
            elif self.state == PLAYING_STATE:
                if self.player1.isAlive():
                    self.player1.key(event.key)
                if self.player2.isAlive():
                    self.player2.key(event.key)
            elif self.state == GAME_OVER_STATE:
                self.handleGameOverState(event)
                if self.finished_entering_name:
                    self.state = SCORE_DISPLAY_STATE
                    self.writeScore()
            # elif self.state == SCORE_DISPLAY_STATE:
            #     if event.key == pygame.K_RETURN:
            #         self.state = START_STATE

    def update(self):
        if self.state == PLAYING_STATE:
            self.move()

    def startgame(self):
        self.player1 = Player(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,210, 210 )
        self.player2 = Player(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,330, 360)
        self.applex = 0
        self.appley = 0
        self.bombx = 0
        self.bomby = 0
        self.putApple()
        self.putBomb()
        self.state = START_STATE
        self.finished_entering_name = False
        self.name = ""
    def move(self):
        ate1 = self.updatePlayer(self.player1)
        ate2 = self.updatePlayer(self.player2)
        someoneAte = ate1 or ate2

        if someoneAte:
            self.putApple()
            self.putBomb()

        if not self.player1.isAlive() and not self.player2.isAlive():
            self.gameover()

    def updatePlayer(self, player):
        if not player.isAlive():
            return False

        newData = player.move()
        if player.isLocationInvalid():
            player.num_hearts = 0

        player.newNode(newData)

        ate = False
        if player.ate(self.applex, self.appley):
            ate = True
            player.score += 1
        else:
            player.pushTail()

        if player.ate(self.bombx, self.bomby):
            ate = True
            player.num_hearts -= 1

        return ate

    def printList(self):
        if self.state == START_STATE:
            self.screen.blit(self.start, (0, 0))
        elif self.state == PLAYING_STATE:
            self.screen.blit(apple, (self.applex, self.appley))
            if self.player1.isAlive():
                self.player1.print(self.screen, 600)
            if self.player2.isAlive():
                self.player2.print(self.screen, 560)
            self.screen.blit(bomb, (self.bombx, self.bomby))
        elif self.state == GAME_OVER_STATE:
            self.screen.blit(self.gameoverScreen, (0, 0))
        elif self.state == SCORE_DISPLAY_STATE:
            self.displayScores()
            self.screen.blit(self.scoreboard, (0, 0))

    def putApple(self):
        flag = True
        while flag:
            x = random.randint(1,19)
            y = random.randint(1,19)
            x*=30
            y*=30
            temp = self.player1.root
            while temp != 0:
                if temp.loc_x == x and temp.loc_y == y:
                    break
                temp = temp.next
            if temp == 0:
                flag = False
        self.applex = x
        self.appley = y
    # def ateApple(self):
    #     return self.player.loc_x == self.applex and self.player.loc_y == self.appley
    def putBomb(self):
        flag = True
        while flag:
            x = random.randint(1, 19)
            y = random.randint(1, 19)
            x *= 30
            y *= 30
            temp = self.player1.root
            while temp != 0:
                if temp.loc_x == x and temp.loc_y == y:
                    break
                temp = temp.next
            if temp == 0:
                flag = False
        self.bombx = x
        self.bomby = y
    # def ateBomb(self):
    #     return self.player.loc_x == self.bombx and self.player.loc_y == self.bomby
    def gameover(self):
        self.state = GAME_OVER_STATE
        pygame.draw.rect(self.screen, (50, 50, 50), pygame.Rect(350, 350, 150, 15))
        pygame.display.flip()
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(350, 350, 148, 13))
        pygame.display.flip()

    def handleGameOverState(self, event):
        pygame.draw.rect(self.screen, (50, 50, 50), pygame.Rect(350, 350, 150, 15))
        pygame.display.flip()
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(350, 350, 148, 13))
        pygame.display.flip()
        if event.key == pygame.K_RETURN:
            self.finished_entering_name = True
        elif event.key == pygame.K_BACKSPACE \
                and not (len(self.name) == 0):
            self.name = self.name[:-1]
        else:
            self.name += event.unicode

        font2 = pygame.font.SysFont('chalkduster.ttf', 15, bold=False)
        img2 = font2.render(self.name, True, (50, 50, 50))
        self.screen.blit(img2, (350, 350))
        pygame.display.update()

    def displayScores(self):
        f = open("scores.txt", 'r', encoding='utf-8')
        all_lines = f.readlines()
        num = 240
        for line in all_lines:
            x = line.split()
            self.screen.blit(pygame.font.SysFont('Comic Sans MS', 30).render(str(x[0]), False, (0, 0, 0)), (35, num))
            self.screen.blit(pygame.font.SysFont('Comic Sans MS', 30).render(str(x[1]), False, (0, 0, 0)), (230, num))
            pygame.display.flip()
            num += 75
        f.close()

    def writeScore(self):
        score = max(self.player1.score, self.player2.score)
        scores = []
        names = []
        f = open("scores.txt", 'r', encoding='utf-8')
        all_lines = f.readlines()
        for line in all_lines:
            x = line.split()
            scores.append(x[1])
            names.append(x[0])
        f.close()

        newScores = []
        newNames = []
        flag = True
        for i in range(5):
            if score > int(scores[i]) and flag == True:
                flag = False
                newScores.append(score)
                newNames.append(name)
            if flag == False and i == 4:
                break
            newScores.append(scores[i])
            newNames.append(names[i])

        with open('scores.txt', 'w', encoding='utf-8') as f:
            for i in range(5):
                f.writelines(newNames[i] + " " + str(newScores[i]) + "\n")