import pygame
import os

BIRD_IMGS = [
  pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))
]

class Bird:
  IMGS = BIRD_IMGS
  MAX_ROTATION = 25
  ROTATION_VELOCITY = 20
  ANIMATION_TIME = 5

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.tilt = 0 # how much the image will tilt 
    self.tick_count = 0 #Time. how many seconds we've been moving for
    self.vel = 0
    self.height = self.y
    self.img_num = 0
    self.img = self.IMGS[0]

  def jump(self):
    self.vel = -10.5
    self.tick_count = 0
    self.height = self.y

  def move(self):
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

  def draw(self, window):
    self.img_num += 1
    if self.img_num < self.ANIMATION_TIME:
      self.img = self.IMGS[0]
    elif self.img_num < self.ANIMATION_TIME*2:
      self.img = self.IMGS[1]
    elif self.img_num < self.ANIMATION_TIME*3:
      self.img = self.IMGS[2]
    elif self.img_num < self.ANIMATION_TIME*4:
      self.img = self.IMGS[1]
    elif self.img_num == self.ANIMATION_TIME*4 + 1:
      self.img = self.IMGS[0]
      self.img_num = 0
    
    if self.tilt <= -80:
      self.img = self.IMGS[1]
      self.img_num = self.ANIMATION_TIME*2

    rotated_image = pygame.transform.rotate(self.img, self.tilt)

    new_rectangle = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)

    window.blit(rotated_image, new_rectangle.topleft)

  def get_mask(self):
    return pygame.mask.from_surface(self.img)
