# SPINSPY
#   This module contains functions that are
#   designed to handle SPINS-type outputs.
#   The provided functions are listed below,
#   along with basic usage information.

__author__ = ["Ben Storer <bastorer@uwaterloo.ca>",
              "David Deepwell, <ddeepwel@uwaterloo.ca>"]
__date__   = "23rd of October, 2018"

# Create a Params instance for storing information
from .spinspy_classes import Params
local_data = Params()
local_data.path = './'
local_data.grid_path = ''
local_data.conf_path = ''
local_data.x = None
local_data.y = None
local_data.z = None
local_data.disc_order = 'xzy'

# Initialization file for package.
# Read in the defined functions. Not strictly necessary,
# but makes usage nicer. i.e. now we can use
# spinspy.grid() instead of spinspy.grid.grid().
from .get_params import get_params
from .get_grid import get_grid
from .get_gridparams import get_gridparams
from .reader import reader
from .get_diagnostics import get_diagnostics
from .set_path import set_path
from .nearestindex import nearestindex

# Define what happens when someone uses
# from matpy import *
__all__ = ["spinspy_classes", "get_params", "get_grid", "get_gridparams", "reader", "get_diagnostics", "set_path","nearestindex"]
