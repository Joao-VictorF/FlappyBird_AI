import pygame
import time
import os

from gameClasses.Bird import Bird
from gameClasses.Pipe import Pipe
from gameClasses.Base import Base


pygame.font.init()
# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

STAT_FONT =  pygame.font.SysFont("comicsans", 80)

def draw_window(window, bird, pipes, base, score):
  window.blit(BG_IMG, (0, 0))
  for pipe in pipes:
    pipe.draw(window)

  text = STAT_FONT.render(str(score), 1, (255, 255, 255))
  window.blit(text, (int(WIN_WIDTH/2), 30))
  base.draw(window)
  bird.draw(window)
  pygame.display.update()

def main():
  score = 0
  # bird = Bird(150, 250)
  bird = Bird(230, 350)
  base = Base(620)
  pipes = [Pipe(600)]
  window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  clock = pygame.time.Clock()
  pygame.display.set_caption('Flappy Bird AI')
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
        print("kkk pego no cano")

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
    
    if bird.y + bird.img.get_height() >=620: #bird hit the ground
      print("pego no chao")
      # pass

    base.move()
    draw_window(window, bird, pipes, base, score)
  pygame.quit()
  quit()

main()