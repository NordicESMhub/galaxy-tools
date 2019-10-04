#!/usr/bin/env python3
#
#
# usage: psymap_simple.py [-h] [--proj PROJ]
#                              [--cmap CMAP]
#                              [--output OUTPUT]
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
#  --proj PROJ      Specify the projection on which we draw
#  --cmap CMAP      Specify which colormap to use for plotting
#  --output OUTPUT  output filename to store resulting image (png format)
#  -v, --verbose    switch on verbose mode
#

import argparse
import warnings
from pathlib import Path

import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot  # noqa: I202,E402

import psyplot.project as psy  # noqa: I202,E402
from psyplot import rcParams   # noqa: I202,E402


class PsyPlot ():
    def __init__(self, input, proj, varname, cmap, output, verbose=False,
                 time=[], nrow=1, ncol=1, format="%B %e, %Y",
                 title=""):
        self.input = input
        self.proj = proj
        self.varname = varname
        self.cmap = cmap
        self.time = time
        if format is None:
            self.format = ""
        else:
            self.format = format
        if title is None:
            self.title = ""
        else:
            self.title = title
        if ncol is None:
            self.ncol = 1
        else:
            self.ncol = int(ncol)
        if nrow is None:
            self.nrow = 1
        else:
            self.nrow = int(nrow)
        if output is None:
            self.output = Path(input).stem + '.png'
        else:
            self.output = output
        self.verbose = verbose
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
            print("output: ", self.output)

    def plot(self):
        if self.title == "" and self.format == "":
            title = '%(long_name)s'
        elif self.title == "" and self.format != "":
            title = self.format
        elif self.title != "" and self.format == "":
            title = self.title
        else:
            title = self.title + "\n" + self.format

        if self.cmap is None and self.proj is None:
            print("op1")
            psy.plot.mapplot(self.input, name=self.varname,
                             title=title,
                             clabel='{desc}')
        elif (self.proj is None or self.proj == ''):
            print("op2")
            psy.plot.mapplot(self.input, name=self.varname,
                             title=title,
                             cmap=self.cmap, clabel='{desc}')
        elif self.cmap is None or self.cmap == '':
            print("op3")
            psy.plot.mapplot(self.input, name=self.varname,
                             projection=self.proj,
                             title=title,
                             clabel='{desc}')
        else:
            print("op4")
            psy.plot.mapplot(self.input, name=self.varname,
                             cmap=self.cmap,
                             projection=self.proj,
                             title=title,
                             clabel='{desc}')

        pyplot.savefig(self.output)

    def multiple_plot(self):
        if self.format == "":
            self.format = "%B %e, %Y"

        if self.title == "":
            title = self.format
        else:
            title = self.title + "\n" + self.format
        mpl.rcParams['figure.figsize'] = [40,8]
        mpl.rcParams.update({'font.size': 8})
        rcParams.update({'plotter.maps.grid_labelsize': 8.0})
        if self.cmap is None and self.proj is None:
            print("op1 time")
            m = psy.plot.mapplot(self.input, name=self.varname,
                             title=title,
                             ax=(self.nrow,self.ncol),
                             time=self.time, sort=['time'],
                             clabel='{desc}')
            m.share(keys = 'bounds')
        elif (self.proj is None or self.proj == ''):
            print("op2 time")
            m = psy.plot.mapplot(self.input, name=self.varname,
                             title=title,
                             ax=(self.nrow,self.ncol),
                             time=self.time, sort=['time'],
                             cmap=self.cmap, clabel='{desc}')
            m.share(keys = 'bounds')
        elif self.cmap is None or self.cmap == '':
            print("op3 time")
            m = psy.plot.mapplot(self.input, name=self.varname,
                             projection=self.proj,
                             ax=(self.nrow,self.ncol),
                             time=self.time, sort=['time'],
                             title=title,
                             clabel='{desc}')
            m.share(keys = 'bounds')
        else:
            print("op4 time")
            m = psy.plot.mapplot(self.input, name=self.varname,
                             cmap=self.cmap,
                             projection=self.proj,
                             ax=(self.nrow, self.ncol),
                             time=self.time, sort=['time'],
                             title=title,
                             clabel='{desc}')
            m.share(keys = 'bounds')

        pyplot.savefig(self.output)


def psymap_plot(input, proj, varname, cmap, output, verbose, time,
                nrow, ncol, format, title):
    """Generate plot from input filename"""

    p = PsyPlot(input, proj, varname, cmap, output, verbose, time,
                nrow, ncol, format, title)
    print("time", time)
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
        help='format for date/time (default is %B %e, %Y)'
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
        time = list(map(int, args.time.split(" ")))
    psymap_plot(args.input, args.proj, args.varname, args.cmap,
                args.output, args.verbose,  time ,
                args.nrow, args.ncol, args.format, args.title)
