import pygame
import numpy as np
import random
from ant_team import *
from GA_team import *


# !zip -r /content/w.zip /content/weights
gui = False
if gui:
    FPS = 5
    WHITE = (200, 200, 200)
    pygame.display.set_caption("Ant Game")
    clock = pygame.time.Clock()
    ANT_IMAGE = pygame.image.load('car.png')
    ANT_IMAGE = pygame.transform.scale(ANT_IMAGE, (TILE_SIZE+10, TILE_SIZE-5))
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
def main(neuralNetwork):
    ##########
    ants = {}
    # nets = []
    # ge = []
    ge = {}
    # nets = {}
    ant_id = 0
    for net in neuralNetwork:
        # nets[ant_id] = net
        ants[ant_id] = Environment(net)
        ge[ant_id] = 0
        ant_id += 1
    ##########
    QUIT = False
    while QUIT == False:
        if gui:
            clock.tick(FPS)
        rem_ants = set()
        for ant_id, ant in ants.items():
            isIn = ant.move()
            if isIn ==False:
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
            ge[ant_id] = ants[ant_id].fitness
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
x = np.random.rand(31, 1)
y = np.random.rand(5, 1)
# nn = []
# for i in range(4):
#     nn.append(NeuralNetwork(x, y, [20, 12]))
# print(main([nn]))
# bestPop = GA(x, y, n_h=[20, 12], generations=200, popSize=100, eliteSize=10, main=main, mutationRate=0.5)
# with open('weights_team.pickle', 'rb') as f:
#     x = pickle.load(f)
#     tmp = []
#     for i in range(1000):
#         tmp.append(x)
#     x = main(tmp)
#     print(sorted(x.items(), key = operator.itemgetter(1), reverse = True)[:100])

