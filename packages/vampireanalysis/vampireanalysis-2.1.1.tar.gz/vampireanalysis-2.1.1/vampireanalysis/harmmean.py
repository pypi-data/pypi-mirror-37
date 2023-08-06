import numpy as np 
def harmmean(x):
	inv = 1. / x
	result = len(x)/np.sum(inv)
	return result