import unittest
import importlib.util
import os


class TestExamples(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_all_examples(self):

        path = os.getcwd() + '/../examples/'
        for module in os.listdir(path):
            if module == '__init__.py' or module[-3:] != '.py':
                continue
            spec = importlib.util.spec_from_file_location(module[:-3], path + os.sep + module)
            script = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(script)
        del module


if __name__ == '__main__':
    unittest.main()
