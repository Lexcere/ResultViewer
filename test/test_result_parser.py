from src.ResultsParser import TestResultParser


def test_number_of_files():
    parser = TestResultParser(path="./test/results_data")
    assert parser.count() == 5
