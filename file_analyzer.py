from typing import Dict, Iterator


def handlers_analysis(files: list) -> None:
    file_gens = {}
    for file in files:
        file_gens[file] = _read_file(file)
    get_total_analysis(file_gens)


def _read_file(file: str) -> Iterator[str]:
    with open(file, 'r') as f:
        for line in f:
            yield line


def get_total_analysis(file_gens: dict[str, Iterator[str]]) -> None:
    total_results = {}
    total_stats = {}
    total_request = 0
    for file_gen in file_gens.values():
        results = get_file_analysis(file_gen)
        for handler, stats in results.items():
            if handler not in total_results:
                total_results[handler] = {}
                for level, value in stats.items():
                    if level not in total_results[handler]:
                        total_results[handler][level] = value
                    else:
                        total_results[handler][level] += value
                    if level not in total_stats:
                        total_stats[level] = value
                    else:
                        total_stats[level] += value
                    total_request += value
        print('total results----------------', total_results)
        print('total requests----------------', total_request)
        print('total stats------------------', total_stats)

    print('total results----------------', total_results)
    print('total requests----------------', total_request)
    print('total stats------------------', total_stats)

def get_file_analysis(file_gen: Iterator[str]) -> Dict[str, Dict[str, int]]:
    results = {}
    for line in file_gen:
        new_line = line.split()
        if new_line[3] == 'django.request:':
            if new_line[5] not in results:
                results[new_line[5]] = {}
            if new_line[2] not in results[new_line[5]]:
                results[new_line[5]][new_line[2]] = 1
            else:
                results[new_line[5]][new_line[2]] += 1
    return results

