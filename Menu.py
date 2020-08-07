import pygame
import os


from flappyBird_AI import AI_PLAYER
from flappyBird_Human import HUMAN_PLAYER
from gameClasses.Bird import Bird
from gameClasses.Base import Base


pygame.font.init()
# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800
# DRAW_LINES = True  # if this variable is true lines will appear between the bird and the nearest pipe!

pygame.display.set_caption('Flappy Bird AI')

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))
TITLE_IMG = pygame.image.load(os.path.join("images/menu", "menu_title.png"))
HUMAN_BTN_IMG = pygame.image.load(os.path.join("images/menu", "ai_button.png"))
AI_BTN_IMG = pygame.image.load(os.path.join("images/menu", "human_button.png"))

STAT_FONT =  pygame.font.SysFont("comicsans", 80)
END_FONT =  pygame.font.SysFont("comicsans", 40)

def draw_window(window, base, birds):
  window.blit(BG_IMG, (0, 0))
  window.blit(TITLE_IMG, (50, 100))
  window.blit(HUMAN_BTN_IMG, (150, 280))
  window.blit(AI_BTN_IMG, (150, 410))

  base.draw(window)
  for bird in birds:
    bird.draw(window)
  pygame.display.update()



def main():
  ai_player = AI_PLAYER()
  human_player = HUMAN_PLAYER()

  human_btn = pygame.Rect(150, 410, 188, 109)
  ai_btn = pygame.Rect(150, 280, 188, 109)

  base = Base(620)
  birds = [Bird(20, 250), Bird(350, 550), Bird(400, 10)]
  
  window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  clock = pygame.time.Clock()
  run = True

  while run:
    clock.tick(30)

    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          x, y = event.pos
          if ai_btn.collidepoint(x, y):
            ai_player.run()
          if human_btn.collidepoint(x, y):
            human_player.main()

      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
        quit()
        break
    
    base.move()

    draw_window(window, base, birds)
    
main()