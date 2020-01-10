import pygame
import neat
import time
import os

from gameClasses.Bird import Bird
from gameClasses.Pipe import Pipe
from gameClasses.Base import Base

pygame.font.init()
# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800
generations = 0
# DRAW_LINES = True  # if this variable is true lines will appear between the bird and the nearest pipe!
DRAW_LINES = False

pygame.display.set_caption('Flappy Bird AI')

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

STAT_FONT =  pygame.font.SysFont("comicsans", 80)
END_FONT =  pygame.font.SysFont("comicsans", 40)

def draw_window(window, birds, pipes, base, score, gen, pipe_ind):
  window.blit(BG_IMG, (0, 0))

  for pipe in pipes:
    pipe.draw(window)

  base.draw(window)

  for bird in birds:
    # draw lines from bird to pipe
    if DRAW_LINES:
      try:
        pygame.draw.line(window, (255, 0, 0), (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
        pygame.draw.line(window, (255, 0, 0), (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
      except:
        pass
    # draw bird
    bird.draw(window)
  
  # score
  score_label = STAT_FONT.render(str(score), 1, (255, 255, 255))
  window.blit(score_label, (int(WIN_WIDTH/2), 30))

  # generation
  score_label = END_FONT.render("Gens: " + str(gen-1), 1, (255, 255, 255))
  window.blit(score_label, (10, 10))

  # how many birds are alive
  score_label = END_FONT.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
  window.blit(score_label, (10, 50))

  pygame.display.update()

def main(genomes, config):

  global generations

  generations += 1
  nets = []
  ge = []
  birds = []

  score = 0
  base = Base(620)
  pipes = [Pipe(600)]
  
  window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  clock = pygame.time.Clock()
  run = True


  for genome_id, genome in genomes: # the genome_id, its because genomes are a turple (id, obj)
    genome.fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    nets.append(net)
    birds.append(Bird(230, 350))
    ge.append(genome)


  while run and len(birds) > 0:
    clock.tick(40)

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
      output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

      if output[0] > 0.5:  # i use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
        bird.jump()

    base.move()
    add_pipe = False
    remove = []

    for pipe in pipes:
      pipe.move()

      for bird in birds:
        # check for collision
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
        pipe.passed = True
        add_pipe = True
            
    if add_pipe:
      score += 1
      for g in ge:
        g.fitness += 5
      pipes.append(Pipe(600))

    for r in remove:
      pipes.remove(r)

    for bird in birds:
      # if bird.y + bird.img.get_height() >= 620 or bird.y < 0: #bird hit the ground
      if bird.y + bird.img.get_height() -10 >= 620 or bird.y < -50: #bird hit the ground
        nets.pop(birds.index(bird))
        ge.pop(birds.index(bird))
        birds.pop(birds.index(bird))

    draw_window(window, birds, pipes, base, score, generations, pipe_ind)

def run(config_file):
  config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
  neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

  population = neat.Population(config)

  population.add_reporter(neat.StdOutReporter(True))
  stats = neat.StatisticsReporter()
  population.add_reporter(stats)
  #calling the main function 50 times
  winner = population.run(main, 50) 
  print('\nBest bird:\n{!s}'.format(winner))

if __name__ == '__main__':
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'neat_configs.txt')
  run(config_path)