#!/usr/bin/env python3
#
#
# usage: psymap_simple.py [-h] [--proj PROJ]
#                              [--cmap CMAP]
#                              [--output OUTPUT]
#                              [-l]
#                              [-v]
#                              input varname
#
# positional arguments:
#  input            input filename with geographical coordinates (netCDF
#                   format)
#  varname          Specify which variable to plot (case sensitive)
#
# optional arguments:
#  -h, --help       show this help message and exit
#  -l, --logscale   log scale the data
#  --proj PROJ      Specify the projection on which we draw
#  --cmap CMAP      Specify which colormap to use for plotting
#  --output OUTPUT  output filename to store resulting image (png format)
#  --time TIMES     time index from the file for multiple plots ("0 1 2 3")
#  --nrow NROW      number of rows for multiple plot grid
#  --ncol NCOL      number of columns for multiple plot grid
#  --format         date format such as %Y (for year) %B (for month), etc.
#  --title          plot or subplot title
#  -v, --verbose    switch on verbose mode
#

import argparse
import warnings
from pathlib import Path
import math
import xarray

import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot  # noqa: I202,E402

import psyplot
import psyplot.project as psy  # noqa: I202,E402
from psyplot import rcParams   # noqa: I202,E402


class PsyPlot ():
    def __init__(self, input, varname, output=None, logscale=False, cmap=None,
                 proj=None, verbose=False, time=None, nrow=None, ncol=None,
                 format=None, title=None):
        self.input = input
                
        self.varname = varname
        if proj is None or proj == "":
            self.proj = "cyl"
        else:
            self.proj = proj
        self.cmap = cmap if cmap is not None else "jet"
        self.time = time if time is not None else []
        self.ncol = int(ncol) if ncol is not None else int(1)
        self.nrow = int(nrow) if nrow is not None else int(1)

        # Open dataset
        ds = xarray.open_dataset(input)[varname]
        minv = math.log2(ds.data.min())
        maxv = math.log2(ds.data.max())
        if title is not None:
            self.title = title 
        else:
            self.title = ds.long_name
            if len(self.title) > 60:
                self.title = ds.standard_name
        del ds

        if logscale:
            # Check that data range is sufficient for log scaling
            if maxv < (minv * (10.0 ** 2.0)):
                print("Not possible to log scale, switching to linear scale")
                self.bounds = None
            else:
                self.bounds = ['log', 2]
        else:
            self.bounds = None
        if format is None:
            self.format = ""
        else:
            self.format = "%B %e, %Y"
        if output is None:
            self.output = Path(input).stem + '.png'
        else:
            self.output = output
        if verbose:
            print("input: ", self.input)
            print("proj: ", self.proj)
            print("varname: ", self.varname)
            print("cmap: ", self.cmap)
            print("time: ", self.time)
            print("ncol: ", self.ncol)
            print("nrow: ", self.nrow)
            print("title: ", self.title)
            print("date format: ", self.format)
            print("logscale: ",self.bounds)
            print("output: ", self.output)

    def plot(self):
        clabel = '{desc}'
        if self.title and self.format:
            title = self.title + "\n" + self.format
        elif not self.title and self.format:
            title = self.format
        elif self.title and not self.format:
            title = self.title
            clabel = self.title
            
        # Plot with chosen options
        if self.bounds is None:
            psy.plot.mapplot(self.input, name=self.varname,
                             cmap=self.cmap,
                             projection=self.proj,
                             title=title,
                             clabel=clabel)
        else:
            psy.plot.mapplot(self.input, name=self.varname,
                             cmap=self.cmap, bounds = self.bounds,
                             projection=self.proj,
                             title=title,
                             clabel=clabel)


        pyplot.savefig(self.output)

    def multiple_plot(self):
        if not self.format:
            self.format = "%B %e, %Y"

        if not self.title:
            title = self.format
        else:
            title = self.title + "\n" + self.format
             
        mpl.rcParams['figure.figsize'] = [20, 8]
        mpl.rcParams.update({'font.size': 8})
        rcParams.update({'plotter.maps.grid_labelsize': 8.0})

        # Plot using options
        if self.bounds is None:
            m = psy.plot.mapplot(self.input, name=self.varname,
                                 cmap=self.cmap,
                                 projection=self.proj,
                                 ax=(self.nrow, self.ncol),
                                 time=self.time, sort=['time'],
                                 title=title,
                                 clabel='{desc}')
        else:
            m = psy.plot.mapplot(self.input, name=self.varname,
                                 cmap=self.cmap, bounds=self.bounds,
                                 projection=self.proj,
                                 ax=(self.nrow, self.ncol),
                                 time=self.time, sort=['time'],
                                 title=title,
                                 clabel='{desc}')

        m.share(keys='bounds')

        pyplot.savefig(self.output)


def psymap_plot(input, proj, varname, logscale, cmap, output, verbose, time,
                nrow, ncol, format, title):
    """Generate plot from input filename"""

    p = PsyPlot(input, varname, output, logscale, cmap, proj, verbose, time,
                nrow, ncol, format, title)

    if len(time) == 0:
        p.plot()
    else:
        p.multiple_plot()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        help='input filename with geographical coordinates (netCDF format)'
    )

    parser.add_argument(
        '--proj',
        help='Specify the projection on which we draw'
    )
    parser.add_argument(
        'varname',
        help='Specify which variable to plot (case sensitive)'
    )
    parser.add_argument(
        "--logscale",
        help='Plot the log scaled data'
    )
    parser.add_argument(
        '--cmap',
        help='Specify which colormap to use for plotting'
    )
    parser.add_argument(
        '--output',
        help='output filename to store resulting image (png format)'
    )
    parser.add_argument(
        '--time',
        help='list of times to plot for multiple plots'
    )
    parser.add_argument(
        '--format',
        help='format for date/time (default is Month d, yyyy)'
    )
    parser.add_argument(
        '--title',
        help='plot title'
    )
    parser.add_argument(
        '--ncol',
        help='number of columns for multiple plots'
    )
    parser.add_argument(
        '--nrow',
        help='number of rows for multiple plots'
    )
    parser.add_argument(
        "-v", "--verbose",
        help="switch on verbose mode",
        action="store_true")
    args = parser.parse_args()

    if args.time is None:
        time = []
    else:
        time = list(map(int, args.time.split(",")))
        
    if args.logscale == 'no':
        logscale = False
    else:
        logscale = True

    psymap_plot(args.input, args.proj, args.varname, logscale, args.cmap,
                args.output, args.verbose, time,
                args.nrow, args.ncol, args.format, args.title)
