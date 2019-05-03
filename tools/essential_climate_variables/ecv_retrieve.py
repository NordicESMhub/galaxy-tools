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
                 verbose=False
                 ):
        self.archive = archive
        self.variable = variable.split(',')
        if product_type == '':
            self.product_type = 'climatology'
        else:
            self.product_type = product_type
        if year == '':
            self.year = '2019'
        else:
            self.year = year.split(',')
        if month == '':
            self.month = '01'
        else:
            self.month = month.split(',')
        if time_aggregation == '':
            self.time_aggregation = '1_month'
        else:
            self.time_aggregation = time_aggregation
        self.area = area
        if format == '':
            self.format = 'tgz'
        else:
            self.format = format
        if output == '':
            self.outputfile = "donwload." + self.format
        else:
            self.outputfile = output
        if verbose:
            print("archive: ", self.archive)
            print("variable: ", self.variable)
            print("year: ", self.year)
            print("month: ", self.month)
        self.cdsapi = cdsapi.Client()

    def retrieve(self):

        self.cdsapi.retrieve(
            self.archive, {
                'variable': self.variable,
                'year': self.year,
                'month': self.month,
                'area': self.area,
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
        with open(".cdsapirc", "w+") as apikey:
            apikey.write("url: https://cds.climate.copernicus.eu/api/v2\n")
            apikey.write(
                  "key: " + os.environ['GALAXY_COPERNICUS_CDSAPIRC_KEY'])
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
            args.format, args.output, args.verbose)
    p.retrieve()
    p.checktar()
    # remove api key file if it was created
    if remove_apikey and os.getcwd() == current_pwd:
        os.remove(os.path.join(current_pwd, '.cdsapirc'))
