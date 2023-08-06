"""
Entry point.

References
----------
https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

Notes
-----
Use config.csv to set analysis parameters.
"""

import os
import argparse
from hrf_opt.hrf_opt_main import hrf_opt_run

# Get path of this file:
strDir = os.path.dirname(os.path.abspath(__file__))


def main():
    """hrf_opt entry point."""

    # Create parser object:
    objParser = argparse.ArgumentParser()

    # Add argument to namespace - config file path:
    objParser.add_argument('-config',
                           metavar='config.csv',
                           help='Absolute file path of config file with \
                                 parameters for hrf optimization. \
                                 Ignored if in testing mode.'
                           )

    # Namespace object containign arguments and values:
    objNspc = objParser.parse_args()

    # Get path of config file from argument parser:
    strCsvCnfg = objNspc.config

    # Print info if no config argument is provided.
    if strCsvCnfg is None:
        print('Please provide the file path to a config file, e.g.:')
        print('   hrf_opt -config /path/to/my_config_file.csv')

    else:

        # Call to main function, to invoke hrf_opt analysis:
        hrf_opt_run(strCsvCnfg)


if __name__ == "__main__":
    main()
