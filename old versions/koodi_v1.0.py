import pygame, random, math, time, eztext, handmade30x40matrixes
from colors import *
import os
from time import gmtime, strftime

clock = pygame.time.Clock()

game_name = "MAZEv1" # for savegame files
gamescreen_width = 960
gamescreen_height = 600 # = gamewindow's height - 100
icon_image = pygame.image.load('Images/MazeIcon1.png')
show_mazecreation_on_screen = True

def ismouseinrect(x,y,width,height):
    # x, y = top left corner of the rectangle
    mouse = pygame.mouse.get_pos()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        return True
    else: 
        return False

class Mainmenu(object):

    """This class is called from Startscreen and passed to main. Contains all the user input game information"""

    def __init__(self):
        self.playername = ""
        self.inputsize = [0,0] # [width, height]
        self.select = 0
        self.inputlevelnumber = 0
        self.selected_theme = THEME1
        self.input_pixels = 20
        self.showcreation = False
        self.startscreen()

    def pressbutton(self, screen, event, message, x, y, width, height, icrect, ictext, acrect, actext):
        # draw buttons
        # draw.rect parameters: (x, y, width, height)
        if ismouseinrect(x,y,width,height):
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

    def create_highscores_file(self):
        hsfile = open('highscores.ma', 'w')
        hsfile.write('MAZEv1 highscores_file\n')
        hsfile.close()

    def read_scoretable(self):
        if not os.path.isfile('highscores.ma'):
            self.create_highscores_file()
        f = open('highscores.ma', 'r')
        current_line = ''
        current_line = f.readline()
        header_parts = current_line.split(" ")
        if header_parts[0] != game_name or header_parts[1].strip().lower() != 'highscores_file':
            self.create_highscores_file()

        scores = {}
        current_line = f.readline()
        parts = current_line.split('_')
        count = 0
        # save all highscores to scores -dictionary
        while current_line != '':
            if parts[0] in scores:
                if scores[parts[0]] < int(parts[1]):
                    scores[parts[0]] = int(parts[1])
            else:
                scores[parts[0]] = int(parts[1])
            current_line = f.readline()
            parts = current_line.split('_')

        f.close()

        best_list = sorted(scores.items(), key=lambda x: x[1], reverse = True) # makes an arranged list of the dictionary scores.
        return best_list

    def show_scoretable(self,screen, x, y, scores, highscoretext):
        highscoretext.setcenter(x, y-50)
        screen.blit(highscoretext.getsurface(BLACK), highscoretext.pos)
        for item in scores:
            text = Displaymessage(item[0]+' : '+str(item[1]), None, 30); text.setcenter(x, y)
            screen.blit(text.getsurface(BLACK), text.pos)
            y += 30
            if y > 560:
                break

    def startscreen(self):
        """This function is the first screen called in the main()
        User can input new parameters to start a new game or load the game from a file """
        # startscreen texts
        welcometext = Displaymessage('Welcome to the MAZE!', None, 90); welcometext.setcenter(400,70)
        welcometext2 = Displaymessage('Your objective is to get out', None, 30); welcometext2.setcenter(400,120)
        instructionstext = Displaymessage('(Use arrow keys to navigate through the maze into the coloured portal. Then press spacebar)', None, 25)
        instructionstext.setcenter(400,150)
        inputnametext = Displaymessage('Input your name:', None, 45)
        playbuttontext = Displaymessage('PLAY!', None, 45)
        loadbuttontext = Displaymessage('Load Game', None, 45)
        readygamebuttontext = Displaymessage('Play a ready game!', None, 30)
        highscoretext = Displaymessage('Highscores:', None, 45)
        pixelerrortext = Displaymessage('Unrestricted pixelsize', None, 30); pixelerrortext.setcenter(150, 270)
        pixelerrortext2 = Displaymessage('Unrestricted pixelsize', None, 30); pixelerrortext2.setcenter(150, 520)
        
        # inputbox for inputting pixelsize
        inputpixelbox = eztext.Input(x=305,y=220,font=pygame.font.Font(None,40),maxlength=2,restricted='1234567890',color=BLACK,prompt='')
        pixeltext = Displaymessage('''Enter square's size in pixels. Max=60, Min=2''', None, 20); pixeltext.setcenter(inputpixelbox.x+15, inputpixelbox.y-30)
        pixeltext2 = Displaymessage('does not affect when loading a game', None, 15); pixeltext2.setcenter(inputpixelbox.x+15, inputpixelbox.y-18)
        #checkboxes for colortheme selection
        themecheckbox1 = Checkbox(300,290,35,35, BRIGHTRED, 'theme1')
        themecheckbox2 = Checkbox(300,370,35,35, WHITE, 'theme2')
        themecheckbox3 = Checkbox(300,450,35,35, WHITE, 'theme3')
        themecheckbox4 = Checkbox(300,530,35,35, WHITE, 'theme4')

        # screen
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(game_name+' Main Menu')
        pygame.display.set_icon(icon_image)

        # read hiscores -file
        scorelist = self.read_scoretable()

        inputpixelbox.value = str(self.input_pixels)
        intro = True
        select = 0; event = pygame.event.Event(1)
        while intro:  # select=1: play new game, select=2: load game

            events = pygame.event.get()
            for event in events:
                #print(event)
                if event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()
                    quit()
                
            screen.fill(WHITE)
            screen.blit(welcometext.getsurface(BLACK), welcometext.pos)
            screen.blit(welcometext2.getsurface(BLACK), welcometext2.pos)
            screen.blit(instructionstext.getsurface(BLACK), instructionstext.pos)
            screen.blit(pixeltext.getsurface(BLACK), pixeltext.pos)
            screen.blit(pixeltext2.getsurface(BLACK), pixeltext2.pos)

            self.show_scoretable(screen, 610, 250, scorelist, highscoretext) # blit hiscores if there are any

            # handle pixelbox
            pygame.draw.rect(screen, RED3, (inputpixelbox.x-10, inputpixelbox.y-10, 50, 50))
            inputpixelbox.update(events)
            if inputpixelbox.value != '':
                self.input_pixels = int(inputpixelbox.value) # also save the input data to self's field
            pygame.draw.rect(screen, WHITE, (inputpixelbox.x-6, inputpixelbox.y-6, 42, 42))
            inputpixelbox.draw(screen)

            #handle checkboxes
            if themecheckbox1.show(screen, event) and self.selected_theme != THEME1:
                self.selected_theme = THEME1; themecheckbox1.color = BRIGHTRED
                themecheckbox2.color = WHITE; themecheckbox3.color = WHITE; themecheckbox4.color = WHITE;
            if themecheckbox2.show(screen, event) and self.selected_theme != THEME2:
                self.selected_theme = THEME2; themecheckbox2.color = BRIGHTRED
                themecheckbox1.color = WHITE; themecheckbox3.color = WHITE; themecheckbox4.color = WHITE;
            if themecheckbox3.show(screen, event) and self.selected_theme != THEME3:
                self.selected_theme = THEME3; themecheckbox3.color = BRIGHTRED
                themecheckbox2.color = WHITE; themecheckbox1.color = WHITE; themecheckbox4.color = WHITE;
            if themecheckbox4.show(screen, event) and self.selected_theme != THEME4:
                self.selected_theme = THEME4; themecheckbox4.color = BRIGHTRED
                themecheckbox2.color = WHITE; themecheckbox3.color = WHITE; themecheckbox1.color = WHITE;

            error = False
            # add loadgame and newgame pushbuttons and process failed input
            if self.pressbutton(screen, event, playbuttontext, 50, 220, 200, 100, RED, CYAN, VANILLA, GREEN):
                if 2 <= self.input_pixels <= 60:
                    self.select = 1
                    intro = False
                else:
                    pygame.draw.rect(screen, WHITE, (50,220,200,100))
                    screen.blit(pixelerrortext.getsurface(BRIGHTRED), pixelerrortext.pos); error = True
            if self.pressbutton(screen, event, loadbuttontext, 50, 350, 200, 100, PURPLE, BLACK, YELLOW, VANILLA):
                self.select = 2
                intro = False
            if self.pressbutton(screen, event, readygamebuttontext, 50, 470, 200, 100, BLACK, BRIGHTRED, GREEN2, BRIGHTPURPLE):
                if 2 <= self.input_pixels <= 20:
                    self.select = 3
                    intro = False
                else:
                    pygame.draw.rect(screen, WHITE, (50,470,200,100))
                    screen.blit(pixelerrortext2.getsurface(BRIGHTRED), pixelerrortext2.pos); error = True

            if error:
                pygame.display.update(); time.sleep(0.5)
            event = pygame.event.Event(1) # neutralize event

            pygame.display.update()
            clock.tick(30)

        if self.select == 2:  # load game
            self.loadgamescreen()
            return
        elif self.select == 3: # play a ready game
            self.inputsize = [40, 30]
            self.playername = 'noob'
            self.inputlevelnumber = 1
            return
        elif self.select == 1:  # start a new game
            self.inputscreen()
            return

    def inputscreen(self):
        """called from startscreen if player chooses to play a new game"""
        max_width = gamescreen_width//self.input_pixels
        max_height = gamescreen_height//self.input_pixels
        instructiontext = Displaymessage('Give your name and the labyrinth´s size', None, 45); instructiontext.setcenter(400,40)
        instructiontext2 = Displaymessage('Return-key: next box   Tab-key: previous box   Esc: back to Main Menu', None, 26); instructiontext2.setcenter(400,80)
        instructiontext3 = Displaymessage('max height = '+str(max_height)+', max width = '+str(max_width), None, 22)
        instructiontext4 = Displaymessage('min height and width = 10', None, 22)
        instructiontext5 = Displaymessage('Big mazes take time to create',None, 22); instructiontext5.setcenter(400, 385)
        startbuttontext = Displaymessage('GO!', None, 60)
        nameprompttext = Displaymessage('Name:', None, 50)
        failedinputtext = Displaymessage('You did not enter a name', None, 30)
        failedinputtext2 = Displaymessage('You did not enter width or height', None, 30)
        failedinputtext3 = Displaymessage('Entered width, height or levels are unrestricted', None, 30)
        failedinputtext4 = Displaymessage('You did not enter the amount of levels', None, 30)
        failedinputtext5 = Displaymessage('Name already exists', None, 30)
        
        # startscreen inputboxes
        inputnamebox = eztext.Input(x=370,y=255,font=pygame.font.Font(None,50),maxlength=10, color=BLACK, prompt='')
        inputheightbox = eztext.Input(x=60,y=195,restricted='1234567890',maxlength=3,color=BLACK,prompt='height:')
        inputwidthbox = eztext.Input(x=60,y=285,restricted='1234567890',maxlength=3,color=BLACK,prompt='width:')
        inputlevelsbox = eztext.Input(x=60,y=375,restricted='1234567890',maxlength=2,color=BLACK,prompt='levels:')
        # width and height can only be numbers
        # checkbox for checking if player wants to see maze creation on screen
        checkbox_showcreation = Checkbox(600,350,35,35, WHITE, 'Show maze creation on screen')

        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(game_name+' Input Menu')
        pygame.display.set_icon(icon_image)

        event = pygame.event.Event(1); intro = True; currentinputbox = 1

        while intro:

            screen.fill(WHITE)
            screen.blit(instructiontext.getsurface(BLACK), instructiontext.pos)
            screen.blit(instructiontext2.getsurface(BLACK), instructiontext2.pos)
            screen.blit(instructiontext3.getsurface(BLACK), [25, 150])
            screen.blit(instructiontext4.getsurface(BLACK), [25, 120])
            screen.blit(instructiontext5.getsurface(BLACK), instructiontext5.pos)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        if currentinputbox == 4: currentinputbox = 1
                        else: currentinputbox += 1
                    if event.key == pygame.K_TAB:
                        if currentinputbox == 1: currentinputbox = 4
                        else: currentinputbox -=1 
                    if event.key == pygame.K_ESCAPE:     
                        self.select = 8 # 8 = back to mainmenu
                        return

            if checkbox_showcreation.show(screen, event):
                if self.showcreation:
                    checkbox_showcreation.color = WHITE; self.showcreation = not self.showcreation 
                else:
                    checkbox_showcreation.color = RED3; self.showcreation = not self.showcreation
                    

            # draw boxes for input texts that light up when selected 

            if currentinputbox == 1:
                pygame.draw.rect(screen, RED3, (50, 180, 200, 50))
                inputheightbox.update(events)
            else: pygame.draw.rect(screen, BLACK, (50, 180, 200, 50))
            pygame.draw.rect(screen, WHITE, (55, 185, 190, 40))

            if currentinputbox == 2:
                pygame.draw.rect(screen, RED3, (50, 270, 200, 50))
                inputwidthbox.update(events)
            else: pygame.draw.rect(screen, BLACK, (50, 270, 200, 50))
            pygame.draw.rect(screen, WHITE, (55, 275, 190, 40))

            if currentinputbox == 3:
                pygame.draw.rect(screen, RED3, (50, 360, 200, 50))
                inputlevelsbox.update(events)
            else: pygame.draw.rect(screen, BLACK, (50, 360, 200, 50))
            pygame.draw.rect(screen, WHITE, (55, 365, 190, 40))

            if currentinputbox == 4:
                pygame.draw.rect(screen, RED3, (350, 210, 330, 100))
                inputnamebox.update(events)
            else: pygame.draw.rect(screen, BLACK, (350, 210, 330, 100))
            pygame.draw.rect(screen, WHITE, (355, 215, 320, 90))

            # startgame pressbutton. check that parameters are in restricted areas

            if self.pressbutton(screen, event, startbuttontext, 100, 450, 600, 100, BLUE, BRIGHTGREEN, GREY, PURPLE):
                if inputwidthbox.value != '' and inputheightbox.value != '' and inputnamebox.value != '' and inputlevelsbox.value != '':
                    width = int(inputwidthbox.value)
                    height = int(inputheightbox.value)
                    levelnumber = int(inputlevelsbox.value)
                    if width >= 10 and width <= max_width and height >= 10 and height <= max_height and levelnumber > 0:
                        #check if there already was a file of the corresponding name given
                        if not os.path.isfile('Savegames/'+inputnamebox.value+'.ma'):
                            self.playername = inputnamebox.value # add the information to the self's fields only when the game can be started
                            self.inputsize[0] = width
                            self.inputsize[1] = height
                            self.inputlevelnumber = levelnumber
                            intro = False
                        else:
                            pygame.draw.rect(screen, WHITE, (100, 450, 600, 100))
                            screen.blit(failedinputtext5.getsurface(BRIGHTRED),[120,480])
                            pygame.display.update()
                            time.sleep(1)
                    else:
                        pygame.draw.rect(screen, WHITE, (100, 450, 600, 100))
                        screen.blit(failedinputtext3.getsurface(BRIGHTRED),[120,480])
                        pygame.display.update()
                        time.sleep(1)
                # process failed input
                if inputnamebox.value == '':
                    pygame.draw.rect(screen, WHITE, (100, 450, 600, 100))
                    screen.blit(failedinputtext.getsurface(BRIGHTRED),[120,480])
                    pygame.display.update()
                    time.sleep(0.5)
                if inputheightbox.value == '' or inputwidthbox.value == '':
                    pygame.draw.rect(screen, WHITE, (100, 450, 600, 100))
                    screen.blit(failedinputtext2.getsurface(BRIGHTRED),[120,480])
                    pygame.display.update()
                    time.sleep(0.5)
                if inputlevelsbox.value == '':
                    pygame.draw.rect(screen, WHITE, (100, 450, 600, 100))
                    screen.blit(failedinputtext4.getsurface(BRIGHTRED),[120,480])
                    pygame.display.update()
                    time.sleep(0.5)

            event = pygame.event.Event(1) # neutralize event

            # draw input boxes
            screen.blit(nameprompttext.getsurface(BLACK),[370,220])
            inputnamebox.draw(screen)
            inputheightbox.draw(screen)
            inputwidthbox.draw(screen)
            inputlevelsbox.draw(screen)

            pygame.display.update()
            clock.tick(30)

    def loadgamescreen(self):
        """This method is called if user presses LOAD GAME -button from startscreen"""

        infotext = Displaymessage('Enter playername, which', None, 45); infotext.setcenter(300, 40)
        infotext2 = Displaymessage('the savegame was named after', None, 45); infotext2.setcenter(300,80)
        infotext3 = Displaymessage('Esc: back to Main Menu', None, 30); infotext3.setcenter(300,120)
        loadbuttontext = Displaymessage('LOAD!', None, 45)
        failedinputtext = Displaymessage('Save not found', None, 45)
        # inputbox
        inputname_eztext = eztext.Input(x=120,y=190,font=pygame.font.Font(None,45),maxlength=10, color=BLACK, prompt='name:')

        screen = pygame.display.set_mode([600, 450])
        pygame.display.set_caption(game_name+' Load Game Menu')
        pygame.display.set_icon(icon_image)

        event = pygame.event.Event(1); intro = True

        while intro:

            screen.fill(WHITE)
            screen.blit(infotext.getsurface(BLACK), infotext.pos)
            screen.blit(infotext2.getsurface(BLACK), infotext2.pos)
            screen.blit(infotext3.getsurface(BLACK), infotext3.pos)
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:     
                        self.select = 8 # 8 = back to mainmenu
                        return

            pygame.draw.rect(screen, RED3, (inputname_eztext.x-10, inputname_eztext.y-15, 360, 60))
            inputname_eztext.update(events)
            savegamename = inputname_eztext.value 
            pygame.draw.rect(screen, WHITE, (inputname_eztext.x-5, inputname_eztext.y-10, 350, 50))

            if self.pressbutton(screen, event, loadbuttontext, 140, 300, 300, 100, GREY, BRIGHTBLUE, BLACK, WHITE):
                self.playername = savegamename
                if not os.path.isfile('Savegames/'+self.playername+'.ma') or self.playername == '': # check if there is a corresponing file
                    failedinputtext.setcenter(280, 350)
                    pygame.draw.rect(screen, WHITE, (130, 300, 300, 100))
                    screen.blit(failedinputtext.getsurface(BRIGHTRED),failedinputtext.pos)
                    pygame.display.update()
                    time.sleep(1)
                else:
                    intro = False

            event = pygame.event.Event(1) # neutralize event

            inputname_eztext.draw(screen)
            pygame.display.update()
            clock.tick(30)


class Checkbox(object):

    def __init__(self, x, y, width, height, color, prompttext = None):
        self.width = width
        self.x = x; self.y = y
        self.height = height
        self.color = color
        if prompttext != None:
            self.prompt = Displaymessage(prompttext, None, width//2)
            self.prompt.setcenter(x+self.width//2, y-self.width//4)
        else: self.prompt = None

    def show(self, screen, event):
        screen.blit(self.prompt.getsurface(BLACK),self.prompt.pos)
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x+3, self.y+3, self.width-6, self.height-6))
        if ismouseinrect(self.x,self.y,self.width,self.height):
            if event.type == pygame.MOUSEBUTTONUP:
                return True
            else:
                return False
        

class IO(object):

    def __init__(self, playername = '', levels = 0, y = 0, x = 0, currentcoord = [0,0], score = 0, current_room_no = 0, passed_time = 0, pixel = 0):
        self.matrixes = []
        self.current_room_no = current_room_no
        self.date = ''
        self.y = y; self.x = x
        self.pixel = pixel
        self.levels = levels
        self.currentcoord = currentcoord # [y, x]
        self.score = score; self.passed_time = passed_time
        self.playername = playername

    def write_loadgame(self):
        """this method can overwrite a savegame"""
        if not os.path.exists('Savegames/'):
            os.makedirs('Savegames/')
        file = open('Savegames/'+self.playername+'.ma', 'w')
        file.write(game_name+' save_file\n')
        file.write('#Date='+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'\n')
        file.write('#y='+str(self.y)+'\n')
        file.write('#x='+str(self.x)+'\n')
        file.write('#levels='+str(self.levels)+'\n')
        file.write('#currentlevel='+str(self.current_room_no)+'\n')
        file.write('#currentcoordinates='+str(self.currentcoord[0])+','+str(self.currentcoord[1])+'\n')
        file.write('#currentscore='+str(self.score)+'\n')
        file.write('#time='+str(self.passed_time)+'\n')
        file.write('#pixel='+str(self.pixel)+'\n')
        for a in range(self.levels):
            file.write('#Matrix '+str(a+1)+'\n')
            for j in range(self.y):
                row = self.matrixes[a][j]
                row = str(row)
                row = row.replace('[','')
                row = row.replace(']','')
                row = row.replace(' ','')
                file.write(row+'\n')

        file.close()
        return True

    def read_savegame(self):
        try:
            """This method fills the self with data. Filename's existence is checked in mainmenu"""
            input = open('Savegames/'+self.playername+'.ma', 'r')
            current_line = ''
            current_line = input.readline()
            header_parts = current_line.split(" ")
            if header_parts[0] != game_name or header_parts[1].strip().lower() != 'save_file':
                raise CorruptedMazeFileError("Unknown file type")

            allread = False
            count = 0
            while allread == False and count < 100:
                count += 1
                current_line = input.readline()
                current_line = current_line.strip().lower()
                if '=' in current_line:
                    current_line_parts = current_line.split('=')

                    if current_line_parts[0] == '#date':
                        self.date = current_line_parts[1]

                    elif current_line_parts[0] == '#y':
                        self.y = int(current_line_parts[1])

                    elif current_line_parts[0] == '#x':
                        self.x = int(current_line_parts[1])

                    elif current_line_parts[0] == '#levels':
                        self.levels = int(current_line_parts[1])

                    elif current_line_parts[0] == '#currentlevel':
                        self.current_room_no = int(current_line_parts[1])

                    elif current_line_parts[0] == '#currentscore':
                        self.score = int(current_line_parts[1])

                    elif current_line_parts[0] == '#time':
                        self.passed_time = int(current_line_parts[1])

                    elif current_line_parts[0] == '#pixel':
                        self.pixel = int(current_line_parts[1])

                    elif current_line_parts[0] == '#currentcoordinates':
                        parts = current_line_parts[1].split(',')
                        self.currentcoord = [int(parts[0]), int(parts[1])]

                else:
                    matrix = []
                    current_line_parts = current_line.split(' ')
                    if current_line_parts[0] == '#matrix':
                        if int(current_line_parts[1]) == self.levels:
                            allread = True
                        for j in range(self.y):
                            row = []
                            current_line = input.readline()
                            current_line = current_line.strip().lower()
                            rowmembers = current_line.split(',')
                            for member in rowmembers:
                                row.append(int(member))
                            matrix.append(row)
                        self.matrixes.append(matrix)

            input.close()
        except IOError or OSError:
            raise CorruptedMazeFileError("Unknown file type")

    def handle_highscore(self):
        """This method appends player's name and score to highscores-file when game is won"""
        try:
            iofile = open('highscores.ma', 'r+')
            current_line = ''
            current_line = iofile.readline()
            header_parts = current_line.split(" ")
            if header_parts[0] != game_name or header_parts[1].strip().lower() != 'highscores_file':
                print('appending to high scores did not succeed')
                return
            iofile.write(self.playername+'_'+str(int(self.score))+'\n')
            iofile.close()
        except IOError or OSError:
            raise CorruptedMazeFileError("Unknown file type")


class CorruptedMazeFileError(Exception):

    def __init__(self, message):
        super(CorruptedMazeFileError, self).__init__(message)


class Displaymessage(object):

    """ This class returns the text's surface and rectangle"""

    def __init__(self, text, fontstring, size):
        self.text = text
        self.size = size
        self.fontstring = fontstring
        self.pos = (0,0)

    def getsurface(self, color):
        screen_text = pygame.font.Font(self.fontstring, self.size)
        surface = screen_text.render(self.text, True, color)
        return surface

    def setcenter(self, centerx, centery):
        msg = self.getsurface(WHITE)
        msgpos = msg.get_rect()
        msgpos.center = (centerx, centery)
        self.pos = (msgpos)


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


    def showsolution(self, screen, player, playercolor, mainmenu, fast = False):
        
        ccy = player.rect.y//self.pixel; ccx = player.rect.x//self.pixel  # cc = current coordinates
        previous = 0 # 1 = down, 2 = up, 3 = right, 4 = left
        matrix = self.wallmatrix.matrix
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True; mainmenu.select = 8
            if not fast: # in not fast-mode, solution is shown on screen real time
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
            pygame.draw.rect(screen,portalcolor, (self.portal_xy[0],self.portal_xy[1], self.pixel, self.pixel))
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


class Cell(object):

    def __init__(self, coord, value):
        """called from Astar method from Mazematrix-class"""
        self.coord = coord # [y, x]
        self.value = value # value 1:wall, 2:start, 3:end...
        self.parent = None
        self.g = 0; self.h = 0; self.f = 0

    def set_h(self, endcoord):
        self.h =  10 * (abs(self.coord[0] - endcoord[0]) + abs(self.coord[1] - endcoord[1]))
        self.f = self.h + self.g

    def calc_g(self):
        if self.parent == None:
            self.g = 0
        else:
            self.g = self.parent.g + 10
        self.f = self.h + self.g


class Mazematrix(object): 

    """Has a matrix that represents a single level's walls. Has also methods (algorithms) for creating one at random or solving one"""

    def __init__(self, size, startxy = None): # size[0] = width, size[1] = height
        self.width = size[0]
        self.height = size[1]
        self.matrix = []
        self.startcoordinates = startxy # previous portal's coordinates = [height, width]

    def printmatrix(self, matrix):
        for j in range(self.height):
            print(matrix[j])

    def printselfmatrix(self):
        for j in range(self.height):
            print(self.matrix[j])
    
    def tellcoordinates(self, number_of_square): # number of square = e.g. 1=wall, 2=start...
        for j in range(self.height):
            for i in range(self.width):
                if self.matrix[j][i] == number_of_square:
                    coordinates = [j, i]
                    break
        # returns the found coordinates of number_of_square from the matrix
        return coordinates 

    def makeouterwalls(self, matrix): # create outerwalls to a matrix: 1 means wall

        for j in range(self.height):
            for i in range(self.width):
                if j == 0 or j == self.height - 1 or i == 0 or i == self.width - 1:
                    matrix[j][i] = 1

    def grid(self, variable): # create a matrix full of variable
        matrix = []
        for j in range(self.height):
            row = []
            for i in range(self.width):
                row.append(variable)
            matrix.append(row)
        return matrix

    def randomgrid(self):
        matrix = []
        for j in range(self.height):
            row = []
            for i in range(self.width):
                row.append(random.randint(10,99))
            matrix.append(row)
        return matrix

    def convertrandomnumberstowalls(self, matrix):
        for j in range(self.height):
            for i in range(self.width):
                if matrix[j][i] >= 10:
                    matrix[j][i] = 1

    def makehandmade30x40level(self):
        if self.width != 40 or self.height != 30:
            return False
        else:
            self.matrix = handmade30x40matrixes.maze1
            return True

    def calculate_cell_s_neighbours_that_are_opened(self, matrix, y, x): #for prim's alogirthm
        count = 0
        try:
            if matrix[y+1][x] in [0,2]: 
                count += 1
        except IndexError:
            pass
        try:
            if matrix[y-1][x] in [0,2]: 
                count += 1
        except IndexError:
            pass
        try:
            if matrix[y][x+1] in [0,2]: 
                count += 1
        except IndexError:
            pass
        try:
            if matrix[y][x-1] in [0,2]: 
                count += 1
        except IndexError:
            pass

        return count

    def neighbours(self, currentcellcoordinates, cellgrid, openlist, closedlist): # called from Astar
        y = currentcellcoordinates[0]; x = currentcellcoordinates[1]

        try:
            if cellgrid[y+1][x].value == 1 or [y+1, x] in closedlist: 
                pass
            elif [y+1, x] not in openlist:
                openlist.append([y+1, x])
                cellgrid[y+1][x].parent = cellgrid[y][x]
                cellgrid[y+1][x].calc_g()
            else:
                if cellgrid[y][x].g + 10 < cellgrid[y+1][x].g:
                    cellgrid[y+1][x].parent = cellgrid[y][x]
                    cellgrid[y+1][x].calc_g()
        except IndexError:
            pass

        try:
            if cellgrid[y-1][x].value == 1 or [y-1, x] in closedlist: 
                pass
            elif [y-1, x] not in openlist:
                openlist.append([y-1, x])
                cellgrid[y-1][x].parent = cellgrid[y][x]
                cellgrid[y-1][x].calc_g()
            else:
                if cellgrid[y][x].g + 10 < cellgrid[y-1][x].g:
                    cellgrid[y-1][x].parent = cellgrid[y][x]
                    cellgrid[y-1][x].calc_g()
        except IndexError:
            pass

        try:
            if cellgrid[y][x+1].value == 1 or [y, x+1] in closedlist: 
                pass
            elif [y, x+1] not in openlist:
                openlist.append([y, x+1])
                cellgrid[y][x+1].parent = cellgrid[y][x]
                cellgrid[y][x+1].calc_g()
            else:
                if cellgrid[y][x].g + 10 < cellgrid[y+1][x].g:
                    cellgrid[y][x+1].parent = cellgrid[y][x]
                    cellgrid[y][x+1].calc_g()
        except IndexError:
            pass

        try:
            if cellgrid[y][x-1].value == 1 or [y, x-1] in closedlist: 
                pass
            elif [y, x-1] not in openlist:
                openlist.append([y, x-1])
                cellgrid[y][x-1].parent = cellgrid[y][x]
                cellgrid[y][x-1].calc_g()
            else:
                if cellgrid[y][x].g + 10 < cellgrid[y+1][x].g:
                    cellgrid[y][x-1].parent = cellgrid[y][x]
                    cellgrid[y][x-1].calc_g()
        except IndexError:
            pass

    def countopencells(self):
        count = 0
        for j in range(self.height):
            for i in range(self.width):
                if self.matrix[j][i] in [2,3,6,0]:
                    count += 1
        return count

    def addAstarsolution(self):
        """Use A* -algorithm to solve a maze represented by a matrix"""
        """Ultimately adds the solution path (value 6) to self's matrix"""

        cellgrid = self.grid(None)
        endcoord = self.tellcoordinates(3) # [y, x]
        startcoord = self.tellcoordinates(2)
        opencoordlist = []
        closedlist = []
        for j in range(self.height): # create a matrix - similar to self's matrix - full of "Cell"s 
            for i in range(self.width):
                cell = Cell([j, i], self.matrix[j][i])
                cell.set_h(endcoord)
                cellgrid[j][i] = cell
                if [j, i] == startcoord:
                    opencoordlist.append([j, i])

        currentcellcoord = opencoordlist[0]
        while True:
             # find the cell that has the smallest f
            currentcellcoord = random.choice(opencoordlist)
            for opencoord in opencoordlist:
                if cellgrid[opencoord[0]][opencoord[1]].f < cellgrid[currentcellcoord[0]][currentcellcoord[1]].f:
                     currentcellcoord = opencoord
            if currentcellcoord not in closedlist:
                closedlist.append(currentcellcoord)
                opencoordlist.remove(currentcellcoord)

            self.neighbours(currentcellcoord, cellgrid, opencoordlist, closedlist)

            if endcoord in closedlist or len(opencoordlist) == 0:
                break

        # add path to self's matrix
        coord = endcoord
        parent = cellgrid[coord[0]][coord[1]].parent
        while True:
            try:
                parent = parent.parent
                coord = parent.coord
            except AttributeError:
                print('did not find a solution')
                break
            if parent.coord == startcoord:
                break    
            self.matrix[parent.coord[0]][parent.coord[1]] = 6

    def makeprimsmaze(self, screen = None, show = False, pixel = 0, mainmenu = None):
        """Use Prim's algorithm to create a randomized maze. Method can be used with or without in-screen-show-creation"""
        """ignore all the 'only drawing' -parts if reading only the algorithm"""

        matrix = self.randomgrid() # matrix with random numbers from 10 to 99
        self.makeouterwalls(matrix) # make edges walls
        openedcoordinates = [] # opened coordinates list
        if self.startcoordinates == None:
            starty = random.randint(1,self.height-2); startx = random.randint(1,self.width-2) # start cell
        else:
            starty = self.startcoordinates[0]; startx = self.startcoordinates[1]
        openedcoordinates.append([starty, startx]) # add start cell to opened coordinates
        matrix[starty][startx] = 2 # mark start cell as opened


        if show:
            pygame.draw.rect(screen, wallcolor, (0,0,self.width*pixel, self.height*pixel))
            screen.blit(Displaymessage('f:fast  s:slow',None,20).getsurface(textcolor),(10, gamescreen_height+30)); pygame.display.update()
            pygame.draw.rect(screen, playercolor, (startx*pixel,starty*pixel,pixel,pixel)); pygame.display.update()

        smallestweightcoordinates = []

        done = False
        count = 0 # count is only for drawing
        while not done: 
            count += 1
            smallestweight = 99 # reset smallest weight of the opened list's coordinates' neighbours' values
            notfound = True

            for coordinate in openedcoordinates: # this for-loop checks which neighbour has the lowest weight
                cy = coordinate[0]; cx = coordinate[1]
                
                try:
                    if matrix[cy+1][cx] >= 10 and matrix[cy+1][cx] < smallestweight: # check if the weight is now current smallest
                        if self.calculate_cell_s_neighbours_that_are_opened(matrix, cy+1, cx) == 1:
                            smallestweight = matrix[cy+1][cx]
                            smallestweightcoordinates = [cy+1, cx]
                            notfound = False
                except IndexError:
                    pass
                try:
                    if matrix[cy-1][cx] >= 10 and matrix[cy-1][cx] < smallestweight: # check if the weight is now current smallest
                        if self.calculate_cell_s_neighbours_that_are_opened(matrix, cy-1, cx) == 1:
                            smallestweight = matrix[cy-1][cx]
                            smallestweightcoordinates = [cy-1, cx]
                            notfound = False
                except IndexError:
                    pass
                try:
                    if matrix[cy][cx+1] >= 10 and matrix[cy][cx+1] < smallestweight: # check if the weight is now current smallest
                        if self.calculate_cell_s_neighbours_that_are_opened(matrix, cy, cx+1) == 1:
                            smallestweight = matrix[cy][cx+1]
                            smallestweightcoordinates = [cy, cx+1]
                            notfound = False
                except IndexError:
                    pass
                try:
                    if matrix[cy][cx-1] >= 10 and matrix[cy][cx-1] < smallestweight: # check if the weight is now current smallest
                        if self.calculate_cell_s_neighbours_that_are_opened(matrix, cy, cx-1) == 1:
                            smallestweight = matrix[cy][cx-1]
                            smallestweightcoordinates = [cy, cx-1]
                            notfound = False
                except IndexError:
                    pass

            # ignore if reading algorithm
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True; mainmenu.select = 8
                    if event.key == pygame.K_p:
                        done = True; notfound = True # if p is pressed, stop creating the maze and put the finishpoint to the recent smallest
                    if mainmenu.showcreation and event.key == pygame.K_f:
                        show = False
                    if mainmenu.showcreation and event.key == pygame.K_s:
                        for c in openedcoordinates:
                            pygame.draw.rect(screen, screencolor, (c[1]*pixel,c[0]*pixel,pixel,pixel))
                        show = True
            if mainmenu.showcreation and count % 100 == 0: # only drawing
                for c in openedcoordinates:
                    pygame.draw.rect(screen, screencolor, (c[1]*pixel,c[0]*pixel,pixel,pixel))
                pygame.draw.rect(screen,playercolor,(startx*pixel,starty*pixel, pixel,pixel))
                pygame.display.update()


            if count % 400 == 0: # once every 400 while-loops, this goes through every member of the openedlist and deletes from it, if a cell has no use
                for c in openedcoordinates:
                    if self.calculate_cell_s_neighbours_that_are_opened(matrix, c[0], c[1]) > 1:
                        openedcoordinates.remove(c)


            if notfound: # break if could not open any more cells
                matrix[smallestweightcoordinates[0]][smallestweightcoordinates[1]] = 3
                done = True

                if mainmenu.showcreation: # only drawing
                    for c in openedcoordinates:
                        pygame.draw.rect(screen, screencolor, (c[1]*pixel,c[0]*pixel,pixel,pixel))
                    pygame.draw.rect(screen,playercolor,(startx*pixel,starty*pixel, pixel,pixel))
                    pygame.draw.rect(screen, portalcolor, (smallestweightcoordinates[1]*pixel,smallestweightcoordinates[0]*pixel,pixel,pixel))
                    pygame.display.update(); time.sleep(0.5)

                break

            if show: #only drawing
                pygame.draw.rect(screen, screencolor, (smallestweightcoordinates[1]*pixel,smallestweightcoordinates[0]*pixel,pixel,pixel))
                pygame.display.update()

            matrix[smallestweightcoordinates[0]][smallestweightcoordinates[1]] = 0 # the most important action: open the current smallest
            if self.calculate_cell_s_neighbours_that_are_opened(matrix, smallestweightcoordinates[0], smallestweightcoordinates[1]) < 2:
                # add the current smallest to opened-list only if it has less than two opened neighbours 
                if smallestweightcoordinates not in openedcoordinates: 
                    openedcoordinates.append(smallestweightcoordinates)

        """-----------------------while ends here--------------------------"""

        if done:
            self.convertrandomnumberstowalls(matrix)

        self.matrix = matrix


def main():
    """ Game """
    # pygame library initialization
    pygame.init()
    """ Get all the inforation from mainmenu """
    mainmenu = Mainmenu()
    if mainmenu.select == 8: # start main() over
        return
    global screencolor, wallcolor, textcolor, playercolor, portalcolor
    (wallcolor, screencolor, textcolor, playercolor, portalcolor) = mainmenu.selected_theme
    
    pixel = mainmenu.input_pixels
    points = 0; current_room_no = 0
    passed_time = 0
    width = gamescreen_width
    height = gamescreen_height + 100

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(game_name+' game window')
    pygame.display.set_icon(icon_image)
    screen.fill(screencolor)

    # Create the player object. Player's speed is set to pixel, so it it can only move a square at a time 
    player = Player(mainmenu.playername, pixel, pixel, color = playercolor) 
    
    rooms = [] # list that has all the Level-objects of the current game
    
    # select gamemode, 1 = newgame, 2 = loadgame, 3 = readymadegame
    lastportalxy = None #last portal coordinates initially None
    # create IO-object for saving the game.
    gameIO = IO(playername = mainmenu.playername, levels = mainmenu.inputlevelnumber, y = mainmenu.inputsize[1], x = mainmenu.inputsize[0], pixel = pixel)

    """------------------------------Create levels--------------------------------"""
    if mainmenu.select == 1: # newgame
        pygame.mixer.music.load('Sounds/Elevator_music.ogg')
        pygame.mixer.music.play(-1)
        for i in range(mainmenu.inputlevelnumber):    
            if i == 0: 
                mazematrix = Mazematrix(mainmenu.inputsize) # inputsize is [x,y] here !!!!!
            else: 
                mazematrix = Mazematrix(mainmenu.inputsize, lastportalxy)
            screen.fill(screencolor) # blit waiting-text on screen while matrixes are being created
            wait_text = Displaymessage('Creating maze number '+str(i+1), None, 60)
            wait_text.setcenter(random.randint(width//2-10, width//2+10), random.randint(height-80, height-20))
            screen.blit(wait_text.getsurface(textcolor), wait_text.pos)
            screen.blit(Displaymessage('q: quit',None,23).getsurface(textcolor),(10, height-30))
            screen.blit(Displaymessage('p: stop creating',None,23).getsurface(textcolor),(width-150, height-50)); pygame.display.update()
            # make the current matrix a maze with prim's randomized algorithm and show creation on screen if selected
            mazematrix.makeprimsmaze(screen = screen, show = mainmenu.showcreation, pixel = pixel, mainmenu = mainmenu) 
            if mainmenu.select == 8: # if player pressed q while maze creation, jump back to mainmenu
                pygame.mixer.music.stop(); return
            lastportalxy = mazematrix.tellcoordinates(3)
            room = Level(mazematrix, wallcolor, pixel)
            rooms.append(room)
            gameIO.matrixes.append(mazematrix.matrix) # store matrixes in IO
        current_room = rooms[current_room_no]
        player.set_xy(current_room)
        pygame.mixer.music.stop()

    elif mainmenu.select == 2: # loadgame
        gameIO.read_savegame()
        points = gameIO.score
        passed_time = gameIO.passed_time
        pixel = gameIO.pixel
        current_room_no = gameIO.current_room_no - 1
        player.changepixel(pixel)#re set player's speed and pixel
        for matrix in gameIO.matrixes:
            mazematrix = Mazematrix([gameIO.x, gameIO.y])
            mazematrix.matrix = matrix
            room = Level(mazematrix, wallcolor, pixel)
            rooms.append(room)
        current_room = rooms[gameIO.current_room_no - 1]
        player.rect.y = gameIO.currentcoord[0]*pixel
        player.rect.x = gameIO.currentcoord[1]*pixel # currentcoord=[y,x]
        
    elif mainmenu.select == 3: # ready made game
        # set walls
        for i in range(1):
            mazematrix = Mazematrix(mainmenu.inputsize)
            mazematrix.makehandmade30x40level()
            room = Level(mazematrix, wallcolor, pixel)
            rooms.append(room)
            gameIO.matrixes.append(mazematrix.matrix)
        current_room = rooms[current_room_no]
        player.set_xy(current_room)
    """-------------------------------------------------------------------------"""

    # define some displaytexts
    mainwindowtext = Displaymessage('MAZE', None, width // 12); mainwindowtext.setcenter(width//1.45, height-60)
    mainwindowtext2 = Displaymessage('Try to find your way into the portal', None, width // 25); mainwindowtext2.setcenter(width//1.45, height-20)
    playernametext1 = Displaymessage('Playername:', None, width // 31); playernametext1.setcenter(width//3.3, height-77)
    playernametext2 = Displaymessage(player.name, None, width // 31); playernametext2.setcenter(width//3.5, height-58)
    timetext = Displaymessage('Score: ' + str(points), None, width // 36); timetext.setcenter(width//3.5, height-35)
    leveltext = Displaymessage('Level '+str(current_room_no+1)+' of '+str(len(rooms)), None, width // 36); leveltext.setcenter(width//3.4, height-15)
    savequittext = Displaymessage('q: quit  s: save&quit', None, width // 38); savequittext.setcenter(100,height-50)
    portaltext = Displaymessage('Spacebar: enter portal', None, width // 38); portaltext.setcenter(100, height-75) 
    giveuptext = Displaymessage('j: give up and delete save', None, width // 40); giveuptext.setcenter(105, height-25)
    winningtext = Displaymessage('You Win!', None, width // 5)

    # make player a sprite. for now there is only the player in the movingsprites-list
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)


    """--------------------------Game loop starts here--------------------------"""
    done = False
    while done == False: # game loop

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                quit()

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
                # quit if q is pressed
                if event.key == pygame.K_q:
                    done = 5 # done = 5 means nothing
                # show solution if player gave up and j is pressed
                if event.key == pygame.K_j:
                    done = 3 
                # save and quit game if s is pressed
                if event.key == pygame.K_s:
                    done = 1
                    
            # check if on portal and if space is pressed
            if player.rect.x == current_room.portal_xy[0] and player.rect.y == current_room.portal_xy[1]:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    """append to score if a level is passed"""
                    points += (current_room.wallmatrix.countopencells()//100)**1.2 + (1/pixel)*500

                    if current_room_no == len(rooms) - 1: # game won
                        done = 2
                    else:
                        player.disappear(screen, portalcolor, current_room, current_room.portal_xy)
                        current_room_no += 1
                        current_room = rooms[current_room_no]
                        pygame.draw.rect(screen, screencolor, (0, 0, width, height-100))
                        current_room.wall_list.draw(screen); pygame.display.update()
                        player.appear(screen, screencolor, current_room, current_room.start_xy)
                        player.set_xy(current_room)
                        
                        
        # move according to event
        player.move(current_room.wall_list)

        # check if invisible portal happening; only possible in 'Play a ready game'-mode for now
        player.check_and_jump_to_invisibleportal(screen, screencolor, current_room)

        screen.fill(screencolor) # blank screen

        # draw player and walls
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        # draw portal
        pygame.draw.rect(screen, portalcolor, (current_room.portal_xy[0]-pixel//10, current_room.portal_xy[1]-pixel//10, pixel+pixel//5, pixel+pixel//5))
        if player.rect.x == current_room.portal_xy[0] and player.rect.y == current_room.portal_xy[1]:
            pygame.draw.rect(screen, playercolor, (current_room.portal_xy[0], current_room.portal_xy[1], pixel, pixel))

        # draw texts and text fields
        pygame.draw.rect(screen, textcolor,(0, height-100,width,10))
        pygame.draw.rect(screen, textcolor,(width//2.5, height-100, 5, 100))
        pygame.draw.rect(screen, textcolor,(width//4.6, height-100, 5, 100))

        leveltext.text = 'Level ' + str(current_room_no + 1) + ' of ' + str(gameIO.levels)
        screen.blit(mainwindowtext.getsurface(textcolor), mainwindowtext.pos)
        screen.blit(mainwindowtext2.getsurface(textcolor), mainwindowtext2.pos)
        screen.blit(timetext.getsurface(textcolor), timetext.pos)
        screen.blit(playernametext1.getsurface(textcolor), playernametext1.pos)
        screen.blit(playernametext2.getsurface(textcolor), playernametext2.pos)
        screen.blit(leveltext.getsurface(textcolor), leveltext.pos)
        screen.blit(savequittext.getsurface(textcolor), savequittext.pos)
        screen.blit(portaltext.getsurface(textcolor), portaltext.pos)
        screen.blit(giveuptext.getsurface(textcolor), giveuptext.pos)
        
        pygame.display.update()

        # calculate gamescore
        points -= 0.04; passed_time += 1/30 

        timetext.text = 'Time: ' + str(int(passed_time))

        clock.tick(30)

    """--------------------------Game loop ends here--------------------------"""




    # process winning and losing -situations
    if done == 1: # save the game
        gameIO.current_room_no = current_room_no + 1
        gameIO.currentcoord = [player.rect.y//pixel, player.rect.x//pixel]
        gameIO.score = str(int(points))
        gameIO.passed_time = str(int(passed_time))
        gameIO.write_loadgame()

    elif done == 2: # win
        if os.path.isfile('Savegames/'+player.name+'.ma'): # delete save file
            os.remove('Savegames/'+player.name+'.ma')
        """calculate gamescore for the last time"""
        points = points / (passed_time // 2)

        if points <= 0: gratz = 'bad :('
        elif 100 > points > 0: gratz = 'nice.'
        else: gratz = 'AMAZING!'
        scoretext = Displaymessage('You were '+gratz+' Score was: '+str(int(points)), None, width // 13)
        scoretext.setcenter(width//2, height//3) # flash winning-text
        screen.blit(scoretext.getsurface(playercolor),scoretext.pos)
        winningtext.setcenter(width//2,height//2)
        screen.blit(winningtext.getsurface(textcolor), winningtext.pos); pygame.display.update(); time.sleep(0.7)
        screen.blit(winningtext.getsurface(portalcolor), winningtext.pos); pygame.display.update(); time.sleep(0.7)
        screen.blit(winningtext.getsurface(textcolor), winningtext.pos); pygame.display.update(); time.sleep(0.7)
        screen.blit(winningtext.getsurface(portalcolor), winningtext.pos); pygame.display.update(); time.sleep(0.7)
        screen.blit(winningtext.getsurface(textcolor), winningtext.pos); pygame.display.update(); time.sleep(0.7)
        screen.blit(winningtext.getsurface(portalcolor), winningtext.pos); pygame.display.update(); time.sleep(0.7)
        gameIO.score = points
        gameIO.handle_highscore() # append player's name and scores to highscores-file

    elif done == 3: # lose
        screen.blit(Displaymessage('Loading...',None, 30).getsurface(textcolor),[width-150, height-73]); pygame.display.update()
        for room in rooms: # add solution-paths to matrixes
            room.wallmatrix.addAstarsolution()
        pygame.mixer.music.load('Sounds/Pat_and_Mat_intro.ogg')
        pygame.mixer.music.play(-1)
        current_room.showsolution(screen, player,  playercolor, mainmenu); count = 1; time.sleep(1)
        current_room_no += 1
        if os.path.isfile('Savegames/'+player.name+'.ma'): # delete save file
            os.remove('Savegames/'+player.name+'.ma')
        while current_room_no < gameIO.levels and mainmenu.select != 8: # show each room's solution in screen
            current_room = rooms[current_room_no]
            pygame.draw.rect(screen, screencolor,(0,0,gamescreen_width,gamescreen_height)); current_room.wall_list.draw(screen)
            pygame.draw.rect(screen, portalcolor, (current_room.portal_xy[0]-pixel//10, current_room.portal_xy[1]-pixel//10, pixel+pixel//5, pixel+pixel//5))
            pygame.draw.rect(screen, screencolor,(leveltext.pos.x-20, leveltext.pos.y, 100, 80))
            leveltext.text = 'Level ' + str(current_room_no + 1)
            screen.blit(leveltext.getsurface(textcolor), leveltext.pos)
            pygame.display.update()
            current_room.showsolution(screen, player, playercolor, mainmenu, fast=True); time.sleep(0.5)
            current_room_no += 1
        # lose-animation
        losetext = Displaymessage('YOU LOSE, ' + player.name + '!', None, 20)
        losetext.setcenter(width//2,height//2)
        for i in range(40):
            pygame.draw.rect(screen, screencolor, (0, 0, width, height-100)) # blank the game field
            screen.blit(losetext.getsurface(BRIGHTRED), losetext.pos); pygame.display.update(); #time.sleep(0.05)
            losetext.size += 3; losetext.setcenter(width//2,height//2)
        pygame.mixer.music.stop()

if __name__ == "__main__":
    count = 0
    while count < 1000:
        main()
        count += 1
    pygame.quit()
    quit()



