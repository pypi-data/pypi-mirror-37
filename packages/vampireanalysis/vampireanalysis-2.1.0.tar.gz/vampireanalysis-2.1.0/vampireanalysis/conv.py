import numpy as np 
def conv(u,v):
	npad = len(v)-1
	u_padded = np.pad(u, (npad//2, npad - npad//2), mode='constant')
	w = np.convolve(u_padded, v, 'valid')
	return w