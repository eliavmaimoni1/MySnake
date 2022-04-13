from Images import *


class Node:
    def __init__(self, data, loc_x, loc_y):
        self.data = data
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.next = 0

    def printData(self, screen):
        screen.blit(self.data, (self.loc_x, self.loc_y))

class Player:
    def __init__(self, upKey, downKey, leftKey, rightKey, loc_x, loc_y):
        self.upKey = upKey
        self.downKey = downKey
        self.leftKey = leftKey
        self.rightKey = rightKey
        self.root = 0
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.dir = 1
        self.pniya = 0
        self.root = Node(tail_left, 240, 300)
        self.root.next = Node(snake_body_horizontal, 270, 300)
        self.root.next.next = Node(snake_body_horizontal, 300, 300)
        self.root.next.next.next = Node(head_right, 330, 300)

        self.score = 0
        self.num_hearts = 3
    def size(self):
        count = 0
        temp = self.root
        while temp != 0:
            temp = temp.next
            count += 1
        return count
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

        return newData

    def newNode(self, newData):
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

    def print(self, screen, height):
        self.printBody(screen)
        self.printHearts(screen, height)
        self.printScore(screen, height)
    def printHearts(self, screen, height):
        num = 30
        for i in range(self.num_hearts):
            screen.blit(heart, (20 + num, height + 10))
            num += 35
    def printScore(self, screen, height):
        screen.blit(pygame.font.SysFont('Comic Sans MS', 30).render('your score is : ' + str(self.score), False,
                                                                         (255, 255, 255)), (180, height))
    def printBody(self, screen):
        temp = self.root
        while temp != 0:
            temp.printData(screen)
            temp = temp.next

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
        if k == self.upKey and self.dir < 3:
            self.pniya = self.dir
            self.dir = 3
        elif k == self.downKey and self.dir < 3:
            self.pniya = self.dir
            self.dir = 4
        elif k == self.rightKey and self.dir > 2:
            self.pniya = self.dir
            self.dir = 1
        elif k == self.leftKey and self.dir > 2:
            self.pniya = self.dir
            self.dir = 2

    def isLocationInvalid(self):
        temp = self.root
        while temp != 0:
            if temp.loc_x == self.loc_x and temp.loc_y == self.loc_y:
                return True
            temp = temp.next
        return self.loc_x < 0 or self.loc_x >= 600 or self.loc_y < 0 or self.loc_y >= 600

    def isAlive(self):
        return self.num_hearts > 0

    def ate(self, x, y):
        return self.loc_x == x and self.loc_y == y