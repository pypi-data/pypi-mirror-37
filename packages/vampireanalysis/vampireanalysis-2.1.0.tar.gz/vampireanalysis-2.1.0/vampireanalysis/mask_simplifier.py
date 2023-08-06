import os
import numpy as np
from PIL import Image

def mask_simplifier(dirname):
	print('## mask simplifier.py')
	if dirname[-1] != '/':
		dirname = dirname + '/' 

	setnames =  [dirname + _ for _ in os.listdir(dirname) if 'set' in _]
	imagenames = []
	for setname in setnames:
		if setname[-1] != '/':
			setname = setname + '/' 
		imagename = [setname + _ for _ in os.listdir(setname) if 'image' in _]
		imagenames.append(imagename)
	imagenames = np.hstack(np.array(imagenames))
	for imagename in imagenames:
		if imagename[-1] != '/':
			imagename = imagename + '/' 
		images = [imagename + _ for _ in os.listdir(imagename) if 'tiff' in _]
		value = 1
		for image in images:
			if image == images[0]:
				addedim = np.asarray(Image.open(image))
				addedim = addedim.copy()
				addedim[addedim>0] = value
				value = value + 1
				addedim = Image.fromarray((addedim).astype('uint16'))
			else:
				im = np.asarray(Image.open(image))
				im = im.copy()
				im[im>0] = value
				value = value + 1
				addedim = Image.fromarray((addedim + im).astype('uint16'))

		# if not os.path.exists(imagename+'sum.tiff'): addedim.save(imagename+'sum.tiff')
		addedim.save(imagename+'sum.tiff')

