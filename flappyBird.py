import pygame
import neat
import time
import os
import random

from Bird import Bird
from Pipe import Pipe
from Base import Base

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

def draw_window(window, bird, pipes, base):
  window.blit(BG_IMG, (0, 0))
  for pipe in pipes:
    pipe.draw(window)

  base.draw(window)
  bird.draw(window)
  pygame.display.update()

def main():
  score = 0
  bird = Bird(150, 250)
  base = Base(620)
  pipes = [Pipe(600)]
  window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  clock = pygame.time.Clock()
  pygame.display.set_caption('Flappy Bird AI')
  run = True
  while run:
    clock.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
    # bird.move()
    add_pipe = False
    remove = []

    for pipe in pipes:
      if pipe.collide(bird):
        pass

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
      pipes.append(Pipe(600))
    
    

    base.move()
    draw_window(window, bird, pipes, base)
  pygame.quit()
  quit()

main()