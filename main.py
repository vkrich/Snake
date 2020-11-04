import pygame
import sys
import random
import sqlite3

# colors
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# all is divided by blocksize
BLOCK_SIZE = 25
# size of playground
size = (BLOCK_SIZE*BLOCK_SIZE, BLOCK_SIZE*BLOCK_SIZE)

# inheritance from Sprite for image on background
class Background(pygame.sprite.Sprite):
  def __init__(self, image_file, location):
    pygame.sprite.Sprite.__init__(self) 
    self.image = pygame.image.load(image_file)
    self.rect = self.image.get_rect()
    self.rect.left, self.rect.top = location


def table_creation():
  # connect to db
  conn = sqlite3.connect("Snake.db")   
  cursor = conn.cursor()  
  # Create table for saving players scores
  cursor.execute("""CREATE TABLE players (
                  player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  player_name text NOT NULL,
                  scores INTEGER 
                );
                """)
  # commit changes in db        
  conn.commit()  


def spam_apple(snake, stones):
  '''Function generate coords for apple'''
  a = random.randrange(0, size[0]-BLOCK_SIZE, BLOCK_SIZE)
  b = random.randrange(0, size[1]-BLOCK_SIZE, BLOCK_SIZE)
  # a, b mod BLOCK_SIZE == 0
  # a, b < size[0], size[1]
  if (a, b) in snake or (a, b) in stones:
    a, b = spam_apple(snake, stones)
    # generate a, b again
  return (a, b)


def game(screen):  
  '''Main game function'''
  # Create coords for snake, stones and apple
  x = random.randrange(BLOCK_SIZE, size[0]-BLOCK_SIZE*2, BLOCK_SIZE)
  y = random.randrange(BLOCK_SIZE, size[1]-BLOCK_SIZE*2, BLOCK_SIZE)
  snake = []
  snake.append((x, y))
  snakesize = len(snake)
  stones = []
  for i in range(250, 301, BLOCK_SIZE):
    for j in range(250, 301, BLOCK_SIZE):
      stones.append((i, j))

  apple_x, apple_y = spam_apple(snake, stones)
  # variables for texting scores
  scores_text_font = pygame.font.SysFont('serif', 36)
  scores_points = 0
  # for moving logic
  direction_moving = {'W': True, 'A': True, 'S': True, 'D': True}
  dx, dy = 0, 0
  clock = pygame.time.Clock()

  while True:                 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()    
    # Background drawing from file
    BackGround = Background('grass.png', [0, 0])
    screen.blit(BackGround.image, BackGround.rect)
     
    keys = pygame.key.get_pressed()
    # Analysing pressed button on keyboard
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
    # snake teleporting cycle
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
    # snake ate apple
    if snake[-1][0] == apple_x and snake[-1][1] == apple_y:
      snakesize+=1
      scores_points+=1
      apple_x, apple_y = spam_apple(snake, stones)   
    
    if len(snake) != len(set(snake)) or set(snake) & set(stones):
      return scores_points
    # draw stones, snake, head snake, apple
    [pygame.draw.rect(screen, BLACK, (i, j, BLOCK_SIZE, BLOCK_SIZE)) for i, j in stones]
    [pygame.draw.rect(screen, BLACK, (i, j, BLOCK_SIZE, BLOCK_SIZE)) for i, j in snake]
    pygame.draw.rect(screen, WHITE, (snake[-1][0], snake[-1][1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, (apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE))

    text_scores = scores_text_font.render(f"Scores: {scores_points}", 0, RED)
    screen.blit(text_scores, (10, 25))
    clock.tick(5)
    #refresh display
    pygame.display.flip()


def user_creation(screen, scores):
  input_text = ""
  input_active = True
  while True:    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        input_active = True
        input_text = ""
      elif event.type == pygame.KEYDOWN and input_active:
        if event.key == pygame.K_RETURN:
          input_active = False
          # GET input text in DB with scores, input_text
        elif event.key == pygame.K_BACKSPACE:
          input_text =  input_text[:-1]
        else:
          input_text += event.unicode

    game_over_background = Background('game_over_cut.jpeg', [0, 0])
    screen.blit(game_over_background.image, game_over_background.rect)
    text_scores = pygame.font.SysFont(None, 100).render(f"Enter your nick:", 0, RED) 
    screen.blit(text_scores, (10, 400))   
    
    font = pygame.font.SysFont(None, 100)
    text_surf = font.render(input_text, True, (255, 0, 0))    
    
    screen.blit(text_surf, (10, 450))
    pygame.display.flip()

# start
pygame.init()
screen = pygame.display.set_mode(size)
taken_scores = game(screen)
user_creation(screen, taken_scores)
pygame.quit()