#! C:\Python27
import numpy as np 
import time

def ginicoeff(In,dim = 1,nosamplecorr = False):
	np.set_printoptions(precision=5,suppress=True)
	if len(In.shape) == 1 :
		dim = 1
	IDXnan = np.isnan(In)

	'''
	IDX = np.any(In[:] < 0, dim-1) or np.sum(~IDXnan,dim-1) < 2
	if dim == 1:
		In.T[IDX] = 0
	else:
		In[IDX] = 0
	'''

	In[IDXnan] = 0 #replace NaNs
	In = np.sort(In, dim-1)
	freq = np.flip(np.cumsum(np.flip(~IDXnan,dim-1),dim-1),dim-1)
	if dim == 1:
		totNum = freq[0]
	else:
		totNum = freq.T[0]
	tot = np.sum(In,dim-1)
	coeff = totNum+1-2*( np.divide(np.sum(np.multiply(In,freq),dim-1),tot) )

	if nosamplecorr:
		coeff = np.divide(coeff, totNum)
	else:
		coeff = np.divide(coeff,(totNum-1))

	return coeff