import unittest
import importlib.util
import os


def make_test_function(name, filename):
    def test(self):
        spec = importlib.util.spec_from_file_location(name, filename)
        script = importlib.util.module_from_spec(spec)
        path = filename.split(name + '.')[0]
        old_cwd = os.getcwd()
        os.chdir(path)
        spec.loader.exec_module(script)
        os.chdir(old_cwd)

    return test


class TestExamples(unittest.TestCase):
    """ Tests all examples in examples directory."""
    @staticmethod
    def init_tests():
        path = os.getcwd()
        for folder in os.walk(path):
            if folder[0].split('/')[-1] =='__pycache__':
                continue
            files = folder[2]
            for file in files:
                if file == '__init__.py' or file[-3:] != '.py':
                    continue
                else:
                    name = file.split('.')[0]
                    filename = folder[0] + os.sep + file
                    test_func = make_test_function(name, filename)
                    setattr(TestExamples, 'test_{0}'.format(name), test_func)


# create tests dynamically
TestExamples.init_tests()

if __name__ == '__main__':
    unittest.main()
