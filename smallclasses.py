import pygame
from koodi import *
from gameinfo import *

class Checkbox(object):

    def __init__(self, x, y, width, height, color, prompttext = ''):
        self.width = width
        self.x = x; self.y = y
        self.height = height
        self.color = color
        if prompttext != '':
            self.prompt = Displaymessage(prompttext, defaultfont, width//2)
            self.prompt.setcenter(x+self.width//2, y-self.width//4)
        else: self.prompt = ''

    def show(self, screen, event):
        screen.blit(self.prompt.getsurface(BLACK),self.prompt.pos)
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x+3, self.y+3, self.width-6, self.height-6))
        if ismouseinrect(self.x,self.y,self.width,self.height):
            if event.type == pygame.MOUSEBUTTONUP:
                return True
            else:
                return False


class Displaymessage(object):

    """ This class returns the text's surface and rectangle"""

    def __init__(self, text, fontstring, size):
        self.text = text
        self.size = size
        self.fontstring = fontstring
        self.pos = (0,0)

    def getsurface(self, color):
        screen_text = pygame.font.SysFont(self.fontstring, self.size)
        surface = screen_text.render(self.text, True, color)
        return surface

    def setcenter(self, centerx, centery):
        msg = self.getsurface(WHITE)
        msgpos = msg.get_rect()
        msgpos.center = (centerx, centery)
        self.pos = (msgpos)


class CorruptedMazeFileError(Exception):

    def __init__(self, message):
        super(CorruptedMazeFileError, self).__init__(message)

def ismouseinrect(x,y,width,height):
    # x, y = top left corner of the rectangle
    mouse = pygame.mouse.get_pos()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        return True
    else: 
        return False



def pause(screen, textcolor):
    pause = True
    pausemessage = Displaymessage('PAUSED', defaultfont, 4*normalfontsize); pausemessage.setcenter(gamescreen_width//2, (gamescreen_height-100)//2)
    info_message = Displaymessage('press Spacebar or p to unpause', defaultfont, 3*normalfontsize); info_message.setcenter(gamescreen_width//2, gamescreen_height-200)
    while pause:
        screen.blit(pausemessage.getsurface(textcolor), pausemessage.pos)
        screen.blit(info_message.getsurface(textcolor), info_message.pos)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    pause = False

