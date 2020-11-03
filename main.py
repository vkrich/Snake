import pygame
import sys
import random
import sqlite3

class Background(pygame.sprite.Sprite):
  def __init__(self, image_file, location):
      pygame.sprite.Sprite.__init__(self) 
      self.image = pygame.image.load(image_file)
      self.rect = self.image.get_rect()
      self.rect.left, self.rect.top = location

def table_creation():
  conn = sqlite3.connect("Snake.db") 
  # или :memory: чтобы сохранить в RAM
  cursor = conn.cursor()
  
  # Создание таблицы в БД для хранения очков пользователя
  cursor.execute("""CREATE TABLE players (
                  player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  player_name text NOT NULL,
                  scores INTEGER 
                );
                """)
  conn.commit()              

pygame.init()

#colors
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

BLOCK_SIZE = 25
size = (BLOCK_SIZE*BLOCK_SIZE, BLOCK_SIZE*BLOCK_SIZE)

def spam_apple(snake):
  a = random.randrange(0, size[0]-BLOCK_SIZE, BLOCK_SIZE)
  b = random.randrange(0, size[1]-BLOCK_SIZE, BLOCK_SIZE)
  if (a, b) in snake:
    a, b = spam_apple(snake)
  return (a, b)


x = random.randrange(BLOCK_SIZE, size[0]-BLOCK_SIZE*2, BLOCK_SIZE)
y = random.randrange(BLOCK_SIZE, size[1]-BLOCK_SIZE*2, BLOCK_SIZE)
snake = [(x, y)]
snakesize = len(snake)
apple_x, apple_y = spam_apple(snake)
screen = pygame.display.set_mode(size)
scores_text = pygame.font.SysFont('serif', 36)
scores_points = 0

clock = pygame.time.Clock()
direction_moving = {'W': True, 'A': True, 'S': True, 'D': True}
dx, dy = 0, 0
while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    BackGround = Background('grass.png', [0,0])
    screen.blit(BackGround.image, BackGround.rect)

    #snake = [(i, j) for i, j in snake]    
    
    if keys[pygame.K_d] and direction_moving['D']:
      direction_moving = {'W': True, 'A': False, 'S': True, 'D': True}
      dx = BLOCK_SIZE
      dy = 0
    if keys[pygame.K_a] and direction_moving['A']:
      direction_moving = {'W': True, 'A': True, 'S': True, 'D': False}
      dx = -BLOCK_SIZE
      dy = 0
    if keys[pygame.K_s] and direction_moving['S']:
      direction_moving = {'W': False, 'A': True, 'S': True, 'D': True}
      dy = BLOCK_SIZE
      dx = 0
    if keys[pygame.K_w] and direction_moving['W']:
      direction_moving = {'W': True, 'A': True, 'S': False, 'D': True}
      dy = -BLOCK_SIZE
      dx = 0    
    
    #add new block in snake
    x += dx
    y += dy    
    snake.append((x, y))
    #delete last block in snake
    snake = snake[-snakesize:]

    for i in range(len(snake)):
        if snake[i][0] > size[0] - BLOCK_SIZE:          
          snake[i] = (0, snake[i][1])
          x = BLOCK_SIZE

        if snake[i][0] < 0:          
          snake[i] = (size[0] - BLOCK_SIZE, snake[i][1])
          x = size[0] - BLOCK_SIZE

        if snake[i][1] > size[1] - BLOCK_SIZE:          
          snake[i] = (snake[i][0], 0)
          y = BLOCK_SIZE

        if snake[i][1] < 0:          
          snake[i] = (snake[i][0], size[1]- BLOCK_SIZE)
          y = size[1] - BLOCK_SIZE

    if snake[-1][0] == apple_x and snake[-1][1] == apple_y:
        snakesize+=1
        scores_points+=1
        apple_x, apple_y = spam_apple(snake)
    
    if len(snake) != len(set(snake)):
      break #game_over

    
    [pygame.draw.rect(screen, BLACK, (i, j, BLOCK_SIZE, BLOCK_SIZE)) for i, j in snake]
    pygame.draw.rect(screen, WHITE, (snake[-1][0], snake[-1][1], BLOCK_SIZE, BLOCK_SIZE)) 
    pygame.draw.rect(screen, RED, (apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE))
    text = scores_text.render(f"Scores: {scores_points}", 0, RED) 

    input_box = pygame.Rect(100, 100, 140, 32)

    screen.blit(text, (10, 25))
    clock.tick(10)
    pygame.display.flip()