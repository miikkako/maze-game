import pygame
import random
import math
import time

BLACK = (0, 0, 0)
WHITE = (230, 230, 230)
VANILLA = (200, 200, 200)
GREEN = (21, 150, 27)
PURPLE = (199, 103, 201)
BRIGHTPURPLE = (255, 0, 255)
BLUE = (26, 31, 190)
BRIGHTBLUE = (0, 0, 255)
RED = (180, 32, 61)
BRIGHTRED = (255, 0, 0)
GREEN2 = (41, 210, 28)  # MM = main menu
GREEN3 = (5, 239, 5)
RED2 = (161, 39, 50)
RED3 = (240, 4, 6)
"""(R, G, B) from 0 to 255 ---move these to another file?"""


class Mainmenu(object):

    """This class is called from Startscreen and passed to main. Contains all the user input game information"""

    def __init__(self):
        self.playername = ""

        self.startscreen()

    def pressbutton(self, screen, event, mouse, message, x, y, width, height, icrect, ictext, acrect, actext):
        # draw buttons
        # draw.rect parameters: (x, y, width, height)
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
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

        # screen
        screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('Labyrinth main menu')
        intro = 0
        while intro == 0: # intro=1: play new game, intro=2: load game
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()
                    quit()

                screen.fill(WHITE)
                screen.blit(welcometext.getsurface(BLACK), [220, 30])
                screen.blit(welcometext2.getsurface(BLACK), [300, 80])

                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                if self.pressbutton(screen,event, mouse, playbuttontext, 600, 450, 180, 120, RED, PURPLE, VANILLA, GREEN):
                    intro = 1

                

            pygame.display.update()
            clock.tick(60)


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


class Wall(pygame.sprite.Sprite):

    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Player(pygame.sprite.Sprite):

    # speed vector
    change_x = 0
    change_y = 0
    speed = 0
    name = ""
    """parameter speed and needs to be put manually in main() for now"""

    def __init__(self, x, y):

        # Call the parent's constructor
        super().__init__()

        # Set height and width. Player's color is WHITE
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def move(self, walls):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Room(object):

    wall_list = None

    def __init__(self):

        self.wall_list = pygame.sprite.Group()


class Level(Room):

    """This creates all the walls in a level using random library"""
    # number of wall-squares

    def __init__(self, wallnumber):

        # Make the walls
        Room.__init__(self)

        # Random colors for inner and outer walls for the Level
        outerwallcolor = random.choice([BLUE, GREEN, RED, PURPLE])
        innerwallcolor = outerwallcolor
        while(innerwallcolor == outerwallcolor):
            innerwallcolor = random.choice([BLUE, GREEN, RED, PURPLE])

        # These are lists of outer and inner walls. Each is in the form [x, y, width,
        # height]
        # Loop through the list. Create the wall, add it to the list
        outerwalls = [[0, 0, 20, 250, outerwallcolor],
                      [0, 350, 20, 250, outerwallcolor],
                      [780, 0, 20, 250, outerwallcolor],
                      [780, 350, 20, 250, outerwallcolor],
                      [20, 0, 760, 20, outerwallcolor],
                      [20, 580, 760, 20, outerwallcolor]]
        for item in outerwalls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        # same for innerwalls (squares)
        for i in range(random.randint(wallnumber - wallnumber // 2, wallnumber)):
            innerwalls = [
                [random.randint(1, 38) * 20, random.randint(1, 28) * 20, 20, 20, innerwallcolor]]
            for item in innerwalls:
                wall = Wall(item[0], item[1], item[2], item[3], item[4])
                self.wall_list.add(wall)


def main():
    """ Main Program """
    # Call this function so the Pygame library can initialize itself
    pygame.init()
    clock = pygame.time.Clock()

    """ Get all the inforation from startscreen, startscreen can also calls loadgame """

    mainmenu = Mainmenu()

    
    """ Game begins here """
    width = 800
    height = 700
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption('Labyrinth')

    """ ---This section needs to be moved to the mainmenu object--- """
    rooms = []

    # set walls, this needs to be moved to wall
    number_of_walls = 200
    for i in range(4):
        room = Level(number_of_walls)
        rooms.append(room)
        number_of_walls += 100

    # Create the player object
    player = Player(width // 40, width // 40)
    player.speed = width // 40
    player.name = 'miikka'

    # define some displaytexts
    mainwindowtext = Displaymessage('MAZE', None, width // 16)
    mainwindowtext2 = Displaymessage(
        'Try to find your way out!', None, width // 23)

    playernametext = Displaymessage(
        'Player: ' + player.name, None, width // 27)
    points = 0
    scoretext = Displaymessage(
        'Score: ' + str(points), None, width // 27)
    winningtext = Displaymessage('You Win!', None, width // 10)

    # insert data to gameinfo
    gameinfo = Gameinfo(player, rooms, 0)

    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    current_room_no = 0
    """ ---This section needs to be moved to startscreen--- """

    current_room = rooms[current_room_no]
    done = False

    while not done:

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

        # move according to event
        player.move(current_room.wall_list)

        if player.rect.x < -15:
            if current_room_no != 0:
                current_room_no -= 1
                current_room = rooms[current_room_no]
                player.rect.x = 780
            elif current_room_no == 0:
                player.rect.x = 0

        if player.rect.x > 801:
            if current_room_no == len(rooms) - 1:
                # print something? play sounds?
                screen.blit(winningtext.getsurface(WHITE), [290, 300])
                pygame.display.update()
                time.sleep(3)
                done = True
            else:
                current_room_no += 1
                current_room = rooms[current_room_no]
                player.rect.x = 0

        # draw screen
        screen.fill(BLACK)
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)
        screen.blit(mainwindowtext.getsurface(WHITE), [345, 620])
        screen.blit(mainwindowtext2.getsurface(WHITE), [270, 670])
        screen.blit(scoretext.getsurface(WHITE), [20, 630])
        screen.blit(playernametext.getsurface(WHITE), [600, 630])

        pygame.display.update()

        # calculate gamescore
        points -= 0.1
        scoretext.text = 'Score: ' + str(int(points))

        clock.tick(60)

        # store game information in every loop so that the game
        # can be saved anytime
        gameinfo.updateparameters(player, rooms, current_room_no)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
