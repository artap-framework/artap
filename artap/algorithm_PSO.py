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

    def UpdatePosition(self, x, v):
        x = np.array(x)
        v = np.array(v)
        new_pos = x + v
        return new_pos

    def UpdateVelocity(self, x, v, best_particle, best_global, c1=0.5, c2=1.5, w=0.75):
        """
        x & v : particle current position and velocity
        best_particle : particle's best position
        best_global : best position among all the particles
        c1 & c2 : cognitive scaling constant & social scaling constant
        w : inertia weight
        """
        x = np.array(x)
        v = np.array(v)
        best_particle = np.array(best_particle)
        best_global = np.array(best_global)

        """
        position and velocity must have same shape
        """
        assert x.shape == v.shape
        random_number = uniform()
        new_velocity = w * v + c1 * random_number * (best_particle - x) + c1 * random_number * (best_global - x)
        return new_velocity

# TODO Define : def run()
