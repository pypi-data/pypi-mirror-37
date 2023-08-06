## Provides classes for the SPINSPY functions.

## Create some error classes
## ------
class Error(Exception):
    """ Base class for exceptions in this module. """
    pass

class SillyHumanError(Error):
    """ Exception raised when the human does something silly.
        
        Attributes:
            msg -- explanation of the error"""

    def __init__(self, msg):
        self.msg = msg
        print(msg)
##------

## Create parameters class
## ------
class Params():
    
    def __init__(self):
        # Initialize the required ones.
        
        # Number of dimensions
        self.nd = None

        # Number of gridpoints
        self.Nx = None
        self.Ny = None
        self.Nz = None
    
        # Domain lengths
        self.Lx = None
        self.Ly = None
        self.Lz = None
    
        # Domain limits [min, max]
        self.xlim = None
        self.ylim = None
        self.zlim = None
    
        # Grid types
        self.type_x = None
        self.type_y = None
        self.type_z = None
    
    def display(self):
        
        print('{0}-dimensional simulation:'.format(self.nd))
        ds = ['x','y','z']
        for ind in range(3):
            if self.nd > ind:
        
                print('  {0}-Dimension:'.format(ds[ind]))
            
                if getattr(self,'N'+ds[ind]) == None:
                    print('    Number of Points: n/a')
                else:
                    print('    Number of Points: {0:d}'.format(getattr(self,'N'+ds[ind])))
            
                if getattr(self,'L'+ds[ind]) == None:
                    print('    Length of Domain: n/a')
                else:
                    print('    Length of Domain: {0:1.3g}'.format(getattr(self,'L'+ds[ind])))
            
                if getattr(self,ds[ind]+'lim') == None:
                    print('    Bounds of Domain: n/a')
                else:
                    print('    Bounds of Domain: {0:1.3g}, {1:1.3g}'.format(\
                                    getattr(self,ds[ind]+'lim')[0],\
                                    getattr(self,ds[ind]+'lim')[1]))
            
                if hasattr(self, 'type_'+ds[ind]):
                    print('    Type: {0:s}'.format(getattr(self, 'type_'+ds[ind])))

        # Print everything else
        param_str = 'Other parameters:'
        setng_str = 'Settings:'
        
        dontdo = ['Nx','Lx','xlim','type_x',\
                  'Ny','Ly','ylim','type_y',\
                  'Nz','Lz','zlim','type_z',\
                  'nd'];
        attrs = dir(self)
        for attr in attrs:
            if not(attr in dontdo) and \
               not(attr[0:2]=='__') and \
               not(type(getattr(self,attr)) is type(getattr(self,'display'))):
                
                # If the value is a string, it's a setting.
                if type(getattr(self,attr)) is type('str'):
                    setng_str = setng_str + \
                               '\n  {0:s}: {1:s}'.format(attr,getattr(self,attr))

                # Otherwise, it's a parameter.
                else:
                    param_str = param_str + \
                        '\n  {0:s}: {1:g}'.format(attr,getattr(self,attr))
        print(param_str)
        print(setng_str)
## ------
