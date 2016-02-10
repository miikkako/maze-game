import pygame
from koodi import *
from gameinfo import *


class Player(pygame.sprite.Sprite):

    # speedvector
    change_x = 0
    change_y = 0

    def __init__(self, name, pixel, speed, color = WHITE):

        # Call the parent's constructor
        super().__init__()

        self.name = name
        self.color = color
        self.image = pygame.Surface((pixel, pixel))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0
        self.pixel = pixel
        self.speed = speed

    def changespeed(self, x, y):
        # change speed if an arrow key is pressed in main
        self.change_x += x
        self.change_y += y

    def changepixel(self, pixel):
        # attributes need to be re set when loading the game from a file
        self.pixel = pixel
        self.speed = pixel
        self.image = pygame.Surface((pixel,pixel))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def set_xy(self, current_room):
        # set player's x and y coordinates to the correct square in the current room we are in
        for j in range(current_room.wallmatrix.height):
            for i in range(current_room.wallmatrix.width):
                if current_room.wallmatrix.matrix[j][i] == 2:
                    self.rect.x = i * self.pixel
                    self.rect.y = j * self.pixel

    def move(self, walls):
        """Move player"""

        self.rect.x += self.change_x # move x
        # check if player hit a wall, spirecollide 
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # reposition player if hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
        
        self.rect.y += self.change_y # move y
        # same thing
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def disappear(self, screen, portalcolor, current_room, coord):
        for i in range(self.pixel): # player disappearing at enter coordinates
            pygame.draw.rect(screen, portalcolor, (coord[0],coord[1], self.pixel, self.pixel))
            pygame.draw.rect(screen, self.color, (coord[0]+int(0.5*i),coord[1]+int(0.5*i), self.pixel-i, self.pixel-i))
            pygame.display.update()

    def appear(self, screen, screencolor, current_room, coord):
        for i in range(self.pixel): # player appearing at lead coordinates
            pygame.draw.rect(screen, screencolor,(coord[0],coord[1], self.pixel, self.pixel))
            pygame.draw.rect(screen, self.color,(coord[0]+int(0.5*(self.pixel-i)),coord[1]+int(0.5*(self.pixel-i)), i, i))
            pygame.display.update()

    def check_and_jump_to_invisibleportal(self, screen, screencolor, current_room):
        """This method is only used in the ready game -mode for now"""
        if self.rect.x == current_room.invisibleportal_enter_xy[0] and self.rect.y == current_room.invisibleportal_enter_xy[1]:
            self.jump(screen, screencolor, current_room, [current_room.invisibleportal_enter_xy[0],current_room.invisibleportal_enter_xy[1]],
                [current_room.invisibleportal_lead_xy[0],current_room.invisibleportal_lead_xy[1]])

    def jump(self, screen, screencolor, current_room, fromcoord, tocoord):
        # draw empty around the player because Putin
        if current_room.wallmatrix.matrix[(self.rect.y+self.pixel)//self.pixel][self.rect.x//self.pixel] != 1:
            pygame.draw.rect(screen, screencolor, (self.rect.x, self.rect.y-self.pixel, self.pixel, self.pixel));pygame.display.update()
        if current_room.wallmatrix.matrix[(self.rect.y-self.pixel)//self.pixel][self.rect.x//self.pixel] != 1:
            pygame.draw.rect(screen, screencolor, (self.rect.x, self.rect.y+self.pixel, self.pixel, self.pixel));pygame.display.update()
        if current_room.wallmatrix.matrix[self.rect.y//self.pixel][(self.rect.x+self.pixel)//self.pixel] != 1:
            pygame.draw.rect(screen, screencolor, (self.rect.x-self.pixel, self.rect.y, self.pixel, self.pixel));pygame.display.update()
        if current_room.wallmatrix.matrix[self.rect.y//self.pixel][(self.rect.x-self.pixel)//self.pixel] != 1:
            pygame.draw.rect(screen, screencolor, (self.rect.x+self.pixel, self.rect.y, self.pixel, self.pixel));pygame.display.update()

        # reposition player
        self.rect.x = tocoord[0]; self.rect.y = tocoord[1] 

        self.disappear(screen, screencolor, current_room, fromcoord)
        
        self.appear(screen, screencolor, current_room, tocoord)

