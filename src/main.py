import argparse
from . import ResultsParser
from . import ui
import sys
import os
import colorama

colorama.init()  # this is necessary for window coloring


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd())
    parser.add_argument("-r", "--recursive", help="select to search recursively inside folder or not", action="store_true")
    parser.add_argument("-c", "--count", help="print metrics", action="store_true")
    parser.add_argument("-k", "--checksum", help="return 0 if checksum is valid", action="store_true")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        ui.main()

    elif args.dir:
        parser = ResultsParser.TestResultParser(folder_path=args.dir, recursive=args.recursive)
        if args.count:
            print(parser.count())
        elif args.checksum:
            print(parser.is_checksum_valid())
        else:
            print(f"{Bcolors.BOLD}{Bcolors.UNDERLINE}Total: {parser.metrics()['total']}{Bcolors.ENDC}")
            print(f"{Bcolors.OKGREEN}Pass: {parser.metrics()['pass']}{Bcolors.ENDC}")
            print(f"{Bcolors.FAIL}Fail: {parser.metrics()['fail']}{Bcolors.ENDC}")
            print(f"{Bcolors.WARNING}Skip: {parser.metrics()['skip']}{Bcolors.ENDC}")
            print(f"{Bcolors.OKCYAN}Other: {parser.metrics()['other']}{Bcolors.ENDC}")


if __name__ == "__main__":
    main()
