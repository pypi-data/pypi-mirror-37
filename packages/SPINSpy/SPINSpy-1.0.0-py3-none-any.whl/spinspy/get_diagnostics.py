import sys
import numpy as np
from spinspy import local_data

## -----------------
## Class for diagnostics
class Diagnostic:
    """ Class for handling diagnostics.
        
        At the moment, doesn't really do anything.
    """
## ----------------


## ------------------
## Purpose: Parse diagnostics.txt and return a
##          class that contains each diagnostic
##          variable.
## Inputs:
##    fp (optional): Specifies the filename of
##                   of the diagnostics file.
## Usage: 
##    diag = spinspy.get_diagnostics()
def get_diagnostics(fp = 'diagnostics.txt'):
   
    fp = '{0:s}{1:s}'.format(local_data.path,fp)

    # Start by seeing how many lines there are
    num_lines = sum(1 for line in open(fp)) - 1

    fid = open(fp, 'r')
    
    # Read the header files
    # We assume that they are comma separated.
    curr = fid.readline()
    fields = [x.strip() for x in curr.split(',')]
    #fields = map(lambda x: x.strip(), curr.split(','))

    # Now, add the fields to the diagnostics object
    diagnostics = Diagnostic()
    diagnostics.nVar = len(fields)
    values = []
    for ii in range(len(fields)):
        values += [np.zeros(num_lines)]

    # Now loop through the rest of the lines.
    # Again, assume that values are comma separated.
    
    curr = fid.readline()
    line_num = 0
    while curr != '':
        #line = map(lambda x: float(x.strip()),curr.split(','))
        line = [float(x.strip()) for x in curr.split(',')]
        for ii in range(len(fields)):
            values[ii][line_num] = line[ii]
        line_num += 1
        curr = fid.readline()

    fid.close()

    for ii in range(len(fields)):
        setattr(diagnostics,fields[ii],values[ii])

    return diagnostics
# ------------------
