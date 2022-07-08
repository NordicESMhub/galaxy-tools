#!/usr/bin/env python3
#
#
# usage: climate_stripes.py [-h] [--cmap CMAP]
#                           [--output OUTPUT]
#                           [--xname XNAME]
#                           [--format_plot FORMAT_PLOT]
#                           [--format_date FORMAT_DATE]
#                           [--title TITLE]
#                           [--nxsplit NXSPLIT]
#                          input varname
#
# positional arguments:
#   input                 input filename with timeseries (tabular format)
#   varname               column name to use for plotting (case sensitive)
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --cmap CMAP           Specify which colormap to use for plotting
#   --output OUTPUT       output filename to store resulting image (png format)
#   --xname XNAME         column name to use for x-axis
#   --format_plot FORMAT_PLOT
#                         format for plotting dates on the x-axis
#   --format_date FORMAT_DATE
#                         format for input date/time column
#   --title TITLE         plot title
#   --nxsplit NXSPLIT     number of ticks on the x-axis
#

import argparse
import warnings

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt   # noqa: I202,E402

import numpy as np  # noqa: I202,E402

import pandas as pd  # noqa: I202,E402


class Stripes ():
    def __init__(self, input, valname, cmap, output, xname="",
                 date_format='%Y%m',
                 plot_format='%Y',
                 nxsplit=10,
                 title=""):
        self.input = input
        self.valname = valname
        self.xname = xname
        if not nxsplit:
            self.nxsplit = 10
        else:
            self.nxsplit = nxsplit
        if not cmap:
            self.cmap = 'RdBu_r'
        else:
            self.cmap = cmap
        if not output:
            self.output = "stripes.png"
        else:
            self.output = output
        self.title = title
        if not date_format:
            self.format = '%Y%m'
        else:
            self.format = date_format.replace('X', '%')
        if not plot_format:
            self.plot_format = self.format
        else:
            self.plot_format = plot_format.replace('X', '%')

    def read_data(self):
        if self.xname is not None:
            self.data = pd.read_csv(self.input, sep='\t', index_col=self.xname, infer_datetime_format=True)
        else:
            self.data = pd.read_csv(self.input, sep='\t')

    def create_stripes(self):
        data = np.zeros((2, self.data[self.valname].shape[0]), dtype='float')
        data[:] = np.NaN
        data[0, :] = self.data[self.valname]
        data[1, :] = self.data[self.valname]
        fig = plt.figure(figsize=(10, 2))
        ax = plt.subplot(111)
        plt.pcolor(data, cmap=self.cmap,
                   vmin=self.data[self.valname].quantile(q=0.01),
                   vmax=self.data[self.valname].quantile(q=0.99))
        if self.title:
            plt.title(self.title)
        if self.xname is not None:
            nrange = self.data.index.values
            date_list = pd.to_datetime(nrange[::int(self.nxsplit)], format=self.format)
            date_list = [i.strftime(self.plot_format) for i in date_list]
            ax.set_xticks(np.arange(0, len(nrange), int(self.nxsplit)), date_list)
            ax.xaxis.set_tick_params(rotation=45)
        else:
            ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        fig.savefig(self.output)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        help='input filename with geographical coordinates (netCDF format)'
    )
    parser.add_argument(
        'varname',
        help='column name to use for plotting (case sensitive)'
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
        '--xname',
        help='column name to use for x-axis'
    )
    parser.add_argument(
        '--format_plot',
        help='format for plotting dates on the x-axis'
    )
    parser.add_argument(
        '--format_date',
        help='format for input date/time column (default is Month d, yyyy)'
    )
    parser.add_argument(
        '--title',
        help='plot title'
    )
    parser.add_argument(
        '--nxsplit',
        help='number of ticks on the x-axis'
    )
    args = parser.parse_args()
    stripes = Stripes(args.input, args.varname, args.cmap, args.output,
                      xname=args.xname, date_format=args.format_date,
                      plot_format=args.format_plot, title=args.title,
                      nxsplit=args.nxsplit)
    stripes.read_data()
    stripes.create_stripes()
