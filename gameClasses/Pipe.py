import pygame
import os
import random 
from gameClasses.PiranhaPlant import PiranhaPlant
from gameClasses.PiranhaPlant import FireBall

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
RED_PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "redPipe.png")))

class Pipe:
  GAP = 200
  VEL = 5
  
  def __init__(self, x, movePipesVertically, showPiranhaPlant):
    self.x = x
    self.height = 0
    self.gap = 200

    self.top = 0
    self.bottom = 0

    self.verticalMove = 0
    self.horizontalMove = 0

    self.moveUp = True
    self.movePipesUpDown = movePipesVertically

    self.showPiranhaPlant = showPiranhaPlant
    self.piranha = PiranhaPlant()
    self.fireball = FireBall()
    self.fireballMove = 10

    if showPiranhaPlant:
      self.PIPE_TOP = pygame.transform.flip(RED_PIPE_IMG, False, True)
      self.PIPE_BOTTOM = RED_PIPE_IMG
    else:
      self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
      self.PIPE_BOTTOM = PIPE_IMG

    self.passed = False
    self.set_height()


  def set_height(self):
    if self.showPiranhaPlant:
      self.top = -400
      self.bottom = 400
      self.height = 200

    else:
      self.height = random.randrange(50, 450)
      self.top = self.height - self.PIPE_TOP.get_height()
      self.bottom = self.height + self.GAP

  def move(self):
    if self.movePipesUpDown and not self.showPiranhaPlant:
      self.movePipesVertically()

    self.x -= self.VEL

  def movePipesVertically(self):
    if self.height <= 40 or self.bottom >= 570:
      # print('BATEU NO TOPO')
      self.moveUp = False
      self.verticalMove = 0

    if self.bottom >= 570:
      # print('BATEU NO BOTTOM')
      self.moveUp = True
      self.verticalMove = 0


    if self.moveUp:
      self.top -= 3
      self.height -= 3
      self.bottom -= 3
      self.verticalMove += 1
      if self.verticalMove == 100:
        self.moveUp = False
    else:
      self.top += 3
      self.height += 3
      self.bottom += 3
      self.verticalMove -= 1
      if self.verticalMove == 0:
        self.moveUp = True

  def draw(self, window):
    if self.showPiranhaPlant:
      self.piranha.draw(window, self.x, self.height + 45)
      if self.piranha.shootFireball:
        self.fireball.draw(window, self.x - self.fireballMove, self.height + 85)
        self.fireballMove += 5


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
