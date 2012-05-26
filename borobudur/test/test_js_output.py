import unittest
import os
from prambanan.test.output_tester import directory_tester

dir = os.path.dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(dir, "js_output_src")

@directory_tester(src_dir, print_output=True)
class TestOutput(unittest.TestCase):
    pass

