import pygame
import os
import random 

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))

class Pipe:
  GAP = 200
  VEL = 5

  def __init__(self, x):
    self.x = x
    self.height = 0
    self.gap = 200

    self.top = 0
    self.bottom = 0
    self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
    self.PIPE_BOTTOM = PIPE_IMG

    self.passed = False
    self.set_height()

  def set_height(self):
    self.height = random.randrange(50, 450)
    self.top = self.height - self.PIPE_TOP.get_height()
    self.bottom = self.height + self.GAP

  def move(self):
    self.x -= self.VEL

  def draw(self, window):
    window.blit(self.PIPE_TOP, (self.x, self.top))
    window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

  def collide(self, bird):
    bird_mask = bird.get_mask()
    top_mask = pygame.mask.from_surface(self.PIPE_TOP)
    bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

    top_offset = (self.x - bird.x, self.top - round(bird.y))

    bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

    bottom_colide_point = bird_mask.overlap(bottom_mask, bottom_offset)

    top_colide_point = bird_mask.overlap(top_mask, top_offset)

    if top_colide_point or bottom_colide_point:
      return True #bird colide with pipe
    
    return False
