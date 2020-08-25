import pygame
import sys
import random
pygame.init()

size = (25*25, 25*25)

#colors
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

BLOCK_SIZE = 25
dx, dy = 0, -BLOCK_SIZE


x = 25#random.randrange(0, size[0], BLOCK_SIZE)
y = 150#random.randrange(0, size[1], BLOCK_SIZE)

apple_x = 0 #random.randrange(0, size[0], BLOCK_SIZE)
apple_y = 300 #random.randrange(0, size[1], BLOCK_SIZE)
# TO DO apple != x y

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

snake = [(x, y), (x - BLOCK_SIZE, y)]

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    snake = [(i + dx, j + dy) for i, j in snake]
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        dx = BLOCK_SIZE
        dy = 0
    if keys[pygame.K_a]:
        dx = -BLOCK_SIZE
        dy = 0
    if keys[pygame.K_s]:
        dy = BLOCK_SIZE
        dx = 0
    if keys[pygame.K_w]:
        dy = -BLOCK_SIZE
        dx = 0

    for i in range(len(snake)):
        if snake[i][0] > size[0]:
            snake[i] = (0, snake[i][1])
        if snake[i][0] < 0:
            snake[i] = (size[0], snake[i][1])

        if snake[i][1] > size[1]:
            snake[i] = (snake[i][0], 0)
        if snake[i][1] < 0:
            snake[i] = (snake[i][0], size[1])

    if snake[-1][0] == apple_x and snake[-1][1] == apple_y:
        if dx>0 or dy>0:
          snake.append((snake[-1][0] + dx, snake[-1][1] + dy))
        else:
          snake.append((snake[-1][0] - dx, snake[-1][1] - dy))
        
        print(snake, apple_x, apple_y, dx)
        #apple_x = random.randrange(0, size[0], BLOCK_SIZE)
        #apple_y = random.randrange(0, size[1], BLOCK_SIZE)
        apple_y += 25

    screen.fill((180, 0, 180))

    [pygame.draw.rect(screen, BLACK, (i, j, BLOCK_SIZE, BLOCK_SIZE)) for i, j in snake]
    pygame.draw.rect(screen, WHITE, (snake[-1][0], snake[-1][1], BLOCK_SIZE, BLOCK_SIZE)) 
    pygame.draw.rect(screen, GREEN, (apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE))


    #print(snake)
    clock.tick(1)

    pygame.display.flip()