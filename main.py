import pygame
import sys
import random
pygame.init()

size = (25*25, 25*25)

def spam_apple(snake):
  a = random.randrange(0, size[0]-BLOCK_SIZE, BLOCK_SIZE)
  b = random.randrange(0, size[1]-BLOCK_SIZE, BLOCK_SIZE)
  if (a, b) in snake:
    spam_apple(snake)
  return (a, b)

#colors
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

BLOCK_SIZE = 25
dx, dy = 0, 0

x = random.randrange(BLOCK_SIZE, size[0], BLOCK_SIZE)
y = random.randrange(BLOCK_SIZE, size[1], BLOCK_SIZE)
snake = [(x, y)]
snakesize = len(snake)

apple_x, apple_y = spam_apple(snake)

spam_apple(snake)
# TO DO apple != x y

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    snake = [(i, j) for i, j in snake]    

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
    print(dx, dy, x, y)
    
    x += dx
    y += dy   
    snake.append((x,y))
    snake = snake[-snakesize:]

    for i in range(len(snake)):
        if snake[i][0] > size[0] - BLOCK_SIZE:
          print("LOOOOOOOOOOW")
          snake[i] = (0, snake[i][1])
          x = BLOCK_SIZE

        if snake[i][0] < 0:
          print("HIIIIIIIIIIIIIII")
          snake[i] = (size[0] - BLOCK_SIZE, snake[i][1])
          x = size[0] - BLOCK_SIZE

        if snake[i][1] > size[1] - BLOCK_SIZE:
          print("HIIIIIIIIIIIIIII")
          snake[i] = (snake[i][0], 0)
          y = BLOCK_SIZE

        if snake[i][1] < 0:
          print("LOOOOOOOOOOW")
          snake[i] = (snake[i][0], size[1]- BLOCK_SIZE)
          y = size[1] - BLOCK_SIZE

    if snake[-1][0] == apple_x and snake[-1][1] == apple_y:
        snakesize+=1
        apple_x, apple_y = spam_apple(snake)

    screen.fill((0, 0, 180))

    [pygame.draw.rect(screen, BLACK, (i, j, BLOCK_SIZE, BLOCK_SIZE)) for i, j in snake]
    pygame.draw.rect(screen, WHITE, (snake[-1][0], snake[-1][1], BLOCK_SIZE, BLOCK_SIZE)) 
    pygame.draw.rect(screen, GREEN, (apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE))

    print(snake)
    clock.tick(10)
    pygame.display.flip()