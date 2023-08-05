"""
Unit tests for askelerator.actions.upperize()
"""
import unittest

from askelerator import actions


class TestActionsUpprize(unittest.TestCase):

    """Unit tests for askelerator.actions.upperize()"""
    def test_upperize_1(self):
        """Test normal runtime in expected context"""
        specs = {
            "foo": {
                "output": "foobar"
            },
            "bar": {
                "action": {
                    "type": "upperize",
                    "target": "foo"
                }
            }
        }
        self.assertEqual(actions.upperize(specs, "bar"), "FOOBAR")

    def test_upperize_2(self):
        """Test with invalid key"""
        specs = {
            "foo": {
                "output": "foobar"
            },
            "bar": {
                "action": {
                    "type": "upperize",
                    "target": "fail"
                }
            }
        }
        with self.assertRaises(SystemExit):
            actions.upperize(specs, "bar")

if __name__ == "__main__":
    unittest.main(exit=False)
