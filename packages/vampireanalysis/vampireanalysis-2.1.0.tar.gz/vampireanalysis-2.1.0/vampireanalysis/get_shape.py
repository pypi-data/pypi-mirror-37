#! C:\Python27
import numpy as np 
from scipy import stats, signal
from mode import *
from copy import deepcopy
from ginicoeff import *
from harmmean import *
import time
def get_shape(x):
	
	np.set_printoptions(precision=5,suppress=True)
	#cc = [(~np.isnan(_) and ~np.isinf(_)) for _ in x]
	#x=x[cc]
	x = x [~np.isnan(x)]
	x = x [~np.isinf(x)]
	s=np.zeros(38)
	if x.size != 0:
		s[0] = np.mean(x) # x = dist  0 = mean dist
		yk = x-s[0]
		s[1] = np.median(x)	# 1 = median dist
		xx = deepcopy(x)
		s[2] = mode(xx)
		s[3] = np.max(x)
		s[4] = np.min(x)
		s[5] = np.percentile(x,25)
		s[6] = np.percentile(x,75)
		s[7] = np.mean(x[x>s[6]])
		s[8] = np.mean(x[x<s[5]])
		s[9] = np.sum(x)
		s[10] = harmmean(x)
		s[11] = stats.trim_mean(x,0.03)
		s[12] = stats.trim_mean(x,0.05)
		s[13] = stats.trim_mean(x,0.15)
		s[14] = stats.trim_mean(x,0.25)
		s[15] = np.std(x)
		s[16] = s[15] / np.abs(s[0])
		s[17] = s[15] / np.abs(s[1])
		s[18] = s[15] / np.abs(s[2])
		s[19] = stats.skew(x)
		s[20] = stats.kurtosis(x)
		s[21] = np.mean(np.abs(yk))
		s[22] = s[3] - s[4]
		s[23] = s[6] - s[5]
		# moment, biased
		s[24] = np.sum(np.power(x,2))
		s[25] = np.sum(np.power(x,3))
		s[26] = np.mean(np.power(x,2))
		s[27] = np.mean(np.power(x,3))
		s[28] = np.mean(np.power(x,4))
		s[29] = np.mean(np.power(x,5))
		#moment, unbiased
		s[30] = np.sum(np.power(yk,2))
		s[31] = np.sum(np.power(yk,3))
		s[32] = np.mean(np.power(yk,2))
		s[33] = np.mean(np.power(yk,3))
		s[34] = np.mean(np.power(yk,4))
		s[35] = np.mean(np.power(yk,5))

		mph = s[0]
		mpd = 4
		if len(x)>3:
			locs = signal.argrelextrema(x,np.greater) #local maxima
			pks = x[locs[0]]
			s[36] = len(pks)
		else:
			s[36] = 0
		s[37] = ginicoeff(np.abs(x))
	else:
		s=np.zeros(38)
	return s
