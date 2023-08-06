import numpy as np

## Find the index of list that is closest to value
## assumes list is monotonic and is a vector (though it will work otherwise)
## ------
def nearestindex(list, value):
    index = np.argmin(np.abs(list-value))
    return index
