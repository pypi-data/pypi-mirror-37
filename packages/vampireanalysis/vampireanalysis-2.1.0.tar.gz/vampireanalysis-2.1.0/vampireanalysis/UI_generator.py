#! C:\\Python27
import pandas as pd 
import numpy as np 
import time,re,datetime
#import Tkinter, tkFileDialog
import os

def UI_generator(foldertosort):
	print('## UI_genertor.py')
	#root = Tkinter.Tk()
	#dirname = tkFileDialog.askdirectory(parent=root,initialdir='/',title='subfolder of CP default output?') + "/"
	#root.quit()
	#dirname = 'C:/Users/Kyu/Desktop/CellProfiler/CP default output folder/'
	dirname = foldertosort
	mastercsv = 'Cells.csv'
	subcsv = 'Image.csv'

	mastercsv = pd.read_csv(dirname + mastercsv)
	no_sets = np.add(range(max(mastercsv.Metadata_SetNumber)),1)

	subcsv = pd.read_csv(dirname + subcsv)
	folderpath = subcsv.PathName_Cells
	cell_count = subcsv.Count_Cells.tolist()
	idx = pd.factorize(folderpath)[0]
	group_counts = np.empty((len(no_sets),1)).tolist()
	for index, obj in enumerate(cell_count):
		group_counts[idx[index]].append(obj)
	group_counts = [int(np.sum(_)) for _ in group_counts]
	folderpath = np.unique(folderpath)

	foldername = [_ for _ in os.listdir(dirname) if 'set' in _]
	foldername = np.core.defchararray.add(dirname,foldername)

	d = {'date':[datetime.datetime.now()]*len(no_sets),'set number':no_sets, \
	'cell count':group_counts,'raw_imageset_path':folderpath,
	'build_model':np.zeros(len(no_sets)),'apply_model':np.zeros(len(no_sets)), \
	'ctrl/exp?':['NaN']*len(no_sets),'maskset_path':foldername}

	df = pd.DataFrame(data=d)
	df.to_csv(dirname+ 'UI.csv', index=False)

	d = {'date':[],'set number':[], \
	'cell count':[],'raw_imageset_path':[],
	'build_model':[],'apply_model':[], \
	'ctrl/exp?':[],'maskset_path':[]}
	df = pd.DataFrame(data=d)
	masterUIpath = os.path.abspath(os.path.join(foldertosort,'..')) + '/masterUI.csv'
	if not os.path.isfile(masterUIpath):
		df.to_csv(masterUIpath,index=False)
