# Let's make a game where a target is drawn randomly on the screen and the average aiming time is calculated
# The game will also have some customisable options such as:
# number of targets, time between targets, target size etc

# Game Plan
# A list of targets are generated in a list before deploying them
# According to the time between targets, one by one will be spawned
# The targets themselves keep track of their time and will add their time in a list
# The game manages this list and when the length of the list is equal to the length of targets:
# show the average time and worst time shots made by the player as well as missed shots and accuracy

# The loop will be managed by the game and when the mouse is clicked:
# Loop through a filtered list of deployed targets and check the distance for each target
# and compare it to the target size
# If any target matches, activate it's shot function
# If not, add one to missed shots counter

import pygame
import random
import time
import math

class Game():
     SCREEN_WIDTH = 1000
     SCREEN_HEIGHT = 800
     FRAMERATE = 30
     BACKGROUND_COLOR = (100, 100, 100)

     def __init__(self, targetAmount, targetDelay, targetSize):
          pygame.init()
          self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

          self.targetAmount = targetAmount
          self.targetDelay = targetDelay
          self.targetSize = targetSize

          self.game_init()

     def game_init(self):
          self.misses = 0
          self.targets = self.generateTargets()
          self.timeDelays = []

     def generateTargets(self):
          targetList = []
          for _ in range(self.targetAmount): 
               # Ran into a problem where two targets can span close to each other. 
               # Fix by measuring the distance to each previous target 
               # and get random values until the distance is greater than the target size
               xpos = random.randint(self.targetSize, self.SCREEN_WIDTH - self.targetSize)
               ypos = random.randint(self.targetSize, self.SCREEN_HEIGHT - self.targetSize)
               targetList.append(Target(xpos, ypos, self.targetSize))
          return targetList

     def distance(self, currentx, currenty, markerx, markery):
          distanceX = currentx - markerx
          distanceY = currenty - markery
          return math.sqrt(pow(distanceX, 2) + pow(distanceY, 2))

     def checkShot(self, shotx, shoty):
          for target in self.targets:
               if self.distance(shotx, shoty, target.xpos, target.ypos) < target.size and target.visible:
                    target.hit(self)
                    return True # We do not want to continue if we hit a target
          # If we're here, then we must have missed
          return False

     def miss(self):
          self.misses += 1 # Might do something fancier here

     def timePassed(self, activeTimer, currentTime, amount):
          return currentTime-activeTimer > amount

     def draw(self):
          self.screen.fill(self.BACKGROUND_COLOR) # Change this to a background later
          for target in self.targets:
               target.draw(self)
          pygame.display.update()
     
     def roundOver(self):
          # Some fancier displays here later. No need to restart
          avg = round(sum(self.timeDelays)/len(self.timeDelays), 2)
          print("Average:", avg, "seconds")
          print("Maximum:", round(max(self.timeDelays), 2), "seconds")
          print("Minimum:", round(min(self.timeDelays), 2), "seconds")
          print("Misses:", self.misses)

     def play(self):
          gameQuit = False
          targetDeployTimer = time.time()
          targetIndex = 0
          startingTimer = time.time() # Use this as a "3, 2, 1, GO" later
          gameStart = False # This corelates with the starting timer

          while len(self.timeDelays) < len(self.targets) and not gameQuit:
               clock = pygame.time.Clock()
               clock.tick(self.FRAMERATE)

               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         gameQuit = True
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                         if not self.checkShot(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                              self.miss()
               
               if self.timePassed(startingTimer, time.time(), 3) and not gameStart:
                    gameStart = True # Here, the "3, 2, 1, GO" can be implemented
               
               if self.timePassed(targetDeployTimer, time.time(), self.targetDelay) and targetIndex < len(self.targets):
                    self.targets[targetIndex].deploy(self)
                    targetIndex += 1
                    targetDeployTimer = time.time()
               

               self.draw()
               
          self.roundOver()
          pygame.quit()
               


class Target():
     COLOR = (255, 150, 50)
     def __init__(self, xpos, ypos, size):
          self.xpos = xpos
          self.ypos = ypos
          self.size = size

          self.visible = False

     def deploy(self, game):
          self.visible = True
          self.delayTimer = time.time()

     def hit(self, game):
          self.visible = False
          game.timeDelays.append(time.time() - self.delayTimer)

     def draw(self, game):
          if self.visible:
               # Change this for style, ex. multiple circles inside
               pygame.draw.circle(game.screen, self.COLOR, (self.xpos, self.ypos), self.size)


if __name__ == "__main__":
     Practice = Game(10, 1, 50)
     Practice.play()