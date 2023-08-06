import pytest
from dcim import main

# all command line entry points as specified in setup.py are called here


def run():
    main.run()


def test():
    pytest.main()
