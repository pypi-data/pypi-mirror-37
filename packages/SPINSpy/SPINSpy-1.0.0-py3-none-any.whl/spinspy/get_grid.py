from .reader import reader
from .get_params import get_params
from .isdim import isdim
import os
from spinspy import local_data

## Read in the grid as either vectors (1)
## or full matrices (2).
## (1) x,y[,z] = spinspy.grid()
## (2) x,y[,z] = spinspy.grid(style='full')
## ------
def get_grid(style='vector'):
    
    grid_data = get_params()

    if os.path.realpath(local_data.path) == local_data.grid_path:
        # We've already loaded it, so just return the stored value
        if grid_data.nd == 3:
            x = local_data.x.copy()
            y = local_data.y.copy()
            z = local_data.z.copy()
        elif grid_data.nd == 2:
            if isdim('x'):
                X1 = local_data.x.copy()
                if isdim('y'):
                    X2 = local_data.y.copy()
                else:
                    X2 = local_data.z.copy()
            else:
                X1 = local_data.y.copy()
                X2 = local_data.z.copy()
    else:
        if grid_data.nd == 2:
            sel1 = ([0,-1],0)
            sel2 = (0,[0,-1])
            sel3 = ([0,-1], [0,-1])
            if style == 'vector':
                if isdim('x'):
                    X1 = reader('x', *sel1)
                    if isdim('y'):
                        X2 = reader('y', *sel2)
                    elif isdim('z'):
                        X2 = reader('z', *sel2)
                else:
                    X1 = reader('y', *sel1)
                    X2 = reader('z', *sel2)
            elif style == 'full':
                if isdim('x'):
                    X1 = reader('x',*sel3)
                    if isdim('y'):
                        X2 = reader('y', *sel3)
                    elif isdim('z'):
                        X2 = reader('z', *sel3)
                else:
                    X1 = reader('y', *sel3)
                    X2 = reader('z', *sel3)
            if isdim('x'):
                x = X1
                if isdim('y'):
                    y = X2
                else:
                    z = X2
            else:
                y = X1
                z = X2
        elif grid_data.nd == 3:
            if style == 'vector':
                x = reader('x', [0,-1],0,0)
                y = reader('y', 0,[0,-1],0)
                z = reader('z', 0,0,[0,-1])
            elif style == 'full':
                x = reader('x', [0,-1],[0,-1],[0,-1])
                y = reader('y', [0,-1],[0,-1],[0,-1])
                z = reader('z', [0,-1],[0,-1],[0,-1])

        # Store path and grids for future reference
        local_data.grid_path = os.path.realpath(local_data.path)
        if isdim('x'):
            local_data.x = x.copy()
        if isdim('y'):
            local_data.y = y.copy()
        if isdim('z'):
            local_data.z = z.copy()

    if grid_data.nd == 2:
        return X1,X2
    elif grid_data.nd == 3:
        return x,y,z
## ------
