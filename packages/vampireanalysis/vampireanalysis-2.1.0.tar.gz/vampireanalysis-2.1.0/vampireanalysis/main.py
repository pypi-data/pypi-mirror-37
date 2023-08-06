#!/usr/bin/env python

import os
import re
import time
import pandas as pd
import pickle
import random
import numpy as np
from Tkinter import *
from maskreader_new import read_selected_imageset
from bdreg import *
from pca_bdreg import *
from clusterSM import *


def recordIDX(IDX,BuildModel,cpout):
	print('#recordIDX')
	#cwd = os.path.abspath(os.path.dirname(__file__))
	#UI = pd.read_csv(cwd + '/' + 'masterUI.csv')
	UI = pd.read_csv(cpout + 'masterUI.csv')
	if BuildModel:
		on = UI.build_model
		tag = 'build_model'
	else:
		on = UI.apply_model
		tag = 'apply_model'

	setpath = UI.maskset_path
	index = np.argwhere(on).flatten()

	activeset = setpath[index].tolist()
	activeset = [x for x in activeset if  str(x) != 'nan']
	activefolder = range(len(activeset))
	for i in activefolder:
		activefolder[i] = os.path.dirname(activeset[i])
	ar = np.array(activefolder)
	arr = np.unique(ar)
	for csv in arr: 
		CellsCSV = pd.read_csv(csv + '/Cells.csv')

		idx = np.argwhere(np.isnan(CellsCSV.Location_Center_X))
		idx = idx.flatten()

		if np.isnan(CellsCSV.Location_Center_X.tolist()[-1]):
			IDX = np.append(IDX,np.nan)
		IDX = np.insert(IDX,idx,np.nan)
		IDX = np.delete(IDX,-1)
		#CellsCSV['IDX']=IDX[range(len(CellsCSV['ImageNumber']))]
		CellsCSV['IDX']=pd.Series(IDX)
		#IDX = IDX[range(len(CellsCSV['ImageNumber']))[-1]:]
		IDX = IDX[range(len(IDX))[-1]:]
		CellsCSV.to_csv(csv + '/Cells.csv')
	print('IDX recorded')
def main(BuildModel,clnum,cpout,entries,modelname,progress_bar):
	print('## main.py')
	if BuildModel:
		# if firstrun == True:
		# 	df = read_selected_imageset(cpout,BuildModel) #convert mask to pickle for choosen image set

		#picklejar = os.path.abspath(os.path.dirname(__file__))
		#picklejar = picklejar.replace('sourcecode','picklejar')
		picklejar = cpout + 'picklejar/'

		df = read_selected_imageset(cpout,BuildModel)

		VamModel = {
		"N":[],
		"bdrn":[],
		"mdd":[],
		"sdd":[],
		"pc":[],
		"latent":[],
		"clnum":[],
		"pcnum":[],
		"mincms":[],
		"testmean":[],
		"teststd":[],
		"boxcoxlambda":[],
		"C":[],
		"dendidx":[]
		}

		N = None
		progress_bar["value"] = 20
		progress_bar.update()
		bdpc, bnreg, sc, VamModel = bdreg_main(df,N,VamModel,BuildModel)
		progress_bar["value"] = 40
		progress_bar.update()
		pc , score, latent, VamModel = pca_bdreg_main(bdpc,VamModel,BuildModel)
		progress_bar["value"] = 60
		progress_bar.update()
		pcnum=None
		IDX,bdsubtype,C,VamModel = cluster_main(cpout,modelname,score,pc,bdpc,clnum,pcnum,VamModel,BuildModel)
		progress_bar["value"] = 80
		progress_bar.update()
		if os.path.exists(picklejar + modelname+ '.pickle'):
			f=open(picklejar + modelname + str(random.randint(0,100)) +'.pickle','wb')
			pickle.dump(VamModel,f)
			f.close()
		else:
			f=open(picklejar + modelname+'.pickle','wb')
			pickle.dump(VamModel,f)
			f.close()
		progress_bar["value"] = 90
		progress_bar.update()
		entries['Status'].delete(0,END)
		entries['Status'].insert(0,'created the model')
		print('Model Saved')

		result = recordIDX(IDX,BuildModel,cpout)
		progress_bar["value"] = 95
		progress_bar.update()

	else:
		df = read_selected_imageset(cpout,BuildModel)
		progress_bar["value"] = 20
		progress_bar.update()
		# picklejar = os.path.abspath(os.path.dirname(__file__))
		# picklejar = picklejar.replace('sourcecode','picklejar') +'/'
		picklejar = cpout + 'picklejar/'
		
		try:
			f=open(picklejar + modelname +'.pickle','r')
		except:
			entries['Status'].delete(0,END)
			entries['Status'].insert(0,'the model does not exist. please replace model name to the one you built')
			
		VamModel = pickle.load(f)

		N = VamModel['N'] 
		#input bdpc,score,pc in new formats
		progress_bar["value"] = 30
		progress_bar.update()
		bdpc_new, bnreg_new, sc_new, VamModel = bdreg_main(df,N,VamModel,BuildModel)
		progress_bar["value"] = 40
		progress_bar.update()
		pc_new, score_new, latent_new, VamModel = pca_bdreg_main(bdpc_new,VamModel,BuildModel)
		progress_bar["value"] = 60
		progress_bar.update()
		clnum=VamModel['clnum']
		pcnum=VamModel['pcnum']
		#pc_new goes in for sake of placing, but pc from the model is used in cluster_main
		IDX_new,bdsubtype_new,C_new,VamModel = cluster_main(cpout,modelname,score_new,pc_new,bdpc_new,clnum,pcnum,VamModel,BuildModel)
		progress_bar["value"] = 90
		progress_bar.update()
		print 'Model Applied'
		result = recordIDX(IDX_new,BuildModel,cpout)
		entries['Status'].delete(0,END)
		entries['Status'].insert(0,'applied the model')
		# build = [bdpc,bdsubtype,bnreg,C,IDX,latent,pc,sc,score]
		# new = [bdpc_new,bdsubtype_new,bnreg_new,C_new,IDX_new,latent_new,pc_new,sc_new,score_new]

		# f=open('build.pickle','wb')
		# pickle.dump(build,f)
		# f.close()

		# f=open('new.pickle','wb')
		# pickle.dump(new,f)
		# f.close()
