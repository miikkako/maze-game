import pygame, random, math, time, eztext, handmade30x40matrixes
from colors import *

clock = pygame.time.Clock()


class Mainmenu(object):

    """This class is called from Startscreen and passed to main. Contains all the user input game information"""

    def __init__(self):
        self.playername = ""
        self.inputsize = [0,0] # [width, height]
        self.startscreen()
        self.select
        
    def ismouseinrect(self,x,y,width,height): # x, y = top left corner of the rectangle
        mouse = pygame.mouse.get_pos()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            return True
        else: 
            return False

    def pressbutton(self, screen, event, message, x, y, width, height, icrect, ictext, acrect, actext):
        # draw buttons
        # draw.rect parameters: (x, y, width, height)
        if self.ismouseinrect(x,y,width,height):
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, acrect, (x, y, width, height))
                msg = message.getsurface(actext)
                msgpos = msg.get_rect()
                msgpos.center = ((x + (width / 2)), (y + (height / 2)))
                screen.blit(msg, msgpos)
            elif event.type == pygame.MOUSEBUTTONUP:
                return True
            else:
                pygame.draw.rect(screen, icrect, (x, y, width, height))
                msg = message.getsurface(ictext)
                msgpos = msg.get_rect()
                msgpos.center = ((x + (width / 2)), (y + (height / 2)))
                screen.blit(msg, msgpos)
        else:
            pygame.draw.rect(screen, icrect, (x, y, width, height))
            msg = message.getsurface(ictext)
            msgpos = msg.get_rect()
            msgpos.center = ((x + (width / 2)), (y + (height / 2)))
            screen.blit(msg, msgpos)
        return False

    def loadgame():
        pass

    def startscreen(self):
        """This function is the first screen called in the main()
        User can input new parameters to start a new game or load the game from a file """
        # call mainmenuinfo object

        clock = pygame.time.Clock()

        # startscreen texts
        welcometext = Displaymessage('Welcome to the MAZE!', None, 60)
        welcometext2 = Displaymessage('Your objective is to get out', None, 30)
        inputnametext = Displaymessage('Input your name:', None, 45)
        playbuttontext = Displaymessage('PLAY!', None, 45)
        loadbuttontext = Displaymessage('Load Game', None, 45)
        readygamebuttontext = Displaymessage('Play a ready game!', None, 25)

        
        # screen
        screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('Labyrinth main menu')
        intro = True
        select = 0
        while intro:  # select=1: play new game, select=2: load game

            events = pygame.event.get()
            for event in events:
                # print(event)
                if event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()
                    quit()

            screen.fill(WHITE)
            screen.blit(welcometext.getsurface(BLACK), [180, 30])
            screen.blit(welcometext2.getsurface(BLACK), [270, 80])

            # add loadgame and newgame pushbuttons
            if self.pressbutton(screen, event, playbuttontext, 450, 220, 180, 120, RED, PURPLE, VANILLA, GREEN):
                self.select = 1
                intro = False
            if self.pressbutton(screen, event, loadbuttontext, 100, 220, 180, 120, PURPLE, BLACK, BLACK, VANILLA):
                self.select = 2
                intro = False
            if self.pressbutton(screen, event, readygamebuttontext, 290, 450, 160, 100, BLACK, BRIGHTRED, GREEN2, GREY):
                self.select = 3
                intro = False

            pygame.display.update()
            clock.tick(30)

        if self.select == 2:  # load game
            return
        elif self.select == 3: # play a ready game
            self.inputsize = [40, 30]
            return
        elif select == 1:  # start a new game
            self.inputscreen()
            return

    def inputscreen(self):

        clock = pygame.time.Clock()

        instructiontext = Displaymessage('Give your name and the labyrinth´s size', None, 45)
        instructiontext2 = Displaymessage('press Tab or Return to change box', None, 22)
        instructiontext3 = Displaymessage('max height = 40, max width = 30, min = 10', None, 22)
        startbuttontext = Displaymessage('GO!', None, 60)
        nameprompttext = Displaymessage('Name:', None, 50)
        failedinputtext = Displaymessage('You did not enter a name', None, 30)
        failedinputtext2 = Displaymessage('You did not enter width and/or height', None, 30)
        failedinputtext3 = Displaymessage('Entered width and/or height are unrestricted', None, 30)
        

        # startscreen inputboxes
        inputnamebox = eztext.Input(x=370,y=255,font=pygame.font.Font(None,50),maxlength=10, color=BLACK, prompt='')
        inputwidthbox = eztext.Input(x=60,y=195,restricted='1234567890',maxlength=2,color=BLACK,prompt='width:')
        inputheightbox = eztext.Input(x=60,y=285,restricted='1234567890',maxlength=2,color=BLACK,prompt='height:')
        # width and height can only be numbers

        screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('Labyrinth input menu')

        event = 1; intro = True; currentinputbox = 1

        while intro:

            screen.fill(WHITE)
            screen.blit(instructiontext.getsurface(BLACK), [100, 30])
            screen.blit(instructiontext2.getsurface(BLACK), [150, 80])
            screen.blit(instructiontext3.getsurface(BLACK), [25, 150])

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        if currentinputbox == 3: currentinputbox = 1
                        else: currentinputbox += 1
                    if event.key == pygame.K_TAB:
                        if currentinputbox == 1: currentinputbox = 3
                        else: currentinputbox -=1
            

            # draw boxes for input texts that light up when mouse is in the box and update input boxes

            
            if currentinputbox == 1:
                pygame.draw.rect(screen, RED3, (50, 180, 200, 50))
                inputwidthbox.update(events)
                self.inputsize[0] = inputwidthbox.value # also save the input data to self's attributes
            else: pygame.draw.rect(screen, BLACK, (50, 180, 200, 50))
            pygame.draw.rect(screen, WHITE, (55, 185, 190, 40))
            if currentinputbox == 2:
                pygame.draw.rect(screen, RED3, (50, 270, 200, 50))
                inputheightbox.update(events)
                self.inputsize[1] = inputheightbox.value # also save the input data to self's attributes
            else: pygame.draw.rect(screen, BLACK, (50, 270, 200, 50))
            pygame.draw.rect(screen, WHITE, (55, 275, 190, 40))
            if currentinputbox == 3:
                pygame.draw.rect(screen, RED3, (350, 210, 250, 100))
                inputnamebox.update(events)
                self.playername = inputnamebox.value # also save the input data to self's attributes
            else: pygame.draw.rect(screen, BLACK, (350, 210, 250, 100))
            pygame.draw.rect(screen, WHITE, (355, 215, 240, 90))

            

            # startgame pressbutton. check that width and height are restricted

            if self.pressbutton(screen, event, startbuttontext, 100, 450, 600, 100, BLUE, BRIGHTGREEN, GREY, PURPLE):
                if self.inputsize[0] != '' and self.inputsize[1] != '' and self.playername != '':
                    width = int(self.inputsize[0])
                    height = int(self.inputsize[1])
                    if width >= 10 and width <= 40 and height >= 10 and height <= 30:
                        self.inputsize[0] = int(self.inputsize[0])
                        self.inputsize[1] = int(self.inputsize[1])
                        intro = False
                    else:
                        pygame.draw.rect(screen, WHITE, (100, 450, 600, 100))
                        screen.blit(failedinputtext3.getsurface(BRIGHTRED),[120,480])
                        pygame.display.update()
                        time.sleep(1)
                # process failed input
                if self.playername == '':
                    pygame.draw.rect(screen, WHITE, (100, 450, 600, 100))
                    screen.blit(failedinputtext.getsurface(BRIGHTRED),[120,480])
                    pygame.display.update()
                    time.sleep(1)
                if self.inputsize[0] == '' or self.inputsize[1] == '':
                    pygame.draw.rect(screen, WHITE, (100, 450, 600, 100))
                    screen.blit(failedinputtext2.getsurface(BRIGHTRED),[120,480])
                    pygame.display.update()
                    time.sleep(1)

            # draw input boxes
            screen.blit(nameprompttext.getsurface(BLACK),[370,220])
            inputnamebox.draw(screen)
            inputwidthbox.draw(screen)
            inputheightbox.draw(screen)

            pygame.display.update()
            clock.tick(30)


class Displaymessage(object):

    """ This class returns the text's surface and rectangle"""

    def __init__(self, text, fontstring, size):
        self.text = text
        self.size = size
        self.fontstring = fontstring

    def getsurface(self, color):
        screen_text = pygame.font.Font(self.fontstring, self.size)
        surface = screen_text.render(self.text, True, color)
        return surface


class Gameinfo(object):

    """ This class is for storing game information"""
    loadname = ""

    def __init__(self, player, room_list, current_room_number):
        self.player = player
        self.room_list = room_list
        self.current_room_number = current_room_number

    def updateparameters(self, player, room_list, current_room_number):
        self.player = player
        self.room_list = room_list
        self.current_room_number = current_room_number


class Player(pygame.sprite.Sprite):

    # speed vector
    change_x = 0
    change_y = 0

    speed = 0
    """parameter speed needs to be put manually in main() for now"""

    def __init__(self, name, color = WHITE):

        # Call the parent's constructor
        super().__init__()

        self.name = name
        # Set height and width. Player's color is WHITE
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = 20
        self.rect.x = 20

    def changespeed(self, x, y):
        # change speed if key is pressed in main
        self.change_x += x
        self.change_y += y

    def set_xy(self, current_room):
        # set player's x and y coordinates to the correct square in the current room we are in
        for j in range(current_room.wallmatrix.height):
            for i in range(current_room.wallmatrix.width):
                if current_room.wallmatrix.matrix[j][i] == 2:
                    self.rect.x = i * 20
                    self.rect.y = j * 20

    def move(self, walls):
        """ Find a new position for the player """

        self.rect.x += self.change_x # move x

        # check if player hit wall
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # ff we are moving right, set player's right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # if we are moving left, do the opposite
                self.rect.left = block.rect.right
        
        self.rect.y += self.change_y # move y

        # same thing
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Room(object):

    wall_list = None

    def __init__(self):

        self.wall_list = pygame.sprite.Group()


class Level(Room):

    """This class represents a single Level created from a wallmatrix """
    

    def __init__(self, mazematrix):

        # Make the walls
        Room.__init__(self)

        self.wallmatrix = mazematrix
        self.portal_xy = [-1, -1]
        self.invisibleportal_enter_xy = [-1, -1]
        self.invisibleportal_lead_xy = [-1, -1]
        self.makelevel()

        """ # random colors for inner and outer walls for the Level
        outerwallcolor = random.choice([BLUE, GREEN, RED, PURPLE])
        innerwallcolor = outerwallcolor
        while(innerwallcolor == outerwallcolor):
            innerwallcolor = random.choice([BLUE, GREEN, RED, PURPLE])"""
        
    def makelevel(self):
        # make level
        for j in range(self.wallmatrix.height):
            for i in range(self.wallmatrix.width):
                if self.wallmatrix.matrix[j][i] == 1:
                    wall = Wall(i * 20,j * 20, 20, 20, RED) # wall(x, y, width, height)
                    self.wall_list.add(wall) 
                elif self.wallmatrix.matrix[j][i] == 3:
                    self.portal_xy = [i * 20, j * 20]
                elif self.wallmatrix.matrix[j][i] == 4:
                    self.invisibleportal_enter_xy = [i * 20, j * 20]
                elif self.wallmatrix.matrix[j][i] == 5:
                    self.invisibleportal_lead_xy = [i * 20, j * 20]


    def showsolution(self, screen):
        startcoordinates = self.wallmatrix.tellcoordinates(2) # first tell where startpoint is
        
        ccx = startcoordinates[0]; ccy = startcoordinates[1] # cc = current coordinates
        previous = 0 # 1 = down, 2 = up, 3 = right, 4 = left
        
        while True:
            pygame.draw.rect(screen, WHITE, (ccx*20, ccy*20, 20, 20)); pygame.display.update()
            if self.wallmatrix.matrix[ccy+1][ccx] == 6 and previous != 1: # move down
                ccy += 1; previous = 2
            elif self.wallmatrix.matrix[ccy-1][ccx] == 6 and previous != 2: # move up
                ccy -= 1; previous = 1
            elif self.wallmatrix.matrix[ccy][ccx+1] == 6 and previous != 3: # move right
                ccx += 1; previous = 4
            elif self.wallmatrix.matrix[ccy][ccx-1] == 6 and previous != 4: # move left
                ccx -= 1; previous = 3
            else: break
            


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


class Mazematrix(object): 

    """Has a matrix that represents a single level's walls. Has also methods (algorithms) for creating one at random or solving one"""

    def __init__(self, size): # size[0] = width, size[1] = height
        self.width = size[0]
        self.height = size[1]
        self.matrix = self.emptylevel()

    def emptylevel(self): # create an empty levelmatrix with outerwalls: 0 means empty, 1 means wall
        matrix = []
        for j in range(self.height):
            row = []
            for i in range(self.width):
                if j == 0 or j == self.height - 1 or i == 0 or i == self.width - 1: value = 1
                else: value = 0
                row.append(value)
            matrix.append(row)
        return matrix

    def makehandmade30x40level(self):
        if self.width != 40 or self.height != 30:
            return False
        else:
            self.matrix = handmade30x40matrixes.maze1
            return True

    def tellcoordinates(self, number_of_square): # number of square = e.g. 1=wall, 2=start...
        for j in range(self.height):
            for i in range(self.width):
                if self.matrix[j][i] == number_of_square:
                    coordinates = [i, j]
                    break
        # returns the found coordinates of number_of_square from the matrix
        return coordinates 


def main():
    """ Main Program """
    # pygame library initialization
    pygame.init()
    

    """ Get all the inforation from mainmenu, mainmenu can also calls loadgame """

    mainmenu = Mainmenu()

    points = 0; current_room_no = 0

    """ Game begins here """
    width = 800
    height = 700
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption('Labyrinth')

    # Create the player object
    player = Player(mainmenu.playername)
    player.speed = 20
    
    rooms = []
    
    # select gamemode, 1 = newgame, 2 = loadgame, 3 = readymadegame
    if mainmenu.select == 1 or mainmenu.select == 2: # only a ready made game can be played for now :/
        screen.fill(WHITE)
        screen.blit(Displaymessage('you can only play a ready made 30x40 matrix for now', None, 40).getsurface(BRIGHTRED), [100,330])
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        quit()
    elif mainmenu.select == 3:
        player.name = 'noob'
        # set walls
        for i in range(1):
            mazematrix = Mazematrix(mainmenu.inputsize)
            mazematrix.makehandmade30x40level()
            room = Level(mazematrix)
            rooms.append(room)

    current_room = rooms[current_room_no]
    player.set_xy(current_room)

    
    

    # define some displaytexts
    mainwindowtext = Displaymessage('MAZE', None, width // 16)
    mainwindowtext2 = Displaymessage('Try to find your way out to the green portal', None, width // 23)
    playernametext = Displaymessage('Player: ' + player.name, None, width // 27)
    scoretext = Displaymessage('Score: ' + str(points), None, width // 27)
    winningtext = Displaymessage('You Win!', None, width // 5)
    leveltext = Displaymessage('Level ' + str(current_room_no + 1), None, width // 27)
    savequittext = Displaymessage('q: save & quit', None, width // 38)
    portaltext = Displaymessage('Space: enter portal', None, width // 38)

    """ ---This section needs to be moved to Mazealgorithm """
    
    # insert data to gameinfo
    gameinfo = Gameinfo(player, rooms, 0)

    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    done = False

    while not done: # game loop

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-player.speed, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(player.speed, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -player.speed)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, player.speed)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(player.speed, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-player.speed, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, player.speed)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -player.speed)
                # quit and save if q is pressed
                if event.key == pygame.K_q:
                    done = True
                # show solution if j is pressed
                if event.key == pygame.K_j:
                    done = True
                    current_room.showsolution(screen)

            # check if on portal and if space is pressed
            if player.rect.x == current_room.portal_xy[0] and player.rect.y == current_room.portal_xy[1]:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    points += 100
                    if current_room_no == len(rooms) - 1: # game won. flash winningtext
                        scoretext.text = 'Your Score is amazing: ' + str(int(points)); scoretext.size = width // 10
                        screen.blit(scoretext.getsurface(BRIGHTPURPLE),[20, 100])
                        screen.blit(winningtext.getsurface(BRIGHTBLUE), [160, 300]); pygame.display.update(); time.sleep(0.5)
                        screen.blit(winningtext.getsurface(BRIGHTRED), [160, 300]); pygame.display.update(); time.sleep(0.5)
                        screen.blit(winningtext.getsurface(BRIGHTBLUE), [160, 300]); pygame.display.update(); time.sleep(0.5)
                        screen.blit(winningtext.getsurface(BRIGHTRED), [160, 300]); pygame.display.update(); time.sleep(0.5)
                        screen.blit(winningtext.getsurface(BRIGHTBLUE), [160, 300]); pygame.display.update(); time.sleep(0.5)
                        screen.blit(winningtext.getsurface(BRIGHTRED), [160, 300]); pygame.display.update(); time.sleep(0.5)
                        done = True
                    else:
                        current_room_no += 1
                        current_room = rooms[current_room_no]
                        player.set_xy(current_room)
                        
        # move according to event
        player.move(current_room.wall_list)

        # check if invisible portal happening 
        if player.rect.x == current_room.invisibleportal_enter_xy[0] and player.rect.y == current_room.invisibleportal_enter_xy[1]:
            pygame.draw.rect(screen, BLACK, (player.rect.x,player.rect.y-20, 20, 20));pygame.display.update()

            # reposition player
            player.rect.x = current_room.invisibleportal_lead_xy[0]; player.rect.y = current_room.invisibleportal_lead_xy[1] 
            for i in range(20): # player disappearing at enter coordinates
                pygame.draw.rect(screen, BLACK, 
                    (current_room.invisibleportal_enter_xy[0],current_room.invisibleportal_enter_xy[1], 20, 20))
                pygame.draw.rect(screen, WHITE, 
                    (current_room.invisibleportal_enter_xy[0]+int(0.5*i),current_room.invisibleportal_enter_xy[1]+int(0.5*i), 20-i, 20-i))
                pygame.display.update(); time.sleep(0.05)
            for i in range(20): # player appearing at lead coordinates
                pygame.draw.rect(screen, BLACK,
                    (current_room.invisibleportal_lead_xy[0],current_room.invisibleportal_lead_xy[1], 20, 20))
                pygame.draw.rect(screen, WHITE,
                    (current_room.invisibleportal_lead_xy[0]+int(0.5*(20-i)),current_room.invisibleportal_lead_xy[1]+int(0.5*(20-i)), i, i))
                pygame.display.update(); time.sleep(0.05)


        # draw screen
        screen.fill(BLACK)

        # draw portal
        pygame.draw.rect(screen, BRIGHTGREEN, (current_room.portal_xy[0] - 2, current_room.portal_xy[1] - 2, 24, 24))

        # draw player and walls
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        # draw texts
        screen.blit(mainwindowtext.getsurface(WHITE), [345, 620])
        screen.blit(mainwindowtext2.getsurface(WHITE), [270, 670])
        screen.blit(scoretext.getsurface(WHITE), [20, 650])
        screen.blit(playernametext.getsurface(WHITE), [600, 630])
        screen.blit(leveltext.getsurface(WHITE), [20, 610])
        screen.blit(savequittext.getsurface(WHITE), [160, 610])
        screen.blit(portaltext.getsurface(WHITE), [160, 640])
        leveltext.text = 'Level ' + str(current_room_no + 1)


        pygame.display.update()

        # calculate gamescore
        points -= 0.05
        scoretext.text = 'Score: ' + str(int(points))

        clock.tick(30)

        # store game information in every loop so that the game
        # can be saved anytime
        gameinfo.updateparameters(player, rooms, current_room_no)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
