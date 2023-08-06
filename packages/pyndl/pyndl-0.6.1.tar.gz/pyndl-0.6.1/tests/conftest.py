'''
Configuration for py.test-3.

'''


def pytest_addoption(parser):
    """
    adds custom option to the pytest parser
    """
    parser.addoption("--runslow", action="store_true",
                     help="run slow tests")
