import numpy as np
from random import uniform
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .problem import Problem


class PSOAlgorithm(GeneralEvolutionaryAlgorithm):
    def __init__(self, problem: Problem, name="Classic PSO Algorithm"):
        super.__init__(problem, name)

        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum evaluations')
        self.options.declare(name='max_population_number', default=100, lower=1,
                             desc='max_population_number')
        self.options.declare(name='max_population_size', default=100, lower=1,
                             desc='Maximal number of individuals in population')
        self.options.declare(name='n_particles', default=50, lower=10,
                             desc='number_of_particles')
        self.options.declare(name='init_position', default=[1, 1],
                             desc='initial_position_of_particles')

        self.init_pos = np.array(self.options['init_position'])
        self.particle_dim = len(self.options['init_position'])

        '''
        Uniform distribution for initializing particle position and velocity
        '''
        self.particle_pos = uniform(size=(self.options['n_particles'], self.particle_dim)) * self.init_pos
        self.velocity = uniform(size=(self.options['n_particles'], self.particle_dim))

        self.best_global = self.options['init_position']
        self.best_particle = self.particle_pos

# TODO Define : def Update_positions and def Update_velocity
