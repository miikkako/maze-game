import pygame, random, math, time, eztext, handmade30x40matrixes
from colors import *
import os
from time import gmtime, strftime
from mainmenu import *
from smallclasses import *
from inputoutput import *
from player import *
from room import *
from algorithms import *
from gameinfo import *

clock = pygame.time.Clock()

def main():
    """ Game """
    # pygame library initialization
    pygame.init()
    """--------------------Get all the inforation from mainmenu----------------"""
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
            screen.blit(Displaymessage('q: quit',None,30).getsurface(textcolor),(10, height-30))
            screen.blit(Displaymessage('p: stop creating',None,30).getsurface(textcolor),(width-180, height-50)); pygame.display.update()
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
    savequittext = Displaymessage('q: quit  s: save&quit', None, width // 38); savequittext.setcenter(100,height-53)
    portaltext = Displaymessage('Spacebar: enter portal', None, width // 38); portaltext.setcenter(100, height-77) 
    giveuptext = Displaymessage('j: give up and delete save', None, width // 40); giveuptext.setcenter(105, height-30)
    pausetext = Displaymessage('p: pause', None, width // 40); pausetext.setcenter(90, height-12)
    winningtext = Displaymessage('You Win!', None, width // 5)

    # make player a sprite. for now there is only the player in the movingsprites-list
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)


    """--------------------------Game loop starts here--------------------------"""
    pause(screen, textcolor)
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
                if event.key == pygame.K_p: # pause if p is pressed
                    pause(screen, textcolor)
                    
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
        screen.blit(pausetext.getsurface(textcolor), pausetext.pos)

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
        current_room.showsolution(screen, playercolor, portalcolor, mainmenu, startxy =(player.rect.y//pixel, player.rect.x//pixel)); time.sleep(1)
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
            current_room.showsolution(screen, playercolor, portalcolor, mainmenu, fast=True); time.sleep(0.5)
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
    while count < 100:
        main()
        count += 1
    pygame.quit()
    quit()



