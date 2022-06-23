import pytest
from src.ResultsParser import TestResultParser


@pytest.fixture(scope="module")
def parsed_results():
    parser = TestResultParser(folder_path="./test/results_data")
    yield parser


@pytest.mark.skip
def test_dictionary(parsed_results):
    dict, error = parsed_results.get_dictionary()
    assert error == 0


@pytest.mark.parametrize("recursive, expected_result", [
    (False, 2),
    (True, 4)
])
def test_number_of_files(parsed_results,
                         recursive,
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
