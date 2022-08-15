import argparse
import ResultsParser
import ui
import sys
import os


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
