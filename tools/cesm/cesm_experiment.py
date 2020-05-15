# CESM tool for:
# - running CESM in Galaxy

import argparse
import warnings


class GalaxyCESM ():
    def __init__(self,
                 output="metadata.txt",
                 verbose=False
                 ):

        f = open(output, 'w')
        if verbose:

            f.write("CESM running in Galaxy workflow")
            f.write("outout file: " + output)
        f.close()


if __name__ == '__main__':
        warnings.filterwarnings("ignore")
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--output',
            help='outfile for storing metadata information'
        )
        parser.add_argument(
            "-v", "--verbose",
            help="switch on verbose mode",
            action="store_true")
        args = parser.parse_args()

        p = GalaxyCESM(args.output, args.verbose)
