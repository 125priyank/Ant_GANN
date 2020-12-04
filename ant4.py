import numpy as np
import random
import pygame
from Ant import *
from GA import *

gui = False
if gui:
    FPS = 20
    WHITE = (200, 200, 200)
    pygame.display.set_caption("Ant Game")
    clock = pygame.time.Clock()
    ANT_IMAGE = pygame.image.load('car.png')
    ANT_IMAGE = pygame.transform.scale(ANT_IMAGE, (TILE_SIZE+10, TILE_SIZE-5))
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
GEN_NUM = 0
def main(neuralNetwork):
    ##########
    global GEN_NUM, food_storage
    food_storage = []
    for i in range(100):
        food_storage.append((random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)))
    ants = {}
    GEN_NUM += 1
    # nets = []
    # ge = []
    ge = {}
    nets = {}
    ant_id = 0
    for net in neuralNetwork:
        nets[ant_id] = net
        ants[ant_id] = Ant(10, 10)
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
        if len(ants) == 0:
            QUIT = True


        if gui:
            WIN.fill((255, 255, 255))
            for ant_id, ant in ants.items():
                ant.draw(WIN, ANT_IMAGE)
                # ant.move(np.random.rand(5))
            pygame.display.update()

    return ge 
        

# np.random.seed(1999)
x = np.random.rand(20, 1)
y = np.random.rand(4, 1)
bestPop = GA(x, y, n_h=[20, 12], generations=2, popSize=1, eliteSize=0, main=main, mutationRate=0.05)

