import unittest
import importlib.util
import os


def make_test_function(name, filename):
    def test(self):
        print(name)
        spec = importlib.util.spec_from_file_location(name, filename)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
    return test


class TestExamples(unittest.TestCase):
    """ Tests all examples in examples directory."""
    @staticmethod
    def init_tests():
        path = os.getcwd() + '/../examples/'
        for module in os.listdir(path):
            if module == '__init__.py' or module[-3:] != '.py':
                continue

            name = module[:-3]
            filename = path + os.sep + module
            test_func = make_test_function(name, filename)
            setattr(TestExamples, 'test_{0}'.format(name), test_func)

    # def test_all_examples(self):
    #
    #     path = os.getcwd() + '/../examples/'
    #     for module in os.listdir(path):
    #         if module == '__init__.py' or module[-3:] != '.py':
    #             continue
    #         spec = importlib.util.spec_from_file_location(module[:-3], path + os.sep + module)
    #         script = importlib.util.module_from_spec(spec)
    #         spec.loader.exec_module(script)
    #     del module


# create tests dynamically
TestExamples.init_tests()

if __name__ == '__main__':
    unittest.main()
