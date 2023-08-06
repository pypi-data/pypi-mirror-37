from __future__ import division		# as long as python 2.x is being used
import numpy as np
import spinspy as spy
from .spinspy_classes import SillyHumanError

# need to test on 2D and mapped grids 
# (on mapped grids a vector grid will not represent the topography)

## Determine simulation parameters and make grid
## Purpose:
##     - Read spins.conf if it exists
##     - Read the grid
##     - Check and add other grid parameters (such as grid spacing) into parameters object
##
## Usage:
##     x,y[,z],params = spinspy.get_paramgrid()
## ------
def get_gridparams(style='vector'):
    # read parameters and grid
    params = spy.get_params()
    gd = spy.get_grid(style=style)

    try:
        if params.mapped_grid in ['true', 'True', True]:
            gdparams = add_mapped_params(gd, params)
    except:
        if not(hasattr(params, 'mapped_grid')):
            print('Assuming grid is unmapped.')
            params.mapped_grid = 'false'
        gdparams = add_unmapped_params(gd, params) 

    return gdparams

def add_mapped_params(gd, params):

    # shorten some variables
    Nx = params.Nx
    Ny = params.Ny
    Nz = params.Nz

    # need to do something separate about reading in the grid in this case
    msg = 'Mapped Grid is not supported yet.'
    raise SillyHumanError(msg)

    return gd, params


def add_unmapped_params(gd, params):

    # read vectorized grid
    gdvec = spy.get_grid()

    # shorten some variables
    Nx = params.Nx
    Ny = params.Ny
    Nz = params.Nz

    # check dimension and parse grid based on which dimensions are used
    if len(gd) != 2 and len(gd) != 3:
        msg = 'Number of dimensions is incorrect.'
        raise SillyHumanError(msg)
    elif len(gd) == 2:
        if Nx == 1:
            y,z = gdvec
        if Ny == 1:
            x,z = gdvec
        if Nz == 1:
            x,y = gdvec
    elif len(gd) == 3:
        x,y,z = gdvec

    # could make this shorter by using a loop over x, y, and z (but will get difficult to read)
    # check if grid expansion type are in parameter object
    if params.type_x == None and Nx > 1:
        if np.abs((x[Nx/2]-x[Nx/2-1])/(x[1]-x[0])) > 2:
            params.type_x = 'NO_SLIP'
        else:
            params.type_x = 'FREE_SLIP or PERIODIC'
    if params.type_y == None and Ny > 1:
        if np.abs((y[Ny/2]-y[Ny/2-1])/(y[1]-y[0])) > 2:
            params.type_y = 'NO_SLIP'
        else:
            params.type_y = 'FREE_SLIP or PERIODIC'
    if params.type_z == None and Nz > 1:
        if np.abs((z[Nz/2]-z[Nz/2-1])/(z[1]-z[0])) > 2:
            params.type_z = 'NO_SLIP'
        else:
            params.type_z = 'FREE_SLIP or PERIODIC'

    # Add grid spacing for linear grids
    if (params.type_x != ('NO_SLIP' or 'CHEBY')) and Nx > 1 and hasattr(params, 'dx') == False:
        dx = x[1] - x[0]
        params.dx = dx
    if (params.type_y != ('NO_SLIP' or 'CHEBY')) and Ny > 1 and hasattr(params, 'dy') == False:
        dy = y[1] - y[0]
        params.dy = dy
    if (params.type_z != ('NO_SLIP' or 'CHEBY')) and Nz > 1 and hasattr(params, 'dz') == False:
        dz = z[1] - z[0]
        params.dz = dz

    # check if length of each dimension are in parameter object
    if params.Lx == None and Nx > 1:
        if params.type_x == ('NO_SLIP' or 'CHEBY'):
            params.Lx = np.abs(x[-1] - x[0])
        else:
            params.Lx = Nx*dx #which is equiavalent to np.abs(x[-1] - x[0]) + dx
    if params.Ly == None and Ny > 1:
        if params.type_y == ('NO_SLIP' or 'CHEBY'):
            params.Ly = np.abs(y[-1] - y[0])
        else:
            params.Ly = Ny*dy #np.abs(y[-1] - y[0]) + dy
    if params.Lz == None and Nz > 1:
        if params.type_z == ('NO_SLIP' or 'CHEBY'):
            params.Lz = np.abs(z[-1] - z[0])
        else:
            params.Lz = Nz*dz #np.abs(z[-1] - z[0]) + dz

    # check if bounds of each dimension are in parameters object
    # DD: what is the proper format for dimension limits? is it [x_0, x_1]? or as a numpy array?
    if params.xlim == None and Nx > 1:
        if params.type_x == ('NO_SLIP' or 'CHEBY'):
            params.xlim = [x[0], x[-1]]
        else:
            params.xlim = np.around([x[0]-dx/2, x[-1]+dx/2], 15)
    if params.ylim == None and Ny > 1:
        if params.type_y == ('NO_SLIP' or 'CHEBY'):
            params.ylim = [y[0], y[-1]]
        else:
            params.ylim = np.around([y[0]-dy/2, y[-1]+dy/2], 15)
    if params.zlim == None and Nz > 1:
        if params.type_z == ('NO_SLIP' or 'CHEBY'):
            params.zlim = [z[0], z[-1]]
        else:
            params.zlim = np.around([z[0]-dz/2, z[-1]+dz/2], 15)

    # Return everything in the proper order
    if len(gd) == 2:
        return gd[0], gd[1], params
    else:
        return gd[0], gd[1], gd[2], params
