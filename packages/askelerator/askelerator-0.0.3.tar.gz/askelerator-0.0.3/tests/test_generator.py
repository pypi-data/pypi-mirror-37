"""
Test suite for Generator object

"""

import unittest
from unittest.mock import patch
import os
import re
from askelerator import generator

class TestGeneratorMethods(unittest.TestCase):
    """Test suite for Generator object methods"""

    source = "/home/fx/src/python/askelerator/askelerator/templates/test"
    target = "/tmp/askelerator_test"
    gen = None
    gen = generator.Generator(source, target)


    def setUp(self):
        pass


    def test_init_1(self):
        """Normal instanciation of a Generator object."""
        self.assertEqual(self.gen.source_path, self.source + '/skel')
        self.assertEqual(self.gen.target_path, self.target)


    @patch('askelerator.actions.get_input', return_value='Plop')
    def test_000_prepare_specs_1(self, get_input):
        """Normal use of prepare_specs()."""
        self.gen.prepare_specs()
        self.assertEqual(self.gen.specs['foo']['output'], 'Plop')
        self.assertEqual(self.gen.specs['foo']['regexp'], re.compile('^foo'))
        self.assertEqual(self.gen.specs['FOO']['output'], 'PLOP')
        self.assertEqual(self.gen.specs['FOO']['regexp'], re.compile('^FOO'))


    def test_010_substitute_1(self):
        """Normal use of substitute()."""
        self.assertEqual(self.gen.substitute('foobar'), 'Plopbar')
        self.assertEqual(self.gen.substitute('bazfoobar'), 'bazfoobar')
        self.assertEqual(self.gen.substitute('FOOBAR'), 'PLOPBAR')


    def test_020_list_files_1(self):
        """Normal use of list_files()."""
        self.gen.list_files()
        ass_files = {
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/barefoot.txt':
            '/tmp/askelerator_test/barefoot.txt',
            '/home/fx/src/python/askelerator/'
            'askelerator/templates/test/skel/FOO1/foobar/barefoot.txt':
            '/tmp/askelerator_test/PLOP1/Plopbar/barefoot.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/FOO1/foobar/foo_B.txt':
            '/tmp/askelerator_test/PLOP1/Plopbar/Plop_B.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/FOO1/foobar/bar.txt':
            '/tmp/askelerator_test/PLOP1/Plopbar/bar.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/FOO1/foobar/foo_A.txt':
            '/tmp/askelerator_test/PLOP1/Plopbar/Plop_A.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/foo_B.txt':
            '/tmp/askelerator_test/Plop_B.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/bar.txt':
            '/tmp/askelerator_test/bar.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/foo_A.txt':
            '/tmp/askelerator_test/Plop_A.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/foo/barefoot.txt':
            '/tmp/askelerator_test/Plop/barefoot.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/foo/foo_B.txt':
            '/tmp/askelerator_test/Plop/Plop_B.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/foo/bar.txt':
            '/tmp/askelerator_test/Plop/bar.txt',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/foo/foo_A.txt':
            '/tmp/askelerator_test/Plop/Plop_A.txt'}
        ass_dirs = {
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/FOO1':
            '/tmp/askelerator_test/PLOP1',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/FOO1/foobar':
            '/tmp/askelerator_test/PLOP1/Plopbar',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/foo':
            '/tmp/askelerator_test/Plop',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/FOO':
            '/tmp/askelerator_test/PLOP',
            '/home/fx/src/python/askelerator/askelerator/templates/test/skel/FOO2':
            '/tmp/askelerator_test/PLOP2'}
        self.assertEqual(self.gen.source_to_target_files, ass_files)
        self.assertEqual(self.gen.source_to_target_dirs, ass_dirs)


    @patch('builtins.input', return_value='O')
    def test_030_check_files_1(self, input):
        """Normal use of check_files()."""
        self.gen.check_files()


    def test_040_build_skel_1(self):
        """Normal use of build_skel()."""
        self.gen.build_skel()
        for directory in self.gen.source_to_target_dirs:
            self.assertTrue(os.path.isdir(directory))
        for f in self.gen.source_to_target_files:
            self.assertTrue(os.path.isfile(f))


if __name__ == '__main__':
    unittest.main()
