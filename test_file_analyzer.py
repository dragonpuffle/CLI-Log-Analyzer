import os
import pytest
from file_analyzer import get_analysis, handlers_analysis, handlers_analysis_for_all_files, \
    handlers_analysis_for_one_file, _read_file


def test_log_files_exist():
    files = ['logs/app1.log', 'logs/app2.log', 'logs/app3.log']
    for path in files:
        assert os.path.isfile(path), f'Файл не найден: {path}'


def test_handlers_analysis_for_one_file():
    file = 'logs/app1.log'
    gen = _read_file(file)
    test_result = handlers_analysis_for_one_file(gen)

    assert test_result['/admin/dashboard/']['INFO'] == 6
    assert test_result['/admin/dashboard/']['ERROR'] == 2
    assert test_result['/api/v1/users/']['INFO'] == 4
    assert 'ERROR' not in test_result['/api/v1/users/']


def test_handlers_analysis_for_all_files(capsys):
    files = ['logs/app1.log', 'logs/app2.log', 'logs/app3.log']
    file_gens = {}

    for file in files:
        file_gens[file] = _read_file(file)

    total_results, total_stats, total_request = handlers_analysis_for_all_files(file_gens)

    assert total_request == 188

    assert total_stats['INFO'] == 148
    assert total_stats['ERROR'] == 40
    assert total_stats['DEBUG'] == 0

    assert total_results[0][0] == '/admin/dashboard/'
    assert total_results[4][0] == '/api/v1/checkout/'
    assert total_results[-1][0] == '/api/v1/users/'

    assert total_results[0][1]['INFO'] == 13
    assert total_results[4][1]['ERROR'] == 4
    assert total_results[-1][1]['CRITICAL'] == 0


def test_get_analysis():
    error_files = ['logs/ap10.log']
    report_type = 'handlers'

    with pytest.raises(FileNotFoundError):
        get_analysis(error_files, report_type)


def test_handlers_analysis(capsys):
    files = ['logs/app1.log', 'logs/app2.log', 'logs/app3.log']

    file_gens = {}
    for file in files:
        file_gens[file] = _read_file(file)

    handlers_analysis(file_gens)

    result = capsys.readouterr().out

    assert "Total requests: 188" in result
    assert '/api/v1/auth/login/' in result
