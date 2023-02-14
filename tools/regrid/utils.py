"""
Code taken from https://github.com/tom-andersson/icenet-paper and slightly 
adjusted to fit the galaxy interface. 

"""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'icenet'))  # if using jupyter kernel
import config
import itertools
import requests
import json
import time
import re
import xarray as xr
import iris
import imageio


def assignLatLonCoordSystem(cube):
    ''' Assign coordinate system to iris cube to allow regridding. '''

    cube.coord('latitude').coord_system = iris.coord_systems.GeogCS(6367470.0)
    cube.coord('longitude').coord_system = iris.coord_systems.GeogCS(6367470.0)

    return cube


def fix_near_real_time_era5_func(latlon_path):

    '''
    Near-real-time ERA5 data is classed as a different dataset called 'ERA5T'.
    This results in a spurious 'expver' dimension. This method detects
    whether that dim is present and removes it, concatenating into one array
    '''

    ds = xr.open_dataarray(latlon_path)

    if len(ds.data.shape) == 4:
        print('Fixing spurious ERA5 "expver dimension for {}.'.format(latlon_path))

        arr = xr.open_dataarray(latlon_path).data
        arr = ds.data
        # Expver 1 (ERA5)
        era5_months = ~np.isnan(arr[:, 0, :, :]).all(axis=(1, 2))

        # Expver 2 (ERA5T - near real time)
        era5t_months = ~np.isnan(arr[:, 1, :, :]).all(axis=(1, 2))

        ds = xr.concat((ds[era5_months, 0, :], ds[era5t_months, 1, :]), dim='time')

        ds = ds.reset_coords('expver', drop=True)

        os.remove(latlon_path)
        ds.load().to_netcdf(latlon_path)

