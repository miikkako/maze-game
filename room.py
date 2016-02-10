import pygame
from koodi import *
from gameinfo import *


class Level(object):

    """This class represents a single Level created from a wallmatrix """
    wall_list = None

    def __init__(self, mazematrix, color, pixel):
        # Make the walls
        self.wall_list = pygame.sprite.Group()
        self.color = color
        self.wallmatrix = mazematrix
        self.portal_xy = [-1, -1] # [x, y] !
        self.start_xy = [-1, -1]
        self.invisibleportal_enter_xy = [-1, -1]
        self.invisibleportal_lead_xy = [-1, -1]
        self.pixel = pixel
        self.makelevel()

    def makelevel(self):
        # make level
        for j in range(self.wallmatrix.height):
            for i in range(self.wallmatrix.width):
                if self.wallmatrix.matrix[j][i] == 1 or self.wallmatrix.matrix[j][i] == 8:
                    wall = Wall(i * self.pixel,j * self.pixel, self.pixel, self.pixel, self.color) # wall(x, y, width, height)
                    self.wall_list.add(wall) 
                elif self.wallmatrix.matrix[j][i] == 2:
                    self.start_xy = [i * self.pixel, j * self.pixel]
                elif self.wallmatrix.matrix[j][i] == 3:
                    self.portal_xy = [i * self.pixel, j * self.pixel]
                elif self.wallmatrix.matrix[j][i] == 4:
                    self.invisibleportal_enter_xy = [i * self.pixel, j * self.pixel]
                elif self.wallmatrix.matrix[j][i] == 5:
                    self.invisibleportal_lead_xy = [i * self.pixel, j * self.pixel]


    def showsolution(self, screen, playercolor, portalcolor, mainmenu, fast = False, startxy = None):
        if startxy != None:
            ccy = startxy[0]; ccx = startxy[1] # cc = current coordinates
        else:
            cc = self.wallmatrix.tellcoordinates(2)
            ccy = cc[0]; ccx = cc[1]
        previous = 0 # 1 = down, 2 = up, 3 = right, 4 = left
        matrix = self.wallmatrix.matrix
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True; mainmenu.select = 8 # for jumpin back to mainmenu in the middle of solution show
            if not fast: # in not in fast-mode, solution is shown on screen real time
                pygame.draw.rect(screen, playercolor, (ccx*self.pixel, ccy*self.pixel, self.pixel, self.pixel)); pygame.display.update()
            if matrix[ccy+1][ccx] in [6, 3] and previous != 1: # move down
                ccy += 1; previous = 2
            elif matrix[ccy-1][ccx] in [6, 3] and previous != 2: # move up
                ccy -= 1; previous = 1
            elif matrix[ccy][ccx+1] in [6, 3] and previous != 3: # move right
                ccx += 1; previous = 4
            elif matrix[ccy][ccx-1] in [6, 3] and previous != 4: # move left
                ccx -= 1; previous = 3
            else:
                break
        if fast: # if fast-mode, solution is shown on screen not real time
            self.makelevel()
            self.wall_list.draw(screen)
            pygame.draw.rect(screen, portalcolor, (self.portal_xy[0],self.portal_xy[1], self.pixel, self.pixel))
            for j in range(self.wallmatrix.height):
                for i in range(self.wallmatrix.width):
                    if self.wallmatrix.matrix[j][i] == 6:
                        pygame.draw.rect(screen,playercolor,(i*self.pixel,j*self.pixel, self.pixel, self.pixel))
            pygame.display.update()


class Wall(pygame.sprite.Sprite):

    """ This class represents a single square wall """

    def __init__(self, x, y, width, height, color):

        # sprite
        super().__init__()

        # Make a wall
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # x, y = top left corner
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


