from typing import Dict, Iterator


def execute_analysis(files: list, name: str) -> None:
    if name is None:
        name = 'Analysis'

    file_gens = {}
    for file in files:
        file_gens[file] = _read_file(file)
    get_total_analysis(file_gens, name)


def _read_file(file: str) -> Iterator[str]:
    with open(file, 'r') as f:
        for line in f:
            yield line


def get_total_analysis(file_gens: dict[str, Iterator[str]], name) -> None:
    total_results = {}
    total_stats = {}
    for file_gen in file_gens.values():
        results, stats = get_file_analysis(file_gen)
        print('results----------------', results)
        print('stats------------------', stats)

    print('total results----------------', total_results)
    print('total stats------------------', total_stats)

def get_file_analysis(file_gen: Iterator[str]) -> tuple[Dict[str, Dict[str, int]], Dict[str, int]]:
    results = {}
    stats = {}
    for line in file_gen:
        new_line = line.split()
        if new_line[3] == 'django.request:':
            if new_line[5] not in results:
                results[new_line[5]] = {}
            if new_line[2] not in results[new_line[5]]:
                results[new_line[5]][new_line[2]] = 1
                stats[new_line[2]] = 1
            else:
                results[new_line[5]][new_line[2]] += 1
                stats[new_line[2]] += 1
    return results, stats

