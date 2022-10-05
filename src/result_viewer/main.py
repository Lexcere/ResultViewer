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
    parser_viewer = subparsers.add_parser("viewer", help="open GUI", aliases=['v'])
    parser_show = subparsers.add_parser("show", help="show statistic about results", aliases=['s'])
    parser_report = subparsers.add_parser("report", help="generate report", aliases=['r'])

    parser_viewer.description = "Use GUI to view result and manage them"
    parser_show.description = "how statistic about results"
    parser_report.description = "Use this command to generate html report"

    parser_show.add_argument('dir', nargs='?', default=os.getcwd())
    parser_show.add_argument("-r", "--recursive", help="select to search recursively inside folder or not", action="store_true")

    parser_report.add_argument('dir', nargs='?', default=os.getcwd())
    parser_report.add_argument("-r", "--recursive", help="select to search recursively inside folder or not", action="store_true")
    # parser_report.add_argument('-o', "--output", help="select where to save report", action="store_true")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # ui.main()
        parser.print_help()

    elif args.command == "viewer" or args.command == "v":
        ui.main()

    elif args.command == "show" or args.command == "s":
        parser = ResultsParser.TestResultParser(folder_path=args.dir, recursive=args.recursive)

        if parser.count() == 0:
            print("No results found")
            return
        print("")
        total = f"{parser.metrics()['total']} Total"
        passed = f"{colorama.Fore.GREEN}{parser.metrics()['pass']} Passed"
        failed = f"{colorama.Fore.RED}{parser.metrics()['fail']} Failed"
        skipped = f"{colorama.Fore.YELLOW}{parser.metrics()['skip']} Skipped"
        other = f"{colorama.Fore.BLUE}{parser.metrics()['other']} Other{colorama.Style.RESET_ALL}"
        days = f"in {parser.get_testing_days()} day/s"
        title = f" {total}, {passed}, {failed}, {skipped}, {other} {days} "
        title = title.center(100, "=")
        print(title)
        checksum = parser.is_checksum_valid()
        if checksum == 0:
            checksum_status = f"{colorama.Fore.GREEN}OK{colorama.Style.RESET_ALL}"
        else:
            checksum_status = f"{colorama.Fore.RED}NOK{colorama.Style.RESET_ALL}"
        print(f"Checksum\t [{checksum_status}]")
        print("Comments\t [..]")
        print("Incident number\t [..]")
        # if checksum == 0:
        #     print("", end=f"{colorama.Fore.GREEN}")
        #     print(" READY FOR REPORT ".center(80, '='), end=f"{colorama.Style.RESET_ALL}\n")
        # else:
        #     print("", end=f"{colorama.Fore.RED}")
        #     print(" NOT READY FOR REPORT ".center(80, '='), end=f"{colorama.Style.RESET_ALL}\n")

    elif args.command == "report" or args.command == "r":
        parser = ResultsParser.TestResultParser(folder_path=args.dir, recursive=args.recursive)
        ReportHTML.ReportHTML(args.dir, parser.get_files())
        print(f"Report generated in {args.dir}")


if __name__ == "__main__":
    main()
