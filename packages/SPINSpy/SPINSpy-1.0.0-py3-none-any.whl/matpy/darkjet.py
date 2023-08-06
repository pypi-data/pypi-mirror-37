import matplotlib
import os
import sys
# Check to see if DISPLAY variable set, if not
# then use the Agg background
try:
    if not(os.environ["DISPLAY"]):
        matplotlib.use('Agg')
except:
    if not('matplotlib' in sys.modules.keys()):
        matplotlib.use('Agg')
import matplotlib.cm as colmap
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import numpy as np

## Through a jet, darkly.


## Create DarkJet
## ------
col_list = colmap.jet(range(256))
darken = np.tile((1 - 0.5/np.cosh(np.linspace(-10,10,256))).reshape((256,1)), [1,col_list.shape[1]])

col_list = col_list*darken # Apply the darkening

# Matplotlib defaults to rgba, not rgb. 
# Reset the transparency values now.
col_list[:,3] = 1.

darkjet = mplc.ListedColormap(col_list, 'darkjet', 256)
plt.register_cmap(cmap=darkjet)
## ------
