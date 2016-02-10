from koodi import IO
from io import StringIO

def testload():
	loadgame = IO(playername='miikka')
	input_file = StringIO()
	input_file.write('MAZEv1 savefile\n')
	input_file.write('#Date=5.7.2001\n')
	input_file.write('#y=12\n')
	input_file.write('#x=11\n')
	input_file.write('#levels=2\n')
	input_file.write('#currentlevel=1\n')
	input_file.write('#currentcoordinates=0,4\n') # y,x
	input_file.write('#currentscore=90\n')
	input_file.write('#Matrix 1\n')
	input_file.write('0,0,0,0,0,1,0,0,0,0,1\n')
	input_file.write('1,1,0,1,1,1,0,1,1,1,1\n')
	input_file.write('1,1,0,1,1,1,0,0,0,0,1\n')
	input_file.write('1,1,0,1,1,1,0,1,1,0,1\n')
	input_file.write('1,1,0,1,1,1,0,0,0,0,1\n')
	input_file.write('1,1,1,1,1,1,1,1,1,1,1\n')
	input_file.write('1,0,0,0,1,2,6,6,0,0,1\n')
	input_file.write('0,1,1,1,1,1,1,6,1,1,1\n')
	input_file.write('1,0,0,1,1,1,1,6,1,1,1\n')
	input_file.write('1,1,1,0,1,1,1,6,1,1,1\n')
	input_file.write('0,0,0,1,1,1,1,3,1,1,1\n')
	input_file.write('1,1,1,1,1,1,1,1,1,1,1\n')
	input_file.write('#Matrix 2\n')
	input_file.write('0,0,0,0,0,1,0,0,0,0,1\n')
	input_file.write('1,1,0,1,1,1,0,1,1,1,1\n')
	input_file.write('1,1,0,1,1,1,0,0,0,0,1\n')
	input_file.write('1,1,0,1,1,1,0,1,1,0,1\n')
	input_file.write('1,1,0,1,1,1,0,0,0,0,1\n')
	input_file.write('1,1,1,1,1,1,1,1,1,1,1\n')
	input_file.write('1,0,0,0,1,3,6,6,0,0,1\n')
	input_file.write('0,1,1,1,1,1,1,6,1,1,1\n')
	input_file.write('1,0,0,1,1,1,1,6,1,1,1\n')
	input_file.write('1,1,1,0,1,1,1,6,1,1,1\n')
	input_file.write('0,0,0,1,1,1,1,2,1,1,1\n')
	input_file.write('1,1,1,1,1,1,1,1,1,1,1\n')
	input_file.seek(0, 0)

	loadgame.read_savegame()


	# for a in range(loadgame.levels):
	# 	for j in range(loadgame.y):
	# 		print(loadgame.matrixes[a][j])

def testloadrealfile():
	loadgame = IO(playername='miikka')
	if not loadgame.read_savegame():
		print('nothing happened')
	return loadgame



def testwrite():
	matrixes = [[[1,1,1],[1,1,1],[1,0,1]],[[1,1,1],[3,6,2],[1,1,1]]]
	gameIO = IO(playername = 'miikka', levels = 2, y = 3, x = 3, current_room_no = 2, score = 50, currentcoord = [1,2])
	gameIO.matrixes = matrixes
	if not gameIO.write_loadgame():
		print('file already exists')



def main():
	testwrite()
	loadgame = testloadrealfile()
	#testload()

	print(loadgame.x, loadgame.y, loadgame.levels)
	print(loadgame.matrixes)

main()




