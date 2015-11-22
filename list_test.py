

if __name__=="__main__":
	list = [[i*j for i in range(8)] for j in range(8)]
	for row in list:
		print row
		
	print list.index(49)