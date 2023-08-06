import numpy as np 
def flatten_2d(array):
	#a = [['a','b'],['c']]
	a = array
	c = []
	for i in range(len(a)):
		b = [_ for _ in a[i]]
		c = np.hstack([c,b])
	return c