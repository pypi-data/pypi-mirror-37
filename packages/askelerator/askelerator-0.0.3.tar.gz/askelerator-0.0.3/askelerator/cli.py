"""
askelerator CLI runtime
"""
import os
import sys
from pathlib import Path

from . import generator

ASKELERATOR_DIR = str(Path.home()) + '/.askelerator/'
CONFIG_FILE = ASKELERATOR_DIR + '/config.json'

def main():
    """Runtime for cli use"""

    gen = generator.Generator(
            os.path.abspath(ASKELERATOR_DIR + '/templates/' + sys.argv[1]), os.path.abspath('.'))
    gen.prepare_specs()
    gen.list_files()
    gen.check_files()
    gen.build_skel()

    return 0
