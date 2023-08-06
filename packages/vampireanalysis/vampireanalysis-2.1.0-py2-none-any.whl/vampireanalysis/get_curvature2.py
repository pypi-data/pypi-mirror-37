from __future__ import division
import time
import numpy as np 
import scipy as sp 
from fspecial import *
from conv import *
from polyfitw import *
from copy import deepcopy

def get_curvature2(bd,wsz2=None):
	
	if wsz2 == None: wsz2=5 #wsz2 value matters
	pn = len(bd.T[0]) #pn is too big now
	wsz= 1
	bd = bd + np.random.randn(bd.shape[0],bd.shape[1]) * 0.001
	N = int(round(pn/2))
	gx = fspecial((1,11),1)

	u = np.concatenate((bd.T[1], bd.T[1][1:]))
	v = gx.flatten()
	xconv = conv(u,v)

	u = np.concatenate((bd.T[0], bd.T[0][1:]))
	v = gx.flatten()
	yconv = conv(u,v)

	xconv = xconv[wsz-1:-wsz]

	yconv = yconv[wsz-1:-wsz]

	n=2

	cva = np.zeros((pn,1))
	for k in range(pn):
		kid = 2 * wsz2 + (k+1) 
		t = range(kid-wsz2, kid+wsz2+1)
		ind = np.subtract(t,1)
		t = t[::-1] #reverse 
		t = np.asarray(t)
		xtmp = xconv[ind] 
		ytmp = yconv[ind]
		px = polyfitw(t,xtmp,n)
		py = polyfitw(t,ytmp,n)

		pxp = np.polyder(px)
		pxpp = np.polyder(pxp)
		pyp = np.polyder(py)
		pypp = np.polyder(pyp)

		xp = np.polyval(pxp,kid)
		yp = np.polyval(pyp,kid)
		xpp = np.polyval(pxpp,kid)
		ypp = np.polyval(pypp,kid)


		if kid>pn: kid = kid -pn
		cva[kid-1] = (xp*ypp-yp*xpp)/np.power((xp*xp+yp*yp),1.5)

	return cva