import pygame
import os
from time import gmtime, strftime
from koodi import *
from gameinfo import *


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



