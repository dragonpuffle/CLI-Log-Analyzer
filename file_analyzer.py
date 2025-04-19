import os
import re
from typing import Dict, Iterator

HANDLER_PATTERN = re.compile(r'(/\S+)')


def get_analysis(files: list, report_type: str) -> None:
    file_gens = {}
    for file in files:
        if not os.path.isfile(file):
            raise FileNotFoundError(file)
        file_gens[file] = _read_file(file)
    if report_type == 'handlers':
        handlers_analysis(file_gens)

    # if you would like to add new report type:
    # if report_type == 'another':
    #     another_analysis(file_gens)


def _read_file(file: str) -> Iterator[str]:
    with open(file, 'r') as f:
        for line in f:
            yield line


def handlers_analysis(file_gens: Dict[str, Iterator[str]]) -> None:
    total_results, total_stats, total_request = handlers_analysis_for_all_files(file_gens)
    handlers_output(total_results, total_stats, total_request)


def handlers_analysis_for_all_files(file_gens: Dict[str, Iterator[str]]) -> tuple[
    list[tuple[str, Dict[str, int]]], Dict[str, int], int]:
    total_results = {}
    total_stats = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0}
    total_request = 0
    for file_gen in file_gens.values():
        results = handlers_analysis_for_one_file(file_gen)
        for handler, stats in results.items():
            if handler not in total_results:
                total_results[handler] = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0}
            for level, value in stats.items():
                total_results[handler][level] = total_results[handler].get(level, 0) + value
                total_stats[level] = total_stats.get(level, 0) + value
                total_request += value
    sorted_results = sorted(total_results.items(), key=lambda x: x[0])

    return sorted_results, total_stats, total_request


def handlers_analysis_for_one_file(file_gen: Iterator[str]) -> Dict[str, Dict[str, int]]:
    results = {}
    for line in file_gen:
        match = HANDLER_PATTERN.search(line)
        if match:
            handler = match.group(1)
            new_line = line.split()
            if len(new_line) < 5:
                continue
            level = new_line[2]
            if handler not in results:
                results[handler] = {}
            if level not in results[handler]:
                results[handler][level] = 1
            else:
                results[handler][level] += 1
    return results


def handlers_output(total_results: list[tuple[str, Dict[str, int]]], total_stats: Dict[str, int],
                    total_requests: int) -> None:
    print('Total requests:', total_requests, '\n')

    print(f"{'HANDLER':40}|{'DEBUG':15}|{'INFO':15}|{'WARNING':15}|{'ERROR':15}|{'CRITICAL':15}|")
    for result in total_results:
        handler, stats = result[0], result[1]
        print(
            f"{handler:40}|{stats['DEBUG']:15}|{stats['INFO']:15}|{stats['WARNING']:15}|{stats['ERROR']:15}|{stats['CRITICAL']:15}|")
    print(
        f"{'...':40}|{total_stats['DEBUG']:15}|{total_stats['INFO']:15}|{total_stats['WARNING']:15}|{total_stats['ERROR']:15}|{total_stats['CRITICAL']:15}|")
