import numpy as np
import random
import pygame
import json
from Ant import *
from GA import *
# from save import *


# !zip -r /content/w.zip /content/weights
gui = True
if gui:
    FPS = 10
    WHITE = (200, 200, 200)
    pygame.display.set_caption("Ant Game")
    clock = pygame.time.Clock()
    ANT_IMAGE = pygame.image.load('car.png')
    # ANT_IMAGE = pygame.transform.scale(ANT_IMAGE, (TILE_SIZE+10, TILE_SIZE-5))
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
GEN_NUM = 0
# fp_fitness = open('bestFitness.txt', 'w')
# fp_food = open('bestFood.txt', 'w')
# save = Save()
def main(neuralNetwork):
    ##########
    global GEN_NUM, fp_fitness, fp_food
    ants = {}
    
    # nets = []
    # ge = []
    best_fitness = -1e6
    bestAnt = Ant(0, 0)

    ge = {}
    nets = {}
    ant_id = 0
    for net in neuralNetwork:
        nets[ant_id] = net
        ants[ant_id] = Ant(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
        ge[ant_id] = 0
        ant_id += 1
    ##########
    QUIT = False
    while QUIT == False:
        if gui:
            clock.tick(FPS)
        rem_ants = set()
        for ant_id, ant in ants.items():
            brainInput = ant.createVision()
            brainInput = brainInput.reshape(brainInput.shape[0], 1)
            brainOutput = nets[ant_id].forward_propagation(brainInput)
            performance, isIn = ant.move(brainOutput)
            if isIn ==False:
                rem_ants.add(ant_id)
                ge[ant_id] += performance
            else:
                ge[ant_id] += performance
            if ant.num_moves > ant.allowed_moves:
                rem_ants.add(ant_id)
        if gui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QUIT = True
                    pygame.quit()
                    quit()
        
        for ant_id in rem_ants:
            if best_fitness < ge[ant_id]:
                best_fitness = ge[ant_id]
                bestAnt = ants[ant_id]
            ants.pop(ant_id)
        if len(ants) == 0:
            QUIT = True


        if gui:
            WIN.fill((255, 255, 255))
            for ant_id, ant in ants.items():
                ant.draw(WIN, ANT_IMAGE)
                # ant.move(np.random.rand(5))
            pygame.display.update()
    # fp_fitness.write('{}\n'.format(best_fitness))
    # fp_food.write('{}\n'.format(bestAnt.num_food))
    # if GEN_NUM%10 == 0:
    #     if not os.path.exists('save'):
    #       os.makedirs('save')
    #     saveDict = {'ant' : bestAnt.ant_locations, 'food' : bestAnt.food_locations}
    #     # save.generationBest[GEN_NUM] = saveDict
    #     with open('save/save{}.json'.format(GEN_NUM), 'w') as fp:
    #         json.dump(saveDict, fp)
    GEN_NUM += 1
    return ge 
        

# np.random.seed(1999)
x = np.random.rand(24, 1)
y = np.random.rand(8, 1)
bestPop = GA(x, y, n_h=[20, 12], generations=100, popSize=100, eliteSize=10, main=main, mutationRate=0.5)
# with open('weights/weights0.pickle', 'rb') as f:
#     x = pickle.load(f)
#     tmp = []
#     tmp.append(x)
#     print(main(tmp))
# with open('save.json', 'w') as fp:
#     json.dump(save.generationBest, fp)
# print(len(save.generationBest))

# Fitness for every generation
# Every %10 generation - coordinates of ant and food.
# Number of food eaten per generation.


