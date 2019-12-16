import pygame
import os

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))

class Base:
  VEL = 5
  WIDTH = BASE_IMG.get_width()
  IMG = BASE_IMG

  def __init__(self, y):
    self.y = y
    self.base1 = 0
    self.base2 = self.WIDTH

  def move(self):
    self.base1 -= self.VEL
    self.base2 -= self.VEL

    if self.base1 + self.WIDTH < 0:
      self.base1 = self.base2 + self.WIDTH

    if self.base2 + self.WIDTH < 0:
      self.base2 = self.base1 + self.WIDTH

  def draw (self, window):
    window.blit(self.IMG, (self.base1, self.y))
    window.blit(self.IMG, (self.base2, self.y))
