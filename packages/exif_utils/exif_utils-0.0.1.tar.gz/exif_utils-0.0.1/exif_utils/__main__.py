from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from exif_utils import __version__
from .date_classifier import classify
import sys


def main(*argv):
    if not argv:
        argv = list(sys.argv)

    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    # arguments to gpustat
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_directory', required=True,
                        help="Set directory path for classify")
    parser.add_argument('-v', '--version', action='version',
                        version=('exif_utils {}'.format(__version__)))
    parser.add_argument('-o', '--output_directory', default="./out",
                        help="Set output directory path for classify")
    args = parser.parse_args(argv[1:])
    input_directory = args.input_directory
    output_directory = args.output_directory
    classify(input_directory, output_directory)


if __name__ == '__main__':
    main(*sys.argv)
