import pygame
import os

PIRANHA_PLANTS_IMGS = [
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "1.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "2.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "3.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "4.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "5.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "6.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "7.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "8.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "9.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/piranhaPlant", "10.png"))),
]

FIREBALL_IMGS = [
  pygame.image.load(os.path.join("images/piranhaPlant/fireball", "1.png")),
  pygame.image.load(os.path.join("images/piranhaPlant/fireball", "2.png")),
  pygame.image.load(os.path.join("images/piranhaPlant/fireball", "3.png")),
  pygame.image.load(os.path.join("images/piranhaPlant/fireball", "4.png")),
  pygame.image.load(os.path.join("images/piranhaPlant/fireball", "5.png")),
  pygame.image.load(os.path.join("images/piranhaPlant/fireball", "6.png")),
  pygame.image.load(os.path.join("images/piranhaPlant/fireball", "7.png")),
  pygame.image.load(os.path.join("images/piranhaPlant/fireball", "8.png")),
]

class PiranhaPlant():
  ANIMATION_TIME = 5

  def __init__(self):
    self.img_num = 0
    self.img = PIRANHA_PLANTS_IMGS[0]
    self.IMGS = PIRANHA_PLANTS_IMGS
    self.tilt = 0 # how much the image will tilt 
    self.shootFireball = False

  def draw(self, window, x, y):
    self.img_num += 1

    if self.img_num < self.ANIMATION_TIME:
      self.img = self.IMGS[0]
    elif self.img_num < self.ANIMATION_TIME*2:
      self.img = self.IMGS[1]
    elif self.img_num < self.ANIMATION_TIME*3:
      self.img = self.IMGS[2]
    elif self.img_num < self.ANIMATION_TIME*4:
      self.img = self.IMGS[3]
    elif self.img_num == self.ANIMATION_TIME*4 + 1:
      self.img = self.IMGS[4]
    elif self.img_num == self.ANIMATION_TIME*5 + 1:
      self.img = self.IMGS[5]
    elif self.img_num == self.ANIMATION_TIME*6 + 1:
      self.img = self.IMGS[7]
    elif self.img_num == self.ANIMATION_TIME*7 + 1:
      self.img = self.IMGS[8]
      self.shootFireball = True
    elif self.img_num == self.ANIMATION_TIME*8 + 1:
      self.img = self.IMGS[9]
      self.img_num = 0
    
    if self.tilt <= -80:
      self.img = self.IMGS[1]
      self.img_num = self.ANIMATION_TIME*2

    rotated_image = pygame.transform.rotate(self.img, self.tilt)

    new_rectangle = rotated_image.get_rect(center = self.img.get_rect(topleft = (x, y)).center)

    window.blit(rotated_image, new_rectangle.topleft)

class FireBall(pygame.sprite.Sprite):
  ANIMATION_TIME = 5

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.img_num = 0
    self.img = FIREBALL_IMGS[0]
    self.IMGS = FIREBALL_IMGS
    self.x = 0
    self.y = 0
    self.rect = self.img.get_rect()

  def draw(self, window, x, y):
    self.x = x
    self.y = y
    self.img_num += 1
    if self.img_num < self.ANIMATION_TIME:
      self.img = self.IMGS[0]
      self.rect = self.img.get_rect()

    elif self.img_num < self.ANIMATION_TIME*2:
      self.img = self.IMGS[1]
      self.rect = self.img.get_rect()

    elif self.img_num < self.ANIMATION_TIME*3:
      self.img = self.IMGS[2]
      self.rect = self.img.get_rect()
    
    elif self.img_num < self.ANIMATION_TIME*4:
      self.img = self.IMGS[3]
      self.rect = self.img.get_rect()
    
    elif self.img_num == self.ANIMATION_TIME*4 + 1:
      self.img = self.IMGS[4]
      self.rect = self.img.get_rect()
    
    elif self.img_num == self.ANIMATION_TIME*5 + 1:
      self.img = self.IMGS[5]
      self.rect = self.img.get_rect()
    
    elif self.img_num == self.ANIMATION_TIME*6 + 1:
      self.img = self.IMGS[7]
      self.rect = self.img.get_rect()
      self.img_num = 0
    


    new_rectangle = self.img.get_rect(center = self.img.get_rect(topleft = (x, y)).center)

    window.blit(self.img, new_rectangle.topleft)

  def collide(self, fireball, bird):
    bird_mask = bird.get_mask()
    fireball_mask = pygame.mask.from_surface(self.img)

    offset = (self.x - bird.x, self.y - round(bird.y))
    
    colide_point = bird_mask.overlap(fireball_mask, offset)

    
    if colide_point:
      return True #bird colide with fireball
    
    return False