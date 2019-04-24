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


class PsyPlot ():
    def __init__(self, input, proj, varname, cmap, output,
                 verbose=False
                 ):
        self.input = input
        self.proj = proj
        self.varname = varname
        self.cmap = cmap
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
            print("output: ", self.output)

    def plot(self):
        if self.cmap is None and self.proj is None:
            print("op1")
            psy.plot.mapplot(self.input, name=self.varname,
                             clabel='{desc}')
        elif self.proj is None or self.proj == '':
            print("op2")
            psy.plot.mapplot(self.input, name=self.varname,
                             cmap=self.cmap, clabel='{desc}')
        elif self.cmap is None or self.cmap == '':
            print("op3")
            psy.plot.mapplot(self.input, name=self.varname,
                             projection=self.proj,
                             clabel='{desc}')
        else:
            print("op4")
            psy.plot.mapplot(self.input, name=self.varname,
                             cmap=self.cmap,
                             projection=self.proj,
                             clabel='{desc}')

        pyplot.savefig(self.output)


def psymap_plot(input, proj, varname, cmap, output, verbose):
    """Generate plot from input filename"""

    p = PsyPlot(input, proj, varname, cmap, output, verbose)
    p.plot()


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
        "-v", "--verbose",
        help="switch on verbose mode",
        action="store_true")
    args = parser.parse_args()

    psymap_plot(args.input, args.proj, args.varname, args.cmap,
                args.output, args.verbose)
