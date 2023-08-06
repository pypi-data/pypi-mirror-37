#!/usr/bin/env python

from Tkinter import *
from ttk import *
import tkFileDialog as fd
from unicodedata import normalize 
from main import *
from masksort import *
from UI_generator import *
from mask_reader_individual import *
from mask_remover import *


def makeform(root, fields):
	entries = {}
	rows= []
	for field in fields:
		row = Frame(root)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		if not field == 'Modeling' and not field =='Preprocessing' and not field =='':
			ent = Entry(row)
			if field == 'Number of Eigen shapes':
				ent.insert(0,"choose a number")
			elif field == 'Status':
				ent.insert(0,'welcome to the vampire analysis')
			elif field == 'Model name':
				ent.insert(0,'type your model name here to tag your result figures')
			else:ent.insert(0,"click search button")
			ent.pack(side=RIGHT, expand=YES, fill=X)
			entries[field] = ent
			lab = Label(row, width=22, text=field+": ", anchor='w')
			lab.pack(side=LEFT)
		else: 
			lab = Label(row, width=40, text=field, anchor='w',font=("Helvetica", 16))
			lab.pack(side=LEFT)
		rows.append(row)

	return entries,rows

def getCPdir(entries):
	# global b1
	# b1.config(text='Search Again')
	print ('you pressed search folder')
	CPoutput = StringVar()
	foldername = fd.askdirectory()
	CPoutput.set(foldername)
	CPoutput = CPoutput.get()
	entries['Cell Profiler output folder'].delete(0,END)
	entries['Cell Profiler output folder'].insert(0,CPoutput)

def getCPsubdir(entries):
	# b4.config(text='Search Again')
	print ('you pressed search subfolder')
	CPsub=StringVar()
	foldername = fd.askdirectory()
	CPsub.set(foldername)
	CPsub = CPsub.get()
	entries['Cell Profiler output subfolder'].delete(0,END)
	entries['Cell Profiler output subfolder'].insert(0,CPsub)

def build(entries,progress_bar):
	start = time.time()
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'Building a new model')
	progress_bar["maximum"] = 100
	progress_bar["value"] = 10
	progress_bar.update()
	print ('you pressed build')
	CPoutput = entries['Cell Profiler output folder'].get()
	clnum = entries['Number of Eigen shapes'].get()
	modelname = entries['Model name'].get()
	BuildModel = True
	direc = CPoutput
	if direc[-1] != '/':
		direc = direc + '/' 
	main(BuildModel,clnum,direc,entries,modelname,progress_bar)
	progress_bar["value"] = 100
	progress_bar.update()
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'New model generated!')
	end = time.time()
	print('elapsed time is ' + str(end-start) + 'seconds for build')
	print('Build Complete')
	print('interface is ready for another task')

def apply(entries,progress_bar):
	start = time.time()
	progress_bar["maximum"] = 100
	progress_bar["value"] = 10
	progress_bar.update()
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'Applying the model')
	print ('you pressed apply')
	CPoutput = entries['Cell Profiler output folder'].get()
	clnum = entries['Number of Eigen shapes'].get()
	modelname = entries['Model name'].get()
	BuildModel = False
	direc = CPoutput
	if direc[-1] != '/':
		direc = direc + '/'
	
	main(BuildModel,clnum,direc,entries,modelname,progress_bar)
	progress_bar["value"] = 100
	progress_bar.update()
	print 'apply finished'
	end = time.time()	
	print 'elapsed time is ' + str(end-start) + 'seconds for apply'
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'Model applied!')

def preprocess(entries,remove,propgen,progress_bar):
	start = time.time()
	printflag=None
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'preprocessing...')
	progress_bar["maximum"] = 100
	progress_bar["value"] = 10
	progress_bar.update()
	# global b6
	# b6.config(text='process again')
	CPsub = entries['Cell Profiler output subfolder'].get()
	print('you pressed process')
	direc = CPsub
	if direc[-1] != '/': direc = direc + '/'
	unorganized = [x for x in os.listdir(direc) if x.lower().endswith(('.tiff','.png','jpg','jpeg'))]
	if len(unorganized)>0: 
		progress_bar["value"] = 30
		progress_bar.update()
		masksort(direc,remove)
		progress_bar["value"] = 50
		progress_bar.update()
		UI_generator(direc)
		progress_bar["value"] = 80
		progress_bar.update()
		if propgen == True: print('generating property charts')
		print('compressing tiff to pickle')
		mask_reader_individual(direc,propgen) #this is get bdprop
	if remove == True: 
		setnames =  [_ for _ in os.listdir(direc) if 'set' in _]
		if len(setnames) is not 0:
			mask_remover(direc)
		else: 
			print('please choose the correct subfolder')
			printflag = 1
	if printflag is None:
		progress_bar["value"] = 100
		progress_bar.update()
		entries['Status'].delete(0,END)
		entries['Status'].insert(0,'preprocessing finished!')
		end = time.time()
		print('elapsed time is ' + str(end-start) + 'seconds for preprocess')
	else: 
		entries['Status'].delete(0,END)
		entries['Status'].insert(0,'you chose invalid subfolder')

# if __name__ == "__main__":
def interface():
	root = Tk()
	root.title("Vampire Analysis")
	fields = ('Preprocessing','Cell Profiler output subfolder','','Modeling','Cell Profiler output folder', 'Number of Eigen shapes','Model name','','','Status')
	ents,rows = makeform(root, fields)
	root.bind('<Return>', (lambda event, e=ents: fetch(e))) 
	#progress_bar
	progress_bar = Progressbar(rows[9], orient = 'horizontal',length=286, mode ='determinate')
	progress_bar.pack(side=RIGHT,padx=5,pady=5)
	#function 3
	b1 = Button(rows[1],text='Search Subfolder', width=12,command=(lambda e=ents: getCPsubdir(e)))
	b1.pack(side=RIGHT,padx=5,pady=5)
	#function 4
	remove = BooleanVar()
	propgen= BooleanVar()
	b2 = Checkbutton(rows[2],text='Remove Binary Masks',variable=remove)
	b2.pack(side=LEFT,padx=5,pady=5)
	b2_1 = Checkbutton(rows[2],text='Include Morphology Parameters',variable=propgen)
	b2_1.pack(side=LEFT,padx=5,pady=5)
	b3 = Button(rows[2],text='proceed', width=12,command=(lambda e=ents: preprocess(e,remove.get(),propgen.get(),progress_bar)))
	b3.pack(side=RIGHT,padx=5,pady=5)
	#function 1
	b4 = Button(rows[4],text='Search Folder', width=12,command=(lambda e=ents: getCPdir(e)))
	b4.pack(side=RIGHT,padx=5,pady=5)
	#function 2
	b5 = Button(rows[7],text='apply model',width=12,command=(lambda e=ents: apply(e,progress_bar)))
	b5.pack(side=RIGHT,padx=5,pady=5)
	b6 = Button(rows[7],text='build model',width=12,command=(lambda e=ents: build(e,progress_bar)))
	b6.pack(side=RIGHT,padx=5,pady=5)
	
	#terminate
	quit = Button(root, text='Quit', command=root.quit)
	quit.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()

