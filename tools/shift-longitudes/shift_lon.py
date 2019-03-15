#!/usr/bin/env python3
#
import argparse
from pathlib import Path
import os
import warnings
import xarray as xr

if __name__ == '__main__':
  warnings.filterwarnings("ignore")
  parser = argparse.ArgumentParser()
  parser.add_argument(
        'input',
        help='input filename with geographical coordinates (netCDF format)'
  )

  parser.add_argument(
        'lon',
        help='name of the variable for longitudes'
  )

  parser.add_argument(
        'output',
        help='output filename to store resulting image (png format)'
  )
  parser.add_argument("-v", "--verbose", help="switch on verbose mode",
                    action="store_true")
  args = parser.parse_args()
  
  dset = xr.open_dataset(args.input, decode_cf=False)

  if dset[args.lon].max()>180.:
    for i in range(dset[args.lon].size):
        if dset[args.lon].values[i]>180.:
            dset[args.lon].values[i] = dset[args.lon].values[i] - 360.

  dset.sortby(args.lon).to_netcdf(args.output)
  if args.verbose:
      print("Longitudes shifted to -180. and 180.")
