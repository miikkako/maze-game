import pygame

game_name = "MAZEv1" # for savegame files
gamescreen_width = 960
gamescreen_height = 600 # = gamewindow's height - 100
soundfolder = ""
imagefolder = ""
defaultfont = "Arial"
biggerfontsize = 45
plusfontsize = 30
normalfontsize = 20
smallfontsize = 13
# skip loading the image if it doesn't work. Do the same for the game music in the main program
try:
	icon_image = pygame.image.load(imagefolder + 'MazeIcon1.png')
except:
	pass
