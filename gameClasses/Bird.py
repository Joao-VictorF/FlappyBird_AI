import pygame
import os
from random import randint

YELLOW_BIRD_IMGS = [
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/yellowBird", "bird1.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/yellowBird", "bird2.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/yellowBird", "bird3.png")))
]

BLUE_BIRD_IMGS = [
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/blueBird", "bird1.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/blueBird", "bird2.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/blueBird", "bird3.png")))
]

RED_BIRD_IMGS = [
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/redBird", "bird1.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/redBird", "bird2.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/redBird", "bird3.png")))
]


class Bird(pygame.sprite.Sprite):
  IMGS = []
  MAX_ROTATION = 25
  ROTATION_VELOCITY = 20
  ANIMATION_TIME = 5
  birdCollide = False

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    collorBird = (randint(0, 2))
    global BLUE_BIRD_IMGS, RED_BIRD_IMGS, YELLOW_BIRD_IMGS
    if collorBird == 0:
      self.IMGS = BLUE_BIRD_IMGS
    elif collorBird == 1:
      self.IMGS = RED_BIRD_IMGS
    elif collorBird == 2:
      self.IMGS = YELLOW_BIRD_IMGS
    self.x = x
    self.y = y
    self.tilt = 0 # how much the image will tilt 
    self.tick_count = 0 #Time. how many seconds we've been moving for
    self.vel = 0
    self.height = self.y
    self.img_num = 0
    self.img = self.IMGS[0]
    self.rect = self.img.get_rect()
    self.countdown_shield = 0

  def jump(self):
    self.vel = -10.5
    self.tick_count = 0
    self.height = self.y

  def move(self):
    if self.birdCollide:
      self.moveDown()

    self.tick_count += 1

    # This does is tells us based on our current Birds velocity how much we're moving up or how much we're moving down
    displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2
    # This makes the bird's jump look like an arc, because the offset starts negative (which means the bird is rising, like: -9, -7, -5 .. then 0, and then the offset becomes positive: 2, 4, 6 ... so the birds begin to fall.)

    if displacement >= 16:
      displacement = 16

    if displacement < 0:
      displacement -= 2

    self.y = self.y + displacement

    if displacement < 0 or self.y < self.height + 50:
      if self.tilt < self.MAX_ROTATION:
        self.tilt = self.MAX_ROTATION
    else:
      if self.tilt > -90:
        self.tilt -= self.ROTATION_VELOCITY

  def moveDown(self):
    self.x -= 7
    if self.y >= 620 or self.y < -50:
      pass
    else:
      self.y += 25

  def draw(self, window):
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
      self.img = self.IMGS[1]
      self.rect = self.img.get_rect()
    
    elif self.img_num == self.ANIMATION_TIME*4 + 1:
      self.img = self.IMGS[0]
      self.rect = self.img.get_rect()
      self.img_num = 0
    
    if self.tilt <= -80:
      self.img = self.IMGS[1]
      self.img_num = self.ANIMATION_TIME*2

    rotated_image = pygame.transform.rotate(self.img, self.tilt)

    new_rectangle = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)

    window.blit(rotated_image, new_rectangle.topleft)

  def get_mask(self):
    return pygame.mask.from_surface(self.img)
