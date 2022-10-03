import logging

import pytest
from src.result_viewer.ResultsParser import TestResultParser, match_file_name
import os


@pytest.fixture(scope="module")
def parsed_results():
    parser = TestResultParser(folder_path="./test/results_data")
    yield parser


@pytest.mark.skip
def test_dictionary(parsed_results):
    dict, error = parsed_results.get_dictionary()
    assert error == 0


@pytest.mark.parametrize("recursive, expected_result", [
    pytest.param(False, 2, id="not recursive"),
    pytest.param(True, 4, id="recursive")
])
def test_number_of_files(recursive,
                         expected_result):
    parser = TestResultParser(folder_path="./test/results_data", recursive=recursive)
    assert parser.count() == expected_result


def test_metrics_total(parsed_results):
    assert parsed_results.metrics()["total"] == 2


def test_metrics_pass(parsed_results):
    assert parsed_results.metrics()["pass"] == 1


def test_metrics_skip(parsed_results):
    assert parsed_results.metrics()["skip"] == 1


def test_checksum_valid(parsed_results):
    assert parsed_results.is_checksum_valid() == 0


def test_get_files():
    parser = TestResultParser(folder_path="./test/results_data", recursive=False)
    for _file in parser.get_files():
        logging.info(_file)
        assert os.path.isfile(_file)


@pytest.mark.parametrize("filename, fail", [
    ["2020-04-06-19-04-08-LMBPC0588.txt", False],
    ["2020-04-06-19-04-08-LMBPC0588.tx", True],
    ["020-04-06-19-04-08-LMBPC0588.tx", True],
    ["wrong_name_good_extension.txt", True],
    ["wrong_name_wrong_extension.tx", True],
])
def test_match_file_name(filename, fail):
    if fail:
        assert not match_file_name(filename)
    else:
        assert match_file_name(filename)
