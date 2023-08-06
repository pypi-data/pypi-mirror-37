import numpy as np

## CHEB computes the Chebyshev differentiation matrix
## ------
## Dx,x = cheb(Nx, kwargs)
## ------
#    matrix on Nx+1 points (i.e. Nx intervals)
#    Dx = differentiation matrix
#    x = Chebyshev grid on [-1,1]
##
#  kwargs:
#     xlims = [a,b] # Desired limits on x
#           a,b real numbers
#           default = [-1,1]
def cheb(N, xlims=[-1,1]):
    if N == 0:
        D = 0
        x = 1
    else:
        theta = np.pi*np.arange(0,N+1)/N
        x = np.cos(theta.reshape([N+1,1]))
        c = np.ravel(np.vstack([2, np.ones([N-1,1]), 2])) \
            *(-1)**np.ravel(np.arange(0,N+1))
        c = c.reshape(c.shape[0],1)
        X = np.tile(x,(1,N+1))
        dX = X-(X.conj().transpose())
        D  = (c*(1/c).conj().transpose())/(dX+(np.eye(N+1)))   # off-diagonal entries
        D  = D - np.diag(np.sum(D,1))   # diagonal entries

    # Now implement xlims
    x = xlims[0] + (xlims[1]-xlims[0])*(x + 1.)/2.
    D = D*2./(xlims[1]-xlims[0])

    return D,x
## ------
