import argparse
from . import ResultsParser
from . import ui
import sys
import os


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd())
    parser.add_argument("-r", "--recursive", help="select to search recursively inside folder or not", action="store_true")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        ui.main()

    else:
        parser = ResultsParser.TestResultParser(folder_path=args.dir, recursive=args.recursive)
        print(parser.metrics())


if __name__ == "__main__":
    main()
