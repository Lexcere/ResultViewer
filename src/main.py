import argparse
import ResultsParser
import ui
import sys
import os
import colorama
from Plugins import ReportHTML

colorama.init()  # this is necessary for window coloring


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=False)
    parser_show = subparsers.add_parser("show", help="show help", aliases=['sh'])
    parser_report = subparsers.add_parser("report", help="report help", aliases=['rp'])

    parser_show.add_argument('dir', nargs='?', default=os.getcwd())
    parser_show.add_argument("-r", "--recursive", help="select to search recursively inside folder or not", action="store_true")
    parser_show.add_argument("-c", "--count", help="print metrics", action="store_true")
    parser_show.add_argument("-k", "--checksum", help="return 0 if checksum is valid", action="store_true")

    parser_report.add_argument('dir', nargs='?', default=os.getcwd())
    # parser_report.add_argument('-o', "--output", help="select where to save report", action="store_true")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        ui.main()

    elif args.command == "show" or args.command == "sh":
        parser = ResultsParser.TestResultParser(folder_path=args.dir, recursive=args.recursive)
        if args.count:
            print(parser.count())
        elif args.checksum:
            print(parser.is_checksum_valid())
        else:
            print(f"Total: {parser.metrics()['total']}")
            print(f"{colorama.Fore.GREEN}Pass: {parser.metrics()['pass']}")
            print(f"{colorama.Fore.RED}Fail: {parser.metrics()['fail']}")
            print(f"{colorama.Fore.YELLOW}Skip: {parser.metrics()['skip']}")
            print(f"{colorama.Fore.BLUE}Other: {parser.metrics()['other']}")

    elif args.command == "report" or args.command == "rp":
        parser = ResultsParser.TestResultParser(folder_path=args.dir, recursive=False)
        ReportHTML.ReportHTML(args.dir, parser.get_files())
        print(f"Report generated in {args.dir}")


if __name__ == "__main__":
    main()
