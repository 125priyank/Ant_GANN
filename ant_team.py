import random
import copy
import numpy as np
import pygame

TILE_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WIN_WIDTH = TILE_SIZE*GRID_WIDTH
WIN_HEIGHT = TILE_SIZE*GRID_HEIGHT
FOOD_ID = 0

slopes = [
  (-1, 0),(-1, 1),(0, 1),(1, 1),(1, 0),(1, -1),(0, -1),(-1, -1)
]
possible_directions = {'u': 0, 'd': 1, 'l': 2, 'r': 3, 0: 'u', 1: 'd', 2: 'l', 3: 'r', 'n' : 4, 4: 'n'}
moves = {
  'u': (0, 1),
  'd': (0, -1),
  'l': (-1, 0),
  'r': (1, 0),
  'n': (0, 0)
}


class AntTeam:
    def __init__  (self, x, y, antId, foods, grid):
        self.x = x
        self.y = y  
        self.antId = antId
        # self.foods = set() # generate food
        self.grid = []
        self.num_moves = 0
        self.allowed_moves = 100
        self.num_food = 0
        self.direction = possible_directions[random.randrange(0, 4)]
        self.prev_min = 40
        self.foods = foods
        self.grid = grid
        self.performance = 0

    def canEat(self, x,y):
        if self.grid[x][y].food != None:
            return True
        return False
        
    def isBackMove(self, prev_direction):
        if prev_direction=='u':
          return self.direction == 'd'
        elif prev_direction=='d':
          return self.direction == 'u'
        elif prev_direction=='l':
          return self.direction == 'r'
        elif prev_direction=='r':
          return self.direction == 'l'
        
    def move(self, output):
        '''
        returns is In grid(bool), canEatfood(bool)
        '''
        # move - (u - 0)
        self.num_moves += 1
        self.grid[self.x][self.y].ant[self.antId] = False
        indx = np.argmax(output)
        prev_direction = self.direction
        self.direction = possible_directions[indx]
        self.x += moves[self.direction][0]
        self.y += moves[self.direction][1]
        cur_x = self.x
        cur_y = self.y
        if self.isOut(cur_x, cur_y) or self.isBackMove(prev_direction):
            self.performance -= 500
            return False, False
        else:
            self.grid[cur_x][cur_y].ant[self.antId] = True
            self.performance += 1
            tmp = next(iter(self.foods))
            cur_min = self.manhattanDistance(self.x, self.y, tmp.x, tmp.y)
            self.performance += 10*(self.prev_min - cur_min)
            self.prev_min = min(self.prev_min, cur_min)
            if self.canEat(cur_x, cur_y):
                # self.num_food += 1
                # self.allowed_moves += 50
                # self.prev_min = 40
                return True, True
        return True, False
        
    def manhattanDistance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    
    def validatePoint(self, x, y):
        return x < GRID_WIDTH and x >= 0 and y < GRID_HEIGHT and y >= 0
    
    def createVision(self):
        vision = np.zeros(shape=(31, 1))
        vision[possible_directions[self.direction]+26, 0] = 1
        # fnd = False
        if self.grid[self.x][self.y].ant[friendList[self.antId]] == True:
            vision[24] = 1.0
        if self.grid[self.x][self.y].food != None:
            vision[25] = 1.0
        for indx in range(8):
            x, y = self.x, self.y
            found_food = False
            found_friend = False
            # found_enemy = False
            while self.validatePoint(x, y):
                if found_food == False and self.grid[x][y].food != None:
                    found_food = True
                    vision[3*indx] = 1.0
                if found_friend == False and self.grid[x][y].ant[friendList[self.antId]] == True:
                    found_friend = True
                    vision[3*indx+1] = 1.0/(self.manhattanDistance(self.x, self.y, x, y)+1)
                # if found_enemy == False:
                #     for enemy in enemyList[self.antId]:
                #         if self.grid[x][y].ant[enemy] == True:
                #             found_enemy = True
                #             vision[4*indx+2] = 1.0
                #             break
            
                x+=slopes[indx][0]
                y+=slopes[indx][1]
            vision[3*indx+2] = 1.0/(self.manhattanDistance(x, y, self.x, self.y)+1)
        # if fnd:
        #   print(vision)
        return vision
        
    def draw(self, WIN, ANT_IMAGE):
        ant_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        ant_image.fill((0, 0, 0))
        # ant_image = pygame.transform.rotate(ANT_IMAGE, (self.orientation+90))
        WIN.blit(ant_image, (self.x*TILE_SIZE, self.y*TILE_SIZE))
        
        # for food in self.foods:
        #     food.draw(WIN)
    
    def isOut(self, x, y):
        # global GRID_WIDTH, GRID_HEIGHT
        return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, WIN):
        food = pygame.Surface((TILE_SIZE, TILE_SIZE))
        food.fill((255, 0, 0))
        WIN.blit(food, (self.x*TILE_SIZE, self.y*TILE_SIZE))
        
class Grid:
    def __init__(self):
        self.grid = np.zeros((GRID_WIDTH, GRID_HEIGHT))

friendList = {
    'ant1_1': 'ant1_2',
    'ant1_2': 'ant1_1',
    'ant2_1': 'ant2_2',
    'ant2_2': 'ant2_1',
}

enemyList = {
    'ant1_1': ['ant2_1', 'ant2_2'],
    'ant1_2': ['ant2_1', 'ant2_2'],
    'ant2_1': ['ant1_1', 'ant1_2'],
    'ant2_2': ['ant1_1', 'ant1_2'],
}

class Tile:
    def __init__(self, x, y, food = None):
        self.x = x
        self.y = y
        self.food = food
        self.ant = {
            'ant1_1': False,
            'ant1_2': False,
            'ant2_1': False,
            'ant2_2': False,
        }

class Environment:
    def __init__(self, neuralNetwork):
        self.grid = []
        self.neuralNetwork = neuralNetwork
        for i in range(GRID_HEIGHT):
            tmp = []
            for j in range(GRID_WIDTH):
                tmp.append(Tile(i, j))
            self.grid.append(tmp)
        self.foods = []
        self.addFood()
        self.fitness = 0
        self.days_alive = 0
        self.ant = {}
        self.ant[0] = AntTeam(x=random.randrange(0, GRID_WIDTH), y=random.randrange(0, GRID_HEIGHT),antId='ant1_1', foods=self.foods, grid=self.grid)
        self.ant[1] = AntTeam(x=random.randrange(0, GRID_WIDTH), y=random.randrange(0, GRID_HEIGHT),antId='ant1_2', foods=self.foods, grid=self.grid)

    def sameLocation(self, antId1, antId2):
        if antId1 not in self.ant or antId2 not in self.ant:
            return False
        return self.ant[antId1].x==self.ant[antId2].x and self.ant[antId1].y==self.ant[antId2].y

    # def teamEat(self):
    #     kill_profit = 1e3
        

    def move(self):
        remAnt = set()
        contestForFood = []
        self.days_alive += 1
        if self.days_alive > 1000:
            print("Problem here")
            return False

        for antId, ant in self.ant.items():
            isIn, canEat = ant.move(self.neuralNetwork[antId].forward_propagation(ant.createVision().reshape(-1, 1)))
            if isIn == False:
                remAnt.add(antId)
            elif canEat == True:
                contestForFood.append(ant)


        if len(contestForFood) > 1:
            self.fitness += 1e4
            for antId, ant in self.ant.items():
                ant.num_food += 1
                ant.allowed_moves += 50
                ant.prev_min = 40
            self.eat()

        for antId, ant in self.ant.items():
            if ant.num_moves > ant.allowed_moves:
                remAnt.add(antId)

        if len(remAnt) > 0:
            for antId, ant in self.ant.items():
                self.fitness += ant.performance
            return False
        return True


    def eat(self):
        self.grid[self.foods[0].x][self.foods[0].y].food = None
        self.foods.pop()
        self.addFood()

    def addFood(self):
        tmp = (random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH))
        food = Food(tmp[0], tmp[1])
        self.foods.append(food)
        self.grid[food.x][food.y].food = food

    def draw(self, WIN, ANT_IMAGE):
        for food in self.foods:
            food.draw(WIN)
        for antId, ant in self.ant.items():
            ant.draw(WIN, ANT_IMAGE)


# addFood(grid, foods)
# from NerualNetwork import *
# for i in range(100):
#     nn = []
#     x = np.random.rand(36, 1)
#     y = np.random.rand(4, 1)
#     for i in range(4):
#         nn.append(NeuralNetwork(x, y, [20, 12]))
#     a = Environment(nn)
#     for i in range(100):
#         f = a.move()
#         if not f:
#             print(a.fitness)
#             break
