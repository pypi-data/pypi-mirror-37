"""
Unit test for function askelerator.actions.get_input()
"""
import unittest
from unittest.mock import patch

from askelerator import actions


class TestActionGetinput(unittest.TestCase):

    """Unit tests class for function askelerator.get_input"""

    @patch('askelerator.actions.get_input', return_value='Is test passed ?')
    def test_ok(self, input):
        """
        Given this, test will pass.
        """
        specs = {
            "test": {
                "action": {
                    "question": "test question : "
                }
            }
        }
        self.assertEqual(actions.get_input(specs, 'test'), 'Is test passed ?')

if __name__ == "__main__":
    unittest.main()
