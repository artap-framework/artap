import unittest
from ..operators import CustomGenerator, RandomGenerator, FullFactorGenerator, FullFactorLevelsGenerator, PlackettBurmanGenerator, \
    BoxBehnkenGenerator, LHSGenerator, GSDGenerator, HaltonGenerator, UniformGenerator


class TestDOE(unittest.TestCase):

    def setUp(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-2.5, 5]},
                           {'name': 'x_2', 'initial_value': 1.5, 'bounds': [1, 3.4]},
                           {'name': 'x_3', 'initial_value': 3.5, 'bounds': [6, 10]}]

    def test_random_generator(self):
        gen = RandomGenerator(parameters=self.parameters)
        gen.init(3)
        vectors = gen.generate()
        # values
        self.assertTrue(self.parameters[0]['bounds'][0] <= vectors[0][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[0][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[0][2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= vectors[1][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[1][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[1][2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= vectors[2][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[2][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[2][2] <= self.parameters[2]['bounds'][1])

    def test_custom_generator(self):
        gen = CustomGenerator()
        gen.init([[3, 2, 6], [-1, 3, 8]])
        vectors = gen.generate()
        # values
        self.assertEqual(vectors[0][0], 3)
        self.assertEqual(vectors[0][1], 2)
        self.assertEqual(vectors[0][2], 6)
        self.assertEqual(vectors[1][0], -1)
        self.assertEqual(vectors[1][1], 3)
        self.assertEqual(vectors[1][2], 8)

    def test_uniform_generator(self):
        gen = UniformGenerator(parameters=self.parameters)
        gen.init(4)
        vectors = gen.generate()

        # values
        self.assertEqual(len(vectors), 4**len(self.parameters))
        self.assertEqual(vectors[0][2], 6.0)
        self.assertEqual(vectors[1][0], -2.5)
        self.assertEqual(vectors[12][1], 3.4)
        self.assertEqual(vectors[28][2], 6.0)
        self.assertEqual(vectors[35][0], 2.5)
        self.assertEqual(vectors[63][2], 10.0)

    # Factorial Designs
    def test_full_fact_generator(self):
        # General Full-Factorial
        gen = FullFactorGenerator(parameters=self.parameters)
        gen.init(center=False)
        vectors = gen.generate()

        # size
        self.assertEqual(len(vectors), 8)
        # values
        self.assertEqual(vectors[0][0], -2.5)
        self.assertEqual(vectors[1][0], 5.0)
        self.assertEqual(vectors[2][1], 3.4)
        self.assertEqual(vectors[3][1], 3.4)
        self.assertEqual(vectors[7][2], 10.0)

        gen = FullFactorGenerator(parameters=self.parameters)
        gen.init(center=True)
        vectors = gen.generate()

        self.assertEqual(vectors[3][0], -2.5)
        self.assertEqual(vectors[-1][1], 3.4)

    def test_plackett_burman_generator(self):
        # Plackett-Burman
        gen = PlackettBurmanGenerator(parameters=self.parameters)
        vectors = gen.generate()

        # size
        self.assertEqual(len(vectors), 4)
        # values
        self.assertEqual(vectors[0][0], -2.5)
        self.assertEqual(vectors[1][0], 5.0)
        self.assertEqual(vectors[2][2], 6.0)
        self.assertEqual(vectors[3][1], 3.4)

    # Response - Surface Designs
    def test_box_behnken_generator(self):
        # Box-Behnken
        gen = BoxBehnkenGenerator(parameters=self.parameters)
        vectors = gen.generate()

        # size
        self.assertEqual(len(vectors), 13)
        # values
        self.assertEqual(vectors[2][2], 8.0)
        self.assertEqual(vectors[3][1], 3.4)
        self.assertEqual(vectors[5][0], 5.0)
        self.assertEqual(vectors[12][1], 2.2)

    # Randomized Designs
    def test_lhs_generation(self):
        # Latin - Hypercube
        gen = LHSGenerator(parameters=self.parameters)
        gen.init(number=3)
        vectors = gen.generate()

        # size
        self.assertEqual(len(vectors), 3)
        # values
        self.assertTrue(self.parameters[0]['bounds'][0] <= vectors[0][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[0][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[0][2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= vectors[1][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[1][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[1][2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= vectors[2][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[2][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[2][2] <= self.parameters[2]['bounds'][1])

    # Randomized Designs
    def test_halton_generation(self):
        # Halton
        gen = HaltonGenerator(parameters=self.parameters)
        gen.init(number=3)
        vectors = gen.generate()

        # size
        self.assertEqual(len(vectors), 3)
        # values
        self.assertTrue(self.parameters[0]['bounds'][0] <= vectors[0][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[0][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[0][2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= vectors[1][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[1][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[1][2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= vectors[2][0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= vectors[2][1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= vectors[2][2] <= self.parameters[2]['bounds'][1])
        # values
        self.assertEqual(vectors[0][2], 6.8)
        self.assertEqual(vectors[2][0], 3.125)

    # Factorial Designs - levels
    def test_full_fact_levels_generator(self):
        # GSD
        self.parameters = [{'name': 'U_1'},
                           {'name': 'U_2'},
                           {'name': 'U_3'},
                           {'name': 'PH_1'},
                           {'name': 'PH_2'},
                           {'name': 'PH_3'}]
        gen = FullFactorLevelsGenerator(parameters=self.parameters)
        amp = [0, 0.25, 0.5, 0.75, 1]
        phase = [-90.000, -67.500, -45.000, -22.500, 0.000, 22.500, 45.000, 67.500, 90.000]
        gen.init([amp, amp, amp, phase, phase, phase])
        vectors = gen.generate()

        # size
        self.assertEqual(len(vectors), 91125)
        # values
        self.assertEqual(vectors[152][1], 0)
        self.assertEqual(vectors[8596][0], 0.25)
        self.assertEqual(vectors[70153][3], -22.5)
        self.assertEqual(vectors[90454][5], 90.0)

    # Generalized Subset Design (GSD) (C) 2018 - Rickard Sjoegren
    def test_gsd_generator(self):
        # GSD
        # self.parameters = [{'name': 'U_1'}, {'name': 'U_2'}, {'name': 'U_3'}, {'name': 'PH_1'}, {'name': 'PH_2'}, {'name': 'PH_3'}]
        self.parameters = [{'name': 'U_1'}, {'name': 'U_2'}]
        gen = GSDGenerator(parameters=self.parameters)
        gen.init([[1, 3, 2], [6, 8, 4]], reduction=2)
        # amp = [0, 0.25, 0.5, 0.75, 1]
        # phase = [-90.000, -67.500, -45.000, -22.500, 0.000, 22.500, 45.000, 67.500, 90.000]
        # gen.init([amp, amp, amp, phase, phase, phase], reduction=10)
        vectors = gen.generate()

        # size
        self.assertEqual(len(vectors), 5)
        # values
        self.assertEqual(vectors[0][1], 6)
        self.assertEqual(vectors[2][0], 2)
        self.assertEqual(vectors[4][0], 3)


if __name__ == '__main__':
    unittest.main()
