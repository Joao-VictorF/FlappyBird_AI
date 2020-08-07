import pygame
import os

PORTAL_IMGS = [
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/portal", "1.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/portal", "2.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/portal", "3.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/portal", "4.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/portal", "5.png"))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("images/portal", "6.png"))),
]

class Portal(pygame.sprite.Sprite):
  ANIMATION_TIME = 10

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.img_num = 0
    self.img = PORTAL_IMGS[5]
    self.IMGS = PORTAL_IMGS
    self.x = 0
    self.y = 0
    self.rect = self.img.get_rect()
    self.portalMoveX = 0
    self.portalMoveY = 0

  def draw(self, window, bird):
    self.x = bird.x + 70
    self.y = bird.y - 10
    self.portalMoveX -= 1

    self.img_num += 1
    if self.img_num < self.ANIMATION_TIME:
      self.img = self.IMGS[0]
      self.portalMoveY += 1
      self.rect = self.img.get_rect()

    elif self.img_num < self.ANIMATION_TIME*2:
      self.img = self.IMGS[1]
      self.portalMoveY += 1
      self.rect = self.img.get_rect()

    elif self.img_num < self.ANIMATION_TIME*3:
      self.img = self.IMGS[2]
      self.portalMoveY += 1
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
      self.img_num = 0
      self.portalMoveX = 0
      self.portalMoveY = 0
      bird.animatingPortal = False
    
    
    new_rectangle = self.img.get_rect(center = self.img.get_rect(topleft = (self.x + self.portalMoveX, self.y - self.portalMoveY)).center)

    window.blit(self.img, new_rectangle.topleft)

  def collide(self, bird):
    bird_mask = bird.get_mask()
    portal_mask = pygame.mask.from_surface(self.img)

    offset_x = bird.rect.x - self.rect.x - 20
    offset_y = bird.rect.y - self.rect.y

    # offset = (51, int(self.y - round(bird.y)))
    # print(offset)
    colide_point = bird_mask.overlap(portal_mask, (offset_x, offset_y))
    # collide = pygame.sprite.collide_mask()

    if colide_point:
      # print('bateu')
      return True #bird colide with portal
    
    return False