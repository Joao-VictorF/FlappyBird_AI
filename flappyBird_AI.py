import pygame
import neat
import time
import os

from gameClasses.Bird import Bird
from gameClasses.Pipe import Pipe
from gameClasses.Base import Base

class AI_PLAYER():
  pygame.font.init()

  # Constants
  WIN_WIDTH = 500
  WIN_HEIGHT = 800
  generations = 0
  # DRAW_LINES = True  # if this variable is true lines will appear between the bird and the nearest pipe!
  DRAW_LINES = False
  MOVE_PIPES = True
  SHOW_PIRANHA = False 

  pygame.display.set_caption('Flappy Bird AI')

  BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

  STAT_FONT =  pygame.font.SysFont("comicsans", 80)
  END_FONT =  pygame.font.SysFont("comicsans", 40)

  def __init__(self):
    print("AI player class started")

  def draw_window(self, window, birds, pipes, base, score, gen, pipe_ind):
    window.blit(self.BG_IMG, (0, 0))

    for pipe in pipes:
      pipe.draw(window)

    base.draw(window)

    for bird in birds:
      # draw lines from bird to pipe
      if self.DRAW_LINES:
        try:
          pygame.draw.line(
            window,
            (255, 0, 0),
            (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2),
            (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height),
            2
          )
          pygame.draw.line(
            window,
            (255, 0, 0),
            (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2),
            (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom),
            2
          )
        except:
          pass
      
      bird.draw(window)
      if bird.animatingPortal:
        bird.portal.draw(window, bird)
    
    # score
    score_label = self.STAT_FONT.render(str(score), 1, (255, 255, 255))
    window.blit(score_label, (int(self.WIN_WIDTH/2), 30))

    # generation
    score_label = self.END_FONT.render("Geração: " + str(gen-1), 1, (255, 255, 255))
    window.blit(score_label, (10, 10))

    # how many birds are alive
    score_label = self.END_FONT.render("Vivos: " + str(len(birds)), 1, (255, 255, 255))
    window.blit(score_label, (10, 50))

    pygame.display.update()

  def main(self, genomes, config):

    self.generations += 1
    nets = []
    ge = []
    birds = []
    PIXELS_RUNNED_TO_SHOW_PIRANHA = 0
    score = 0
    base = Base(620)
    pipes = [Pipe(600, self.MOVE_PIPES, False)]
    
    window = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True


    for genome_id, genome in genomes: # the genome_id, its because genomes are a turple (id, obj)
      genome.fitness = 0
      net = neat.nn.FeedForwardNetwork.create(genome, config)
      nets.append(net)
      birds.append(Bird(230, 350))
      ge.append(genome)


    while run and len(birds) > 0:
      clock.tick(300)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
          pygame.quit()
          quit()
          break
      
      pipe_ind = 0

      if len(birds) > 0:
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
          pipe_ind = 1

      for x, bird in enumerate(birds):
        ge[x].fitness += 0.1
        bird.move()
        # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
        jump_output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

        if self.SHOW_PIRANHA:  
          distance_to_pipe = pipes[pipe_ind].x - bird.x
          pipe_with_piranha = 0 #False
          if PIXELS_RUNNED_TO_SHOW_PIRANHA >= 5:
            pipe_with_piranha = 1 #True

          portal_output = nets[x].activate((distance_to_pipe, abs(pipe_with_piranha), abs(PIXELS_RUNNED_TO_SHOW_PIRANHA)))
          if portal_output[0] > 0.5:
            bird.open_portal()

        if jump_output[0] > 0.5:  # i use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
          bird.jump()

      base.move()
      add_pipe = False
      remove = []

      for pipe in pipes:
        pipe.move()
        for bird in birds:
          # check for collision
          if bird.animatingPortal:
            bird.portal.collide(bird)

          if self.SHOW_PIRANHA: 
            if pipe.fireball.collide(bird):
              bird.birdCollide = True
              if bird.y + bird.img.get_height() -10 >= 620 or bird.y < -50: #bird hit the ground
                ge[birds.index(bird)].fitness -= 1
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

          if pipe.collide(bird):
            bird.birdCollide = True
            if bird.y + bird.img.get_height() -10 >= 620 or bird.y < -50: #bird hit the ground
              ge[birds.index(bird)].fitness -= 1
              nets.pop(birds.index(bird))
              ge.pop(birds.index(bird))
              birds.pop(birds.index(bird))

        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
          remove.append(pipe)

        if not pipe.passed and pipe.x < bird.x:
          bird.countdown_portal -= 1
          pipe.passed = True
          add_pipe = True
              
      if add_pipe:
        score += 1
        for g in ge:
          g.fitness += 5

        if self.SHOW_PIRANHA:  
          if PIXELS_RUNNED_TO_SHOW_PIRANHA >= 5:   
            pipes.append(Pipe(600, self.MOVE_PIPES, True))
            PIXELS_RUNNED_TO_SHOW_PIRANHA = 0
          else:
            pipes.append(Pipe(600, self.MOVE_PIPES, False))
          
          PIXELS_RUNNED_TO_SHOW_PIRANHA += 1  
        else:
          pipes.append(Pipe(600, self.MOVE_PIPES, False))
        
      for r in remove:
        pipes.remove(r)

      for bird in birds:
        # if bird.y + bird.img.get_height() >= 620 or bird.y < 0: #bird hit the ground
        if bird.y + bird.img.get_height() -10 >= 620 or bird.y < -50: #bird hit the ground
          nets.pop(birds.index(bird))
          ge.pop(birds.index(bird))
          birds.pop(birds.index(bird))

      self.draw_window(window, birds, pipes, base, score, self.generations, pipe_ind)
      
  def run(self):
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'neat_configs.txt')
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    #calling the main function 50 times
    winner = population.run(self.main, 1000) 
    print('\nBest bird:\n{!s}'.format(winner))
