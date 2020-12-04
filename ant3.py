import pygame
import os
import time
import random
import numpy as np
import neat
import copy
pygame.font.init()

TILE_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WIN_WIDTH = TILE_SIZE*GRID_WIDTH
WIN_HEIGHT = TILE_SIZE*GRID_HEIGHT
FOOD_ID = 0

FPS = 200
moves = {
    0 : [
    #   {'x': 0, 'y': 0, 'direction' :90},
    #   {'x': 0, 'y': 0, 'direction' :-90},
      {'x': -1, 'y': 0, 'direction' : 90},
      {'x': 0, 'y': -1, 'direction' :0},
      {'x': 1, 'y': 0, 'direction' :-90}
    ],
    90 : [
    #   {'x': 0, 'y': 0, 'direction' :90},
    #   {'x': 0, 'y': 0, 'direction' :-90},
      {'x': 0, 'y': 1, 'direction' : 90},
      {'x': -1, 'y': 0, 'direction' :0},
      {'x': 0, 'y': -1, 'direction' :-90}
    ],
    180 : [
    #   {'x': 0, 'y': 0, 'direction' :90},
    #   {'x': 0, 'y': 0, 'direction' :-90},
      {'x': 1, 'y': 0, 'direction' : 90},
      {'x': 0, 'y': 1, 'direction' :0},
      {'x': -1, 'y': 0, 'direction' :-90}
    ],
    270 : [
    #   {'x': 0, 'y': 0, 'direction' :90},
    #   {'x': 0, 'y': 0, 'direction' :-90},
      {'x': 0, 'y': -1, 'direction' : 90},
      {'x': 1, 'y': 0, 'direction' :0},
      {'x': 0, 'y': +1, 'direction' :-90}
    ]
  }

food_storage = []
for i in range(100):
    food_storage.append((random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)))
class Ant:
    def __init__  (self, x, y):
        self.x = x
        self.y = y  
        self.orientation = 0
        self.foods = set() # generate food
        self.grid = []
        self.prev_min_dist = 7
        self.prev_avg_dist = 7
        self.num_moves = 0
        self.allowed_moves = 100
        self.food_storage = copy.deepcopy(food_storage)
        self.prev_loc = {}
        for i in range(GRID_HEIGHT):
            tmp = []
            for j in range(GRID_WIDTH):
                tmp.append(Tile(i, j))
            self.grid.append(tmp)
                
        for i in range(10):
            self.addFood()
        
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
        # food = Food(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
        # while self.grid[food.x][food.y].food != None and self.grid[food.x][food.y].ant != None:
        #     food = Food(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
        tmp = self.food_storage.pop()
        # print(tmp[0], tmp[1])
        food = Food(tmp[0], tmp[1])
        self.foods.add(food)
        self.grid[food.x][food.y].food = food
        
    def move(self, output, current_vision):
        # 0-1 angle
        # 2-5 move
        self.num_moves += 1
        indx = np.argmax(output)
        # print((self.x, self.y))
        self.x += moves[self.orientation][indx]['x']
        self.y += moves[self.orientation][indx]['y']
        if (self.x, self.y) in self.prev_loc:
          self.prev_loc[(self.x, self.y)] += 1
        else:
            self.prev_loc[(self.x, self.y)] = 1;
        
        cur_x, cur_y = self.x, self.y
        self.orientation += moves[self.orientation][indx]['direction']
        self.orientation = (self.orientation + 360)%360
        performance = -(self.prev_loc[(self.x, self.y)]-1)*0.1
        if self.isOut(cur_x, cur_y):
            return -1, False
        else:
            tmpPerformance = self.perfomanceCalc(current_vision)
            if self.canEat(cur_x, cur_y):
                self.prev_loc.clear()
                performance += 1
                self.allowed_moves += 40
            else:
                performance += tmpPerformance
        return performance, True
    
    def perfomanceCalc(self, current_vision):
        cur_min_dist = 7
        cur_avg_dist = 0
        num_foods = 0
        for i in range(len(current_vision)//2):
            food = current_vision[2*i]
            wall = current_vision[2*i+1]
            if food:
                v_dist = i//5 + 1
                h_dist = abs(2 - i%5)
                cur_min_dist = min(cur_min_dist, v_dist+ h_dist)
                num_foods += 1
                cur_avg_dist += v_dist + h_dist
        if num_foods == 0:
            cur_avg_dist = 7
        else:
            cur_avg_dist /= num_foods
        performance =  0.100*(self.prev_min_dist - cur_min_dist)  #+ 0.100 * (self.prev_avg_dist - cur_avg_dist)
        self.prev_min_dist = cur_min_dist
        self.prev_avg_dist = cur_avg_dist
        return performance
        
        
    def manhattanDistance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    
    def validatePoint(self, x, y):
        return x < GRID_WIDTH and x >= 0 and y < GRID_HEIGHT and y >= 0
    
    def createVision(self):
        vision = list()
        if self.orientation == 0:
            # upside viewing
          for y in range(self.y-1, self.y-11, -1):
            for x in range(self.x-5, self.x + 6):
              valid = self.validatePoint(x, y)
                    # tmp - [x, y, Food, Wall]
              tmp = list()
              if valid:
                if self.grid[x][y].food != None:
                  tmp.append(1)
                else:
                  tmp.append(0)
                tmp.append(0)
              else:
                tmp.append(0)
                tmp.append(1)
              vision = np.append(vision, tmp)  
        elif self.orientation == 90:
          # leftside viewing
          for x in range(self.x-1, self.x-11, -1):
            for y in range(self.y+5, self.y-6, -1):
              valid = self.validatePoint(x, y)
                    # tmp - [x, y, Food, Wall]
              tmp = list()
              if valid:
                if self.grid[x][y].food != None:
                  tmp.append(1)
                else:
                  tmp.append(0)
                tmp.append(0)
              else:
                tmp.append(0)
                tmp.append(1)
              vision = np.append(vision, tmp)  
        elif self.orientation == 180:
          # downside viewing
          for y in range(self.y+1, self.y+11):
            for x in range(self.x+5, self.x-6, -1):
              valid = self.validatePoint(x, y)
                    # tmp - [x, y, Food, Wall]
              tmp = list()
              if valid:
                if self.grid[x][y].food != None:
                  tmp.append(1)
                else:
                  tmp.append(0)
                tmp.append(0)
              else:
                tmp.append(0)
                tmp.append(1)
              vision = np.append(vision, tmp)   
        elif self.orientation == 270:
          # rightside viewing
          for x in range(self.x+1, self.x+11):
            for y in range(self.y-5, self.y+6):
              valid = self.validatePoint(x, y)
                    # tmp - [x, y, Food, Wall]
              tmp = list()
              if valid:
                if self.grid[x][y].food != None:
                  tmp.append(1)
                else:
                  tmp.append(0)
                tmp.append(0)
              else:
                tmp.append(0)
                tmp.append(1)
              vision = np.append(vision, tmp)
        return vision
        
    
    def draw(self, WIN, ANT_IMAGE):
        # ant = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # ant.fill((0, 0, 0))
        ant_image = pygame.transform.rotate(ANT_IMAGE, (self.orientation+90))
        WIN.blit(ant_image, (self.x*TILE_SIZE, self.y*TILE_SIZE))
        
        for food in self.foods:
            food.draw(WIN)
    
    def isOut(self, x, y):
        # global GRID_WIDTH, GRID_HEIGHT
        return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT
  
class Food:
    def __init__(self, x, y):
        global FOOD_ID
        self.x = x
        self.y = y
        self.id = FOOD_ID
        FOOD_ID+=1
    
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

WHITE = (200, 200, 200)
pygame.display.set_caption("Ant Game")
clock = pygame.time.Clock()
ANT_IMAGE = pygame.image.load('car.png')
ANT_IMAGE = pygame.transform.scale(ANT_IMAGE, (TILE_SIZE+10, TILE_SIZE-5))
GEN_NUM = 0
def main(genomes, config):
    ##########
    global GEN_NUM, food_storage
    food_storage = []
    for i in range(100):
        food_storage.append((random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)))
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    ants = {}
    GEN_NUM += 1
    # nets = []
    # ge = []
    ge = {}
    nets = {}
    ant_id = 0
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets[ant_id] = net
        ants[ant_id] = Ant(10, 10)
        g.fitness = 0
        ge[ant_id] = g
        ant_id += 1
    ##########
    QUIT = False
    # for i in range(10):
    #     ants.add(Ant(random.randrange(5, 15), random.randrange(5, 15)))
    while QUIT == False:
        clock.tick(FPS)
        rem_ants = set()
        for ant_id, ant in ants.items():
            brainInput = ant.createVision()
            brainOutput = nets[ant_id].activate(tuple(brainInput))
            performance, isIn = ant.move(brainOutput, brainInput)
            if isIn ==False:
                performance -= 10
                rem_ants.add(ant_id)
                ge[ant_id].fitness += performance
            else:
                ge[ant_id].fitness += performance
            if ant.num_moves > ant.allowed_moves:
                rem_ants.add(ant_id)
        
        for event in pygame.event.get():
            output = np.zeros(5)
            if event.type == pygame.QUIT:
                QUIT = True
                pygame.quit()
                quit()
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         output[2] = 1
            #     elif event.key == pygame.K_UP:
            #         output[3] = 1
            #     elif event.key == pygame.K_RIGHT:
            #         output[4] = 1
            #     elif event.key == pygame.K_DOWN:
            #         output[0] = 1
            #     for ant in ants:
            #         valid = ant.move(output)
            #         if not valid:
            #             rem_ants.add(ant)
            
        
        for ant_id in rem_ants:
            ants.pop(ant_id)
            nets.pop(ant_id)
            ge.pop(ant_id)
        if len(ants) == 0:
            QUIT = True



            
        WIN.fill((255, 255, 255))
        # for x in range(WIN_WIDTH):
        #     for y in range(WIN_HEIGHT):
        #         rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE,
        #                        TILE_SIZE, TILE_SIZE)
        #         pygame.draw.rect(WIN, WHITE, rect, 1)
        for ant_id, ant in ants.items():
            ant.draw(WIN, ANT_IMAGE)
            # ant.move(np.random.rand(5))
        pygame.display.update()
        
        
        
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 100)
    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
        
        
        
