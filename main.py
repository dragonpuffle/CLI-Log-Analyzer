import argparse
from file_analyzer import get_analysis


def parse_args_and_execute() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('logfiles', nargs='+', help='list of log files')
    parser.add_argument('--report', default='handlers', help='Type of the report')

    args = parser.parse_args()
    get_analysis(args.logfiles, args.report)


if __name__ == '__main__':
    parse_args_and_execute()