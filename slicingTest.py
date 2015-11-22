from numpy import *

if __name__=="__main__":
	matrix = [[(i,j) for i in range(8)] for j in range(8)]
	
	m = array(matrix)
	m = m[1:4,0:2]
	
	for row in matrix:
		print row
		
	for row in m:
		print row