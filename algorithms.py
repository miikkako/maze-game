import pygame, random
from koodi import *
from gameinfo import *

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
        if self.parent == None: # yes
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
        return coordinates #[y, x]

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
        (wallcolor, screencolor, textcolor, playercolor, portalcolor) = mainmenu.selected_theme

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
            screen.blit(Displaymessage('f:fast  s:slow', defaultfont, 30).getsurface(textcolor),(10, gamescreen_height+30)); pygame.display.update()
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
                    if mainmenu.showcreation and event.key == pygame.K_f:
                        show = False
                    if mainmenu.showcreation and event.key == pygame.K_s:
                        for c in openedcoordinates:
                            pygame.draw.rect(screen, screencolor, (c[1]*pixel,c[0]*pixel,pixel,pixel))
                        show = True
                if event.type == pygame.KEYUP and event.key == pygame.K_p:
                    if event.key == pygame.K_p:
                        done = True; notfound = True # if p is pressed, stop creating the maze and put the finishpoint to the recent smallest
                        
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

