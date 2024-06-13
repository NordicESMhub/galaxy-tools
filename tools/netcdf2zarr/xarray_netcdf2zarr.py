import argparse

import cftime  # noqa: F401

import xarray as xr  # noqa: I202,E402


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="input file in netCDF format")
parser.add_argument("-o", "--output", type=str, help="output in Zarr format")
args = parser.parse_args()

dset = xr.open_dataset(args.input)

dset.to_zarr(args.output)
dset.close()
