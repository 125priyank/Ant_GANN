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
possible_directions = {'u': 0, 'd': 1, 'l': 2, 'r': 3, 'ur': 4, 'ul': 5, 'dr': 6, 'dl': 7, 0: 'u', 1: 'd', 2: 'l', 3: 'r', 4:'ur', 5: 'ul', 6: 'dr', 7: 'dl'}
moves = {
  'u': (0, 1),
  'd': (0, -1),
  'l': (-1, 0),
  'r': (1, 0),
  'ur': (1, 1),
  'ul': (-1, 1),
  'dr': (1, -1),
  'dl': (-1, -1)
}
prevDirectionMap = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l', 'ur': 'dl', 'ul': 'dr', 'dl': 'ur', 'dr': 'ul'}

class Ant:
    def __init__  (self, x, y):
        self.x = x
        self.y = y  
        self.foods = set() # generate food
        self.grid = []
        self.num_moves = 0
        self.allowed_moves = 100
        self.num_food = 0
        self.direction = possible_directions[random.randrange(0, 8)]
        self.prev_min = 40
        for i in range(GRID_HEIGHT):
            tmp = []
            for j in range(GRID_WIDTH):
                tmp.append(Tile(i, j))
            self.grid.append(tmp)
                
        for i in range(1):
            self.addFood()

        self.ant_locations = [[x, y, self.direction]]
        self.food_locations = [[next(iter(self.foods)).x, next(iter(self.foods)).y]]
        
    def canEat(self, x,y):
        if self.grid[x][y].food != None:
            self.eat(x, y)
            return True
        return False
        
    def eat(self, x, y):
        self.foods.remove(self.grid[x][y].food)
        self.grid[x][y].food = None
        self.addFood()
        
    def addFood(self):
        # tmp = self.food_storage.pop()
        tmp = (random.randrange(1, GRID_HEIGHT-1), random.randrange(1, GRID_WIDTH-1))
        food = Food(tmp[0], tmp[1])
        self.foods.add(food)
        self.grid[food.x][food.y].food = food
        
    def isBackMove(self, prev_direction):
        return prevDirectionMap[prev_direction] == self.direction
        
    def move(self, output):
        # move - (u - 0)
        self.num_moves += 1
        if self.num_moves > 1e5:
            return 0, False
        indx = np.argmax(output)
        prev_direction = self.direction
        self.direction = possible_directions[indx]
        self.x += moves[self.direction][0]
        self.y += moves[self.direction][1]
        cur_x = self.x
        cur_y = self.y
        self.ant_locations.append([cur_x, cur_y, self.direction])
        self.food_locations.append([next(iter(self.foods)).x, next(iter(self.foods)).y])
        if self.isOut(cur_x, cur_y) :
            return -500, False
        else:
            performance = 1
            tmp = next(iter(self.foods))
            cur_min = self.manhattanDistance(self.x, self.y, tmp.x, tmp.y)
            performance += 10*(self.prev_min - cur_min)
            self.prev_min = min(self.prev_min, cur_min)
            if self.canEat(cur_x, cur_y):
                self.num_food += 1
                performance += 1000
                self.allowed_moves += 50
                self.prev_min = 40
        return performance, True
        
    def manhattanDistance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    
    def validatePoint(self, x, y):
        return x < GRID_WIDTH and x >= 0 and y < GRID_HEIGHT and y >= 0
    
    def createVision(self):
        vision = np.zeros(shape=(24, 1))
        vision[possible_directions[self.direction]+16, 0] = 1
        # fnd = False
        for indx in range(8):
          x, y = self.x, self.y
          found_food = False
          while self.validatePoint(x, y):
              if found_food == False and self.grid[x][y].food != None:
                  # fnd = True
                  found_food = True
                  vision[2*indx] = 1.0
              x+=slopes[indx][0]
              y+=slopes[indx][1]
          vision[2*indx+1] = 1.0/self.manhattanDistance(x, y, self.x, self.y)
        # if fnd:
        #   print(vision)
        return vision

        # function for slope calculation
        # y2-y1+1 / x2 - x1 + 1
        
    def draw(self, WIN, ANT_IMAGE):
        ant_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        ant_image.fill((0, 0, 0))
        # ant_image = pygame.transform.rotate(ANT_IMAGE, (self.orientation+90))
        WIN.blit(ant_image, (self.x*TILE_SIZE, self.y*TILE_SIZE))
        
        for food in self.foods:
            food.draw(WIN)
    
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

class Tile:
    def __init__(self, x, y, ant = None, food = None):
        self.x = x
        self.y = y
        self.food = food
        self.ant = ant

# a = Ant(10, 10)
# t = a.grid
# for i in a.foods:
#   a.x = i.x +1
#   a.y = i.y
#   print(i.x, i.y)
# for i in t:
#   for j in i:
#     if j.food != None:
#       print(j.x, j.y)
# a.createVision()