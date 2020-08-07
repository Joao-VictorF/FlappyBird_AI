import pygame
import time
import os

from gameClasses.Bird import Bird
from gameClasses.Pipe import Pipe
from gameClasses.Base import Base

class HUMAN_PLAYER:
  
  # Constants
  WIN_WIDTH = 500
  WIN_HEIGHT = 800
  MOVE_PIPES = False

  BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

  STAT_FONT =  pygame.font.SysFont("comicsans", 80)

  def __init__(self):
    print("Human player class started")

  def draw_window(self, window, bird, pipes, base, score):
    window.blit(self.BG_IMG, (0, 0))
    for pipe in pipes:
      pipe.draw(window)

    text = self.STAT_FONT.render(str(score), 1, (255, 255, 255))
    window.blit(text, (int(self.WIN_WIDTH/2), 30))
    base.draw(window)
    bird.draw(window)
    pygame.display.update()

  def main(self):
    score = 0
    bird = Bird(230, 350)
    base = Base(620)
    pipes = [Pipe(600, self.MOVE_PIPES, False)]
    window = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    run = True
    while run:
      clock.tick(30)
      bird.move()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            bird.jump()
      
      add_pipe = False
      remove = []

      for pipe in pipes:
        if pipe.collide(bird):
          pygame.quit()

        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
          remove.append(pipe)

        if not pipe.passed and pipe.x < bird.x:
          pipe.passed = True
          add_pipe = True
        
        pipe.move()

      for r in remove:
        pipes.remove(r)

      if add_pipe:
        score += 1
        pipes.append(Pipe(600, self.MOVE_PIPES, False))
      
      if bird.y + bird.img.get_height() >=620: #bird hit the ground
        pygame.quit()
        # pass

      base.move()
      self.draw_window(window, bird, pipes, base, score)
    pygame.quit()
    quit()
