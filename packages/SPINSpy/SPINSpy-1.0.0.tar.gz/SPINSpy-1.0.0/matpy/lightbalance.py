import numpy as np
import cmocean
import matplotlib.cm as colmap
import matplotlib.colors as mplc
import matplotlib.pyplot as plt

num_pts = 256
cmap = cmocean.cm.balance

ref_r = cmap(0.5)[0]
ref_g = cmap(0.5)[1]
ref_b = cmap(0.5)[2]

col_list = np.zeros((num_pts,4))

vals = np.linspace(0, 1, num_pts)

for ind in range(num_pts):

    p = vals[ind]

    r = cmap(p)[0] / ref_r
    g = cmap(p)[1] / ref_g
    b = cmap(p)[2] / ref_b
    a = cmap(p)[3]

    col_list[ind,0] = min(1., max(0., r))
    col_list[ind,1] = min(1., max(0., g))
    col_list[ind,2] = min(1., max(0., b))
    col_list[ind,3] = 1. # fix alpha = 1

    #if (ind == 127) or (ind == 128) :
    #    col_list[ind, 3] = 0.1 # set white to transparent for fun

lightbalance = mplc.ListedColormap(col_list, 'lightbalance', num_pts)
plt.register_cmap(cmap=lightbalance)
