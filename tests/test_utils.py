import unittest
from context import gen_number


class TestGenNumberMethods(unittest.TestCase):

    def test_upper(self):
        lower_bound = 1
        upper_bound = 9
        x = gen_number([lower_bound, upper_bound],1e-9)
        self.assertLessEqual(x, upper_bound)
        self.assertGreaterEqual(x, lower_bound)

        
if __name__ == '__main__':
    unittest.main()