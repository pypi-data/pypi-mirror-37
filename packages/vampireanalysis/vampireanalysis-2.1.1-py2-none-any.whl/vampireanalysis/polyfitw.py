import numpy as np 
import time
def polyfitw(x,y,order):
	rr = len(x)
	AA = np.zeros((rr,order+1))
	count = 0
	for k in range(order+1)[::-1]:
		AA.T[count] = np.power(x,k)
		count = count + 1

	x,resid,rank,s = np.linalg.lstsq(AA,y,rcond=None)
	p = x.T
	return p