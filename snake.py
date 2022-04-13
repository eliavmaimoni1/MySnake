import time
import pygame
import random
from game import *
import sys
import threading

pygame.init()
screen = pygame.display.set_mode((600, 650))

head_right = pygame.image.load('snake_graphics/Graphics/head_right.png')
head_left = pygame.image.load('snake_graphics/Graphics/head_left.png')
head_down = pygame.image.load('snake_graphics/Graphics/head_down.png')
head_up = pygame.image.load('snake_graphics/Graphics/head_up.png')
tail_left = pygame.image.load('snake_graphics/Graphics/tail_left.png')
tail_right = pygame.image.load('snake_graphics/Graphics/tail_right.png')
tail_down = pygame.image.load('snake_graphics/Graphics/tail_down.png')
tail_up = pygame.image.load('snake_graphics/Graphics/tail_up.png')
snake_body_left_down = pygame.image.load('snake_graphics/Graphics/body_bottomright.png')
snake_body_right_down = pygame.image.load('snake_graphics/Graphics/body_bottomleft.png')
snake_body_left_up = pygame.image.load('snake_graphics/Graphics/body_topright.png')
snake_body_right_up = pygame.image.load('snake_graphics/Graphics/body_topleft.png')
snake_body_horizontal = pygame.image.load('snake_graphics/Graphics/body_horizontal.png')
snake_body_vertical = pygame.image.load('snake_graphics/Graphics/body_vertical.png')
apple = pygame.image.load('snake_graphics/Graphics/apple.png')
background = pygame.image.load('snake_graphics/Graphics/background.jpg')
background = pygame.transform.scale(background, (600, 600))
black_box = pygame.image.load('snake_graphics/Graphics/blackbox.png')
black_box = pygame.transform.scale(black_box , (600,50))
bomb = pygame.image.load('snake_graphics/Graphics/bomb.png')
bomb = pygame.transform.scale(bomb , (30,30))
heart = pygame.image.load('snake_graphics/Graphics/heart pixel art 48x48.png')
heart = pygame.transform.scale(heart, (30, 30))
PLAYING_STATE = 0
GAME_OVER_STATE = 1



class Node:
    def __init__(self, data, loc_x, loc_y):
        self.data = data
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.next = 0

    def printData(self):
        screen.blit(self.data, (self.loc_x, self.loc_y))

class Snake:
    def __init__(self):
        self.startgame()
    def handleevent(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == PLAYING_STATE:
                self.key(event.key)
            elif self.state == GAME_OVER_STATE:
                if event.key == pygame.K_RETURN:
                    self.startgame()


    def update(self):
        if self.state == PLAYING_STATE:
            self.move()
        elif self.state == GAME_OVER_STATE:
            print("game over")
    def startgame(self):
        self.root = 0
        self.loc_x = 330
        self.loc_y = 300
        self.dir = 1
        self.pniya = 0
        self.applex = 0
        self.appley = 0
        self.bombx = 0
        self.bomby = 0
        self.score = 0
        self.root = Node(tail_left, 240, 300)
        self.root.next = Node(snake_body_horizontal, 270, 300)
        self.root.next.next = Node(snake_body_horizontal, 300, 300)
        self.root.next.next.next = Node(head_right, 330, 300)
        self.putApple()
        self.putBomb()
        self.num_hearts = 3
        self.state = PLAYING_STATE

    def size(self):
        count = 0
        temp = self.root
        while temp != 0:
            temp = temp.next
            count += 1
        return count
    def boom(self):
        temp = self.root
        while temp != 0:
            if temp.loc_x == self.loc_x and temp.loc_y == self.loc_y:
                return True
            temp = temp.next
        return self.loc_x < 0 or self.loc_x >= 600 or self.loc_y < 0 or self.loc_y >= 600
    def move(self):
        # 1 = right , 2 = left , 3 = up , 4 = down
        if self.dir == 1:
            self.loc_x += 30
            newData = head_right
        elif self.dir == 2:
            self.loc_x -= 30
            newData = head_left
        elif self.dir == 3:
            self.loc_y -= 30
            newData = head_up
        elif self.dir == 4:
            self.loc_y += 30
            newData = head_down
        if self.boom() == True:
            print("Game Over")
            self.gameover()
        newNode = Node(newData, self.loc_x, self.loc_y)
        temp = self.root
        while temp.next != 0:
            temp = temp.next
        if self.pniya != 0:
            if self.pniya == 1 and self.dir == 3 or self.pniya == 4 and self.dir == 2:
                temp.data = snake_body_right_up
            elif self.pniya == 1 and self.dir == 4 or self.pniya == 3 and self.dir == 2:
                temp.data = snake_body_right_down
            elif self.pniya == 2 and self.dir == 3 or self.pniya == 4 and self.dir == 1:
                temp.data = snake_body_left_up
            elif self.pniya == 2 and self.dir == 4 or self.pniya == 3 and self.dir == 1:
                temp.data = snake_body_left_down
        else:
            if self.dir < 3:
                temp.data = snake_body_horizontal
            else:
                temp.data = snake_body_vertical

        temp.next = newNode
        self.pniya = 0
        if self.ate():
            self.putApple()
            self.score += 1
            self.putBomb()
        else:
            self.pushTail()
        if self.ateBomb():
            self.putBomb()
            self.num_hearts -= 1
            if self.num_hearts == 0:
                self.gameover()






    def printList(self):
        temp = self.root
        while temp != 0:
            temp.printData()
            temp = temp.next
        screen.blit(apple, (self.applex,self.appley))
        screen.blit(pygame.font.SysFont('Comic Sans MS', 30).render('your score is : ' + str(self.score), False, (255,255,255)), (180, 600))
        screen.blit(bomb, (self.bombx, self.bomby))

        num = 30
        for i in range(self.num_hearts):
            print(i)
            screen.blit(heart, (20 + num, 610))
            num += 35


    def pushTail(self):
        temp = 0
        if self.root.next.data == snake_body_left_up and self.root.data == tail_right:
            temp = tail_down
        elif self.root.next.data == snake_body_left_up and self.root.data == tail_up:
            temp = tail_left

        elif self.root.next.data == snake_body_right_down and self.root.data == tail_left:
             temp = tail_up
        elif self.root.next.data == snake_body_right_down and self.root.data == tail_down:
             temp = tail_right

        elif self.root.next.data == snake_body_right_up and self.root.data == tail_left:
            temp = tail_down
        elif self.root.next.data == snake_body_left_down and self.root.data == tail_down:
            temp = tail_left
        elif self.root.next.data == snake_body_left_down and self.root.data == tail_right:
            temp = tail_up
        elif self.root.next.data == snake_body_right_up and self.root.data == tail_up:
            temp = tail_right


        elif self.root.next.data == snake_body_horizontal:
            if self.root.loc_x < self.root.next.loc_x:
               temp = tail_left
            else:
                temp = tail_right
        elif self.root.next.data == snake_body_vertical:
            if self.root.loc_y > self.root.next.loc_y:
               temp = tail_down
            else:
                temp = tail_up
        else:
            print("error")

        self.root = self.root.next
        self.root.data = temp
    def key(self,k):
        if k == pygame.K_w and self.dir < 3:
            self.pniya = self.dir
            self.dir = 3
        elif k == pygame.K_s and self.dir < 3:
            self.pniya = self.dir
            self.dir = 4
        elif k == pygame.K_d and self.dir > 2:
            self.pniya = self.dir
            self.dir = 1
        elif k == pygame.K_a and self.dir > 2:
            self.pniya = self.dir
            self.dir = 2
    def putApple(self):
        flag = True
        while flag:
            x = random.randint(1,19)
            y = random.randint(1,19)
            x*=30
            y*=30
            temp = self.root
            while temp != 0:
                if temp.loc_x == x and temp.loc_y == y:
                    break
                temp = temp.next
            if temp == 0:
                flag = False
        self.applex = x
        self.appley = y
    def ate(self):
        return self.loc_x == self.applex and self.loc_y == self.appley
    def putBomb(self):
        flag = True
        while flag:
            x = random.randint(1, 19)
            y = random.randint(1, 19)
            x *= 30
            y *= 30
            temp = self.root
            while temp != 0:
                if temp.loc_x == x and temp.loc_y == y:
                    break
                temp = temp.next
            if temp == 0:
                flag = False
        self.bombx = x
        self.bomby = y
    def ateBomb(self):
        return self.loc_x == self.bombx and self.loc_y == self.bomby
    def gameover(self):
        self.state = GAME_OVER_STATE
def gui():
    screen.blit(background, (0, 0))
    screen.blit(black_box, (0, 600))
    s.printList()
    pygame.display.flip()


s = Game()
s.printList()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             running = False
        s.handleevent(event)
    s.update()
    gui()
    s.printList()
    time.sleep(0.15)










