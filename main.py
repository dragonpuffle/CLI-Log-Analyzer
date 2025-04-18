import argparse
from file_analyzer import handlers_analysis


def parse_args_and_execute() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('logfiles', nargs='+', help='list of log files')
    parser.add_argument('--report', required=True, help='Type of the report')

    args = parser.parse_args()
    if args.report == 'handlers':
        handlers_analysis(args.logfiles)


if __name__ == '__main__':
    parse_args_and_execute()