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

# This creates a circular, perceptually uniform colormap
# The code was stolen from the matplotlib/numpy/scipy 
# presentation (matplotlib 2.0 presentation)


# Number of points
N = 256

# Constant lightness
Jp = 75*np.ones(N)

# Constant saturation, varying hue
radius = 30
theta  = np.linspace(0, 2*np.pi, N)
ap     = radius*np.sin(theta)
bp     = radius*np.cos(theta)

Jpapbp = np.column_stack((Jp, ap, bp))

from colorspacious import cspace_convert
rgb = cspace_convert(Jpapbp, "CAM02-UCS", "sRGB1")


# Matplotlib defaults to rgba, not rgb. 
# Reset the transparency values now.
col_list[:,3] = 1.

circular_map = mplc.ListedColormap(col_list, 'circular_map', 256)
plt.register_cmap(cmap=circular_map)
## ------
