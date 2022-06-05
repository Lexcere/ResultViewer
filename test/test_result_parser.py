from src.ResultsParser import TestResultParser


def test_number_of_files():
    parser = TestResultParser()
    assert parser.count() == 5
