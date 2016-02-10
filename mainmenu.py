import pygame
from colors import *
from koodi import *
from gameinfo import *

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
            text = Displaymessage(item[0]+' : '+str(item[1]), defaultfont, 30); text.setcenter(x, y)
            screen.blit(text.getsurface(BLACK), text.pos)
            y += 30
            if y > 560:
                break

    def startscreen(self):
        """This function is the first screen called in the main()
        User can input new parameters to start a new game or load the game from a file """
        # startscreen texts
        welcometext = Displaymessage('Welcome to the MAZE!', defaultfont, 90); welcometext.setcenter(400,70)
        welcometext2 = Displaymessage('Your objective is to get out', defaultfont, 30); welcometext2.setcenter(400,120)
        instructionstext = Displaymessage('(Use arrow keys to navigate through the maze into the coloured portal. Then press spacebar)', defaultfont, 25)
        instructionstext.setcenter(400,150)
        inputnametext = Displaymessage('Input your name:', defaultfont, 45)
        playbuttontext = Displaymessage('PLAY!', defaultfont, 45)
        loadbuttontext = Displaymessage('Load Game', defaultfont, 45)
        readygamebuttontext = Displaymessage('Play a ready game!', defaultfont, 30)
        highscoretext = Displaymessage('Highscores:', defaultfont, 45)
        pixelerrortext = Displaymessage('Unrestricted pixelsize', defaultfont, 30); pixelerrortext.setcenter(150, 270)
        pixelerrortext2 = Displaymessage('Unrestricted pixelsize', defaultfont, 30); pixelerrortext2.setcenter(150, 520)
        
        # inputbox for inputting pixelsize
        inputpixelbox = eztext.Input(x=305,y=220,font=pygame.font.SysFont(defaultfont,40),maxlength=2,restricted='1234567890',color=BLACK,prompt='')
        pixeltext = Displaymessage('''Enter square's size in pixels. Max=60, Min=2''', defaultfont, 20); pixeltext.setcenter(inputpixelbox.x+15, inputpixelbox.y-30)
        pixeltext2 = Displaymessage('does not affect when loading a game', defaultfont, 15); pixeltext2.setcenter(inputpixelbox.x+15, inputpixelbox.y-18)
        #checkboxes for colortheme selection
        themecheckbox1 = Checkbox(300,290,35,35, BRIGHTRED, 'theme1')
        themecheckbox2 = Checkbox(300,370,35,35, WHITE, 'theme2')
        themecheckbox3 = Checkbox(300,450,35,35, WHITE, 'theme3')
        themecheckbox4 = Checkbox(300,530,35,35, WHITE, 'theme4')

        # screen
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(game_name+' Main Menu')
        try:
            pygame.display.set_icon(icon_image)
        except:
            pass

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
        instructiontext = Displaymessage('Give your name and the labyrinth´s size', defaultfont, 45); instructiontext.setcenter(400,40)
        instructiontext2 = Displaymessage('Return-key: next box   Tab-key: previous box   Esc: back to Main Menu', defaultfont, 26); instructiontext2.setcenter(400,80)
        instructiontext3 = Displaymessage('max height = '+str(max_height)+', max width = '+str(max_width), defaultfont, 22)
        instructiontext4 = Displaymessage('min height and width = 10', defaultfont, 22)
        instructiontext5 = Displaymessage('Big mazes take time to create',defaultfont, 22); instructiontext5.setcenter(400, 385)
        startbuttontext = Displaymessage('GO!', defaultfont, 60)
        nameprompttext = Displaymessage('Name:', defaultfont, 50)
        failedinputtext = Displaymessage('You did not enter a name', defaultfont, 30)
        failedinputtext2 = Displaymessage('You did not enter width or height', defaultfont, 30)
        failedinputtext3 = Displaymessage('Entered width, height or levels are unrestricted', defaultfont, 30)
        failedinputtext4 = Displaymessage('You did not enter the amount of levels', defaultfont, 30)
        failedinputtext5 = Displaymessage('Name already exists', defaultfont, 30)
        
        # startscreen inputboxes
        inputnamebox = eztext.Input(x=370,y=255,font=pygame.font.SysFont(defaultfont,50),maxlength=10, color=BLACK, prompt='')
        inputheightbox = eztext.Input(x=60,y=195,font=pygame.font.SysFont(defaultfont,50), restricted='1234567890',maxlength=3,color=BLACK,prompt='height:')
        inputwidthbox = eztext.Input(x=60,y=285,font=pygame.font.SysFont(defaultfont,50), restricted='1234567890',maxlength=3,color=BLACK,prompt='width:')
        inputlevelsbox = eztext.Input(x=60,y=375,font=pygame.font.SysFont(defaultfont,50), restricted='1234567890',maxlength=2,color=BLACK,prompt='levels:')
        # width and height can only be numbers
        # checkbox for checking if player wants to see maze creation on screen
        checkbox_showcreation = Checkbox(600,350,35,35, WHITE, 'Show maze creation on screen')

        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(game_name+' Input Menu')
        try:
            pygame.display.set_icon(icon_image)
        except:
            pass

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

        infotext = Displaymessage('Enter playername, which', defaultfont, 45); infotext.setcenter(300, 40)
        infotext2 = Displaymessage('the savegame was named after', defaultfont, 45); infotext2.setcenter(300,80)
        infotext3 = Displaymessage('Esc: back to Main Menu', defaultfont, 30); infotext3.setcenter(300,120)
        loadbuttontext = Displaymessage('LOAD!', defaultfont, 45)
        failedinputtext = Displaymessage('Save not found', defaultfont, 45)
        # inputbox
        inputname_eztext = eztext.Input(x=120,y=190,font=pygame.font.SysFont(defaultfont,45),maxlength=10, color=BLACK, prompt='name:')

        screen = pygame.display.set_mode([600, 450])
        pygame.display.set_caption(game_name+' Load Game Menu')
        try:
            pygame.display.set_icon(icon_image)
        except:
            pass

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


