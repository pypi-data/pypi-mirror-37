import pandas as pd 
cellbinary1 = 'C:/Users/kuki/Desktop/cp10092018/experiment_2_cells/set 1/image1/masks_in_pickle.pickle'
boundary1 = pd.read_pickle(cellbinary1)
cellbinary2 = 'C:/Users/kuki/Desktop/cp10092018/experiment_2_cells/set 1/image2/masks_in_pickle.pickle'
boundary2 = pd.read_pickle(cellbinary2)
cellbinary3 = 'C:/Users/kuki/Desktop/cp10092018/experiment_2_cells/set 2/image3/masks_in_pickle.pickle'
boundary3 = pd.read_pickle(cellbinary3)
cellbinary4 = 'C:/Users/kuki/Desktop/cp10092018/experiment_2_cells/set 2/image4/masks_in_pickle.pickle'
boundary4 = pd.read_pickle(cellbinary4)

print len(boundary1),len(boundary2),len(boundary3),len(boundary4)