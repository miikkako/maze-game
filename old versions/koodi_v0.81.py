import pygame, random, math, time, eztext, handmade30x40matrixes
from colors import *
from Mazematrix import *; from Mainmenu import *; from Displaymessage import *
from Player import *; from Room_Level_Wall import *
clock = pygame.time.Clock()


class Inputbox(object): 
    """docstring for Inputbox"""
    def __init__(self, arg):
        self.arg = arg


class Pressbutton(object):
    """docstring for Pressbutton"""
    def __init__(self, arg):
        self.arg = arg

           
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


def main():
    """ Game loop and things here """
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
        screen.blit(Displaymessage('you can only play a ready made 30x40 matrix for now', None, 40).getsurface(BRIGHTRED), [20,330])
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

    
    

    # define some displaytextsb 
    mainwindowtext = Displaymessage('MAZE', None, width // 16)
    mainwindowtext2 = Displaymessage('Try to find your way out to the green portal', None, width // 23)
    playernametext = Displaymessage('Player: ' + player.name, None, width // 27)
    scoretext = Displaymessage('Score: ' + str(points), None, width // 27)
    winningtext = Displaymessage('You Win!', None, width // 5)
    leveltext = Displaymessage('Level ' + str(current_room_no + 1), None, width // 27)
    savequittext = Displaymessage('q: save & quit', None, width // 38)
    portaltext = Displaymessage('Space: enter portal', None, width // 38)
    giveuptext = Displaymessage('j: give up', None, width // 38)

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
                    done = 3 # give up
                    
            # check if on portal and if space is pressed
            if player.rect.x == current_room.portal_xy[0] and player.rect.y == current_room.portal_xy[1]:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    points += 100
                    if current_room_no == len(rooms) - 1: # game won
                        done == 2
                    else:
                        current_room_no += 1
                        current_room = rooms[current_room_no]
                        player.set_xy(current_room)
                        
        # move according to event
        player.move(current_room.wall_list)

        # check if invisible portal happening 
        player.check_and_jump_to_invisibleportal(screen, current_room, movingsprites)


        # draw screen
        screen.fill(BLACK)

        # draw portal
        pygame.draw.rect(screen, BRIGHTGREEN, (current_room.portal_xy[0] - 2, current_room.portal_xy[1] - 2, 24, 24))

        # draw player and walls
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        # draw texts
        leveltext.text = 'Level ' + str(current_room_no + 1)
        screen.blit(mainwindowtext.getsurface(WHITE), [345, 620])
        screen.blit(mainwindowtext2.getsurface(WHITE), [270, 670])
        screen.blit(scoretext.getsurface(WHITE), [20, 650])
        screen.blit(playernametext.getsurface(WHITE), [600, 630])
        screen.blit(leveltext.getsurface(WHITE), [20, 610])
        screen.blit(savequittext.getsurface(WHITE), [160, 605])
        screen.blit(portaltext.getsurface(WHITE), [160, 625])
        screen.blit(giveuptext.getsurface(WHITE), [160, 645])
        

        pygame.display.update()

        # calculate gamescore
        points -= 0.05
        scoretext.text = 'Score: ' + str(int(points))

        clock.tick(60)

        # store game information in every loop so that the game
        # can be saved anytime
        gameinfo.updateparameters(player, rooms, current_room_no)



    if done == 2:
        scoretext.text = 'Your Score is amazing: ' + str(int(points)); scoretext.size = width // 10
        screen.blit(scoretext.getsurface(BRIGHTPURPLE),[20, 100])
        screen.blit(winningtext.getsurface(BRIGHTBLUE), [160, 300]); pygame.display.update(); time.sleep(0.5)
        screen.blit(winningtext.getsurface(BRIGHTRED), [160, 300]); pygame.display.update(); time.sleep(0.5)
        screen.blit(winningtext.getsurface(BRIGHTBLUE), [160, 300]); pygame.display.update(); time.sleep(0.5)
        screen.blit(winningtext.getsurface(BRIGHTRED), [160, 300]); pygame.display.update(); time.sleep(0.5)
        screen.blit(winningtext.getsurface(BRIGHTBLUE), [160, 300]); pygame.display.update(); time.sleep(0.5)
        screen.blit(winningtext.getsurface(BRIGHTRED), [160, 300]); pygame.display.update(); time.sleep(0.5)
    elif done == 3:
        current_room.showsolution(screen)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
