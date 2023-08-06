import os
from spinspy import local_data

def isdim(dim):
    if os.path.isfile('{0:s}{1:s}grid'.format(local_data.path,dim)):
        return True
    else:
        return False
