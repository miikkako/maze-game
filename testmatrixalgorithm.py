from koodi import Mazematrix


def main():
	
	height = 30; width = 40
	mazematrix = Mazematrix([width, height])
	mazematrix.makeprimsmaze()
	print('\nalgorithm ran')
	#print(mazematrix.matrix[1][1])
	mazematrix.printselfmatrix()
	print('\nnow we add solution')
	mazematrix.addAstarsolution()
	mazematrix.printselfmatrix()

main()
