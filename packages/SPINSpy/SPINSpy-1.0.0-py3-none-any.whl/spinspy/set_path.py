from spinspy import local_data

## Specify the baseline path for the SPINSpy
## functions. In particular, data will be read
## from path/u.0, etc. 
def set_path(path):
    
    if path[-1] != '/':
        path += '/'

    local_data.path = path
