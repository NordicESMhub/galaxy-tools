# Retrieve Copernicus ECV
# (Essential climate Variables)

import argparse
import os
import shutil
import tarfile
import tempfile
import warnings

import cdsapi


class ECV ():
    def __init__(self, archive, variable, product_type, year,
                 month, time_aggregation, area, format, output,
                 climate_reference_period=None, verbose=False
                 ):
        self.archive = archive
        self.variable = variable.split(',')
        self.climate_reference_period = climate_reference_period
        if product_type == '':
            self.product_type = 'climatology'
        else:
            self.product_type = product_type
        if year != '' and year is not None:
            self.year = year.split(',')
        else:
            self.year = None
        if month == '' or month is None:
            self.month = '01'
        else:
            self.month = month.split(',')
        if time_aggregation == '':
            self.time_aggregation = '1_month_mean'
        else:
            self.time_aggregation = time_aggregation
        if area == '' or area is None:
            self.area = 'global'
        else:
            self.area = area

        if format == '':
            self.format = 'tgz'
        else:
            self.format = format
        if output == '':
            self.outputfile = "donwload." + self.format
        else:
            self.outputfile = output
        self.verbose = verbose
        if verbose:
            print("archive: ", self.archive)
            print("variable: ", self.variable)
            print("year: ", self.year)
            print("month: ", self.month)
        self.cdsapi = cdsapi.Client()

    def retrieve(self):

        if self.verbose:
            print(self.archive)
            print('variable', self.variable)
            print('year', self.year)
            print('month', self.month)
            print('origin', 'era5')
            print('area', self.area)
            print('format', self.format)
            print('product_type', self.product_type)
            print('time_aggregation', self.time_aggregation)
            print('climate_reference_period',
                  self.climate_reference_period)
            print(self.outputfile)
        if self.climate_reference_period is None:
            self.cdsapi.retrieve(
                self.archive, {
                    'variable': self.variable,
                    'year': self.year,
                    'month': self.month,
                    'origin': 'era5',
                    'area': self.area,
                    'format': self.format,
                    'product_type': self.product_type,
                    'time_aggregation': self.time_aggregation,
                },
                self.outputfile)
        elif self.year is None:
            self.cdsapi.retrieve(
                self.archive, {
                    'variable': self.variable,
                    'climate_reference_period':
                    self.climate_reference_period,
                    'month': self.month,
                    'origin': 'era5',
                    'format': self.format,
                    'product_type': self.product_type,
                    'time_aggregation': self.time_aggregation,
                },
                self.outputfile)
        else:
            self.cdsapi.retrieve(
                self.archive, {
                    'variable': self.variable,
                    'climate_reference_period':
                    self.climate_reference_period,
                    'year': self.year,
                    'month': self.month,
                    'origin': 'era5',
                    'format': self.format,
                    'product_type': self.product_type,
                    'time_aggregation': self.time_aggregation,
                },
                self.outputfile)

    def checktar(self):
        is_grib = False
        with open(self.outputfile, 'rb') as ofile:
            is_grib = ofile.read(4)
        if (is_grib == b'GRIB' and self.format == 'tgz'):
            # we create a tgz to be consistent
            newfilename = tempfile.NamedTemporaryFile()
            gribfile = os.path.basename(newfilename.name) + '.grib'
            shutil.copyfile(self.outputfile, gribfile)
            newfilename.close()
            tar = tarfile.open(self.outputfile, 'w:gz')
            tar.add(gribfile)
            tar.close()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser()

    remove_apikey = False
    current_pwd = os.environ['HOME']
    if 'GALAXY_COPERNICUS_CDSAPIRC_KEY' in os.environ and \
       not os.path.isfile('.cdsapirc'):
        print('GALAXY_COPERNICUS_CDSAPIRC_KEY ')
        with open(".cdsapirc", "w+") as apikey:
            apikey.write("url: https://cds.climate.copernicus.eu/api/v2\n")
            apikey.write("key: " + os.environ['GALAXY_COPERNICUS_CDSAPIRC_KEY'])
            remove_apikey = True

    parser.add_argument(
        'archive',
        help='Archive name'
    )
    parser.add_argument(
        'variable',
        help='Specify which variable to retrieve'
    )
    parser.add_argument(
        '--product_type',
        help='Type of product (climatology or anomaly)'
    )
    parser.add_argument(
        '--year',
        help='Year(s) to retrieve.'
    )
    parser.add_argument(
        '--month',
        help='List of months to retrieve.'
    )
    parser.add_argument(
        '--time_aggregation',
        help='Time range over which data is aggregated (monthly/yearly).'
    )
    parser.add_argument(
        '--area',
        help='Desired sub-area to extract (North/West/South/East)'
    )
    parser.add_argument(
        '--climate_reference_period',
        help='Climate reference period (default is 1981-2010)'
    )
    parser.add_argument(
        '--format',
        help='Output file format (GRIB or netCDF or tgz)'
    )
    parser.add_argument(
        '--output',
        help='output filename'
    )
    parser.add_argument(
        "-v", "--verbose",
        help="switch on verbose mode",
        action="store_true")
    args = parser.parse_args()

    p = ECV(args.archive, args.variable, args.product_type,
            args.year, args.month, args.time_aggregation, args.area,
            args.format, args.output, args.climate_reference_period, args.verbose)
    p.retrieve()
    p.checktar()
    # remove api key file if it was created
    if remove_apikey and os.getcwd() == current_pwd:
        os.remove(os.path.join(current_pwd, '.cdsapirc'))
