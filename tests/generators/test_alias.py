import os
import sys
import random

sys.path.insert(0, os.path.abspath('src'))

from eeyore.generators import Alias

def test_alias_generation():
    random.seed(100)
    identifier = Alias(size=20).get_alias()
    assert identifier == 'eooyfwmxlnqzdrdcxoibv', identifier
