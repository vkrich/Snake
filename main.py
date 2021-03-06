import sys
import random
import sqlite3
import pygame
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QLabel, QMainWindow)
from PyQt5.QtGui import (QFont, QIcon, QPixmap)
from PyQt5.QtCore import QCoreApplication


# colors
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# all is divided by blocksize
with open('config.ini', 'r') as f:
  try:
    BLOCK_SIZE = int(f.read().split('=')[1].strip())
  except TypeError:
    print("Wrong input data for BLOCK_SIZE")
# size of playground
size = (BLOCK_SIZE*BLOCK_SIZE, BLOCK_SIZE*BLOCK_SIZE)

# inheritance from Sprite for image on background
class Background(pygame.sprite.Sprite):
  def __init__(self, image_file, location):
    pygame.sprite.Sprite.__init__(self) 
    self.image = pygame.image.load(image_file)
    self.rect = self.image.get_rect()
    self.rect.left, self.rect.top = location


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
  stones = []
  for i in range(250, 301, BLOCK_SIZE):
    for j in range(250, 301, BLOCK_SIZE):
      stones.append((i, j))

  while (x, y) in stones:
    x = random.randrange(BLOCK_SIZE, size[0]-BLOCK_SIZE*2, BLOCK_SIZE)
    y = random.randrange(BLOCK_SIZE, size[1]-BLOCK_SIZE*2, BLOCK_SIZE)

  snake = []
  snake.append((x, y))
  snakesize = len(snake)  

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
      elif event.type == pygame.KEYDOWN:
        pygame.display.flip()
        if event.key == pygame.K_TAB:
          show_players_table(screen)

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
        x = 0

      if snake[i][0] < 0:          
        snake[i] = (size[0] - BLOCK_SIZE, snake[i][1])
        x = size[0] - BLOCK_SIZE

      if snake[i][1] > size[1] - BLOCK_SIZE:          
        snake[i] = (snake[i][0], 0)
        y = 0

      if snake[i][1] < 0:          
        snake[i] = (snake[i][0], size[1]-BLOCK_SIZE)
        y = size[1] - BLOCK_SIZE

    # snake ate apple
    if snake[-1][0] == apple_x and snake[-1][1] == apple_y:
      snakesize+=1
      scores_points+=1
      apple_x, apple_y = spam_apple(snake, stones)   
    
    # game over
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
  return conn

def user_check(conn, data):
  cursor = conn.cursor()  
  for row in cursor.execute("SELECT * from players ORDER BY scores desc"):
    if row[1] == data[0]:
      sql = '''UPDATE players 
              set scores = ?
              where player_name = ?'''
      cursor.execute(sql, [row[2]+data[1], data[0]])
      conn.commit()
      return False
  return True


def insert_user_information(data):
  # connect to db
  conn = sqlite3.connect("Snake.db") 
  cursor = conn.cursor()  
  if user_check(conn, data):
    # Insert information in table
    cursor.execute("INSERT INTO players(player_name, scores) VALUES (?,?)", data)
    # commit changes in db        
    conn.commit()
  return conn


def show_players_table(screen):  
  conn = sqlite3.connect("Snake.db")   
  cursor = conn.cursor()  
  # Take info from players table
  background_image = Background('space.png', [0, 0])
  while True:    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:     
        return
          
    screen.blit(background_image.image, background_image.rect)
    font = pygame.font.SysFont(None, 80)
    text_surf = font.render("TOP RECORDS:", True, (255, 0, 0))    
    screen.blit(text_surf, (20, 25))
    i = 100
    j = 1
    space=' '
    for row in cursor.execute("SELECT * from players ORDER BY scores desc"):  
      text_info_scores = pygame.font.SysFont('serif', 38)
      if j>9:
        space=''
      current_user_info = f"{j}{space}    {row[1]}     {row[2]}"
      text_info_scores = text_info_scores.render(current_user_info, 0, RED)
      screen.blit(text_info_scores, (100, i))
      i += 30
      j += 1
      if i >= size[1]-BLOCK_SIZE*3:
        break

    font = pygame.font.SysFont(None, 50)
    text_continue = font.render("Click or press any key to go back", True, (255, 0, 0))    
    screen.blit(text_continue, (20, size[1]-BLOCK_SIZE*3))    
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
          return insert_user_information((input_text, scores))        
        elif event.key == pygame.K_BACKSPACE:
          input_text =  input_text[:-1]
        elif event.key == pygame.K_TAB:
          show_players_table(screen)  
        else:
          input_text += event.unicode

    game_over_background = Background('game_over_cut.jpeg', [0, 0])
    screen.blit(game_over_background.image, game_over_background.rect)
    text_scores = pygame.font.SysFont(None, 100).render("Enter your nick:", 0, RED) 
    screen.blit(text_scores, (10, 400))   
    text_info_scores = pygame.font.SysFont('serif', 38).render("Press <TAB> to see Scores Table.", 0, RED) 
    screen.blit(text_info_scores, (20, 40)) 
    
    font = pygame.font.SysFont(None, 100)
    text_surf = font.render(input_text, True, (255, 0, 0))    
    screen.blit(text_surf, (20, 450))
    pygame.display.flip()


def continue_screen(screen):
  background_image = Background('space.png', [0, 0])  
  while True:    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
          return False
        else:   
          return True
    screen.blit(background_image.image, background_image.rect)
    text_continue = pygame.font.SysFont(None, 80).render("DO YOU WANT", 0, RED) 
    screen.blit(text_continue, (50, size[1] - BLOCK_SIZE*20))
    text_continue = pygame.font.SysFont(None, 80).render("TO CONTINUE?", 0, RED) 
    screen.blit(text_continue, (95, size[1] - BLOCK_SIZE*18))
    text_continue = pygame.font.SysFont(None, 60).render("Press ESC or N for QUIT", 0, RED) 
    screen.blit(text_continue, (50, size[1] - BLOCK_SIZE*7))
    text_continue = pygame.font.SysFont(None, 60).render("Press ANY key to continue", 0, RED) 
    screen.blit(text_continue, (50, size[1] - BLOCK_SIZE*4))
   
    pygame.display.flip()
def main_game():  
  pygame.init()
  starter = True
  while starter:    
    screen = pygame.display.set_mode(size)
    taken_scores = game(screen)
    # table_creation()
    user_creation(screen, taken_scores)
    starter = continue_screen(screen)    
  pygame.quit()
  

class MenuWindow(QMainWindow):
  def btn1Clicked(self):
      self.hide()
      main_game()
      
  def btn2Clicked(self):
      #with open("README.md", r) as f:      
      self.btn1.hide()
      self.btn2.hide()
      
      text = ""
      with open('help.txt', 'r') as f:
          for i in f:
              text += i
      
      self.label_help = QLabel(text, self)      
      self.label_help.move(BLOCK_SIZE**2//2-200, 20)
      self.label_help.resize(BLOCK_SIZE**2, BLOCK_SIZE**2-200)
      self.label_help.setFont(QFont('SansSerif', 20))
      self.label_help.setStyleSheet('color: red')
      self.label_help.show()
      
      self.btn3 = QPushButton('Close', self)
      self.btn3.setFont(QFont('SansSerif', 15))
      self.btn3.move(BLOCK_SIZE**2//2-100, 475)
      self.btn3.resize(200, 50)
      self.btn3.clicked.connect(self.btn3Clicked)
      self.btn3.show()
      #main_game()
      
  def btn3Clicked(self):      
      self.btn3.hide()
      self.label_help.hide()
      self.btn1.show()
      self.btn2.show()
    
  def __init__(self): 
    super().__init__() 

    self.acceptDrops()
    self.setWindowIcon(QIcon("snake_icon.png"))     
    # set the title 
    self.setWindowTitle("Snake")    

    # setting  the geometry of window 
    self.setGeometry(0, 0, 625, 567) 
    w = QWidget()    

    # creating label 
    self.label = QLabel(self) 
    self.btn1 = QPushButton('New game', self)
    self.btn1.setFont(QFont('SansSerif', 15))
    self.btn1.move(BLOCK_SIZE**2//2-100, 200)
    self.btn1.resize(200, 50)
    self.btn1.setToolTip('Click for start \bNew game\b')
    self.btn1.clicked.connect(self.btn1Clicked)
    #self.btn1.clicked.connect(main_game())
    self.btn2 = QPushButton('Help', self)
    self.btn2.setFont(QFont('SansSerif', 15))
    self.btn2.move(BLOCK_SIZE**2//2-100, 275)
    self.btn2.resize(200, 50)
    self.btn2.clicked.connect(self.btn2Clicked)
    # loading image 
    self.pixmap = QPixmap('snake.jpg') 

    # adding image to label 
    self.label.setPixmap(self.pixmap) 

    # Optional, resize label to image size 
    self.label.resize(self.pixmap.width(), 
                      self.pixmap.height()) 
    # show all the widgets 
    self.show() 

if __name__ == '__main__':
  #
  # create pyqt5 app 
  App = QApplication(sys.argv) 
    
  # create the instance of our Window 
  window = MenuWindow() 
    
  # start the app 
  sys.exit(App.exec()) 
