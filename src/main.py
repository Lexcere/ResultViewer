import argparse
import ResultsParser
import ui
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recursive", help="select to search recursively inside folder or not", action="store_true")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        ui.main()

    if args.recursive:
        print("recu")


if __name__ == "__main__":
    main()
