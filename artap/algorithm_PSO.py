import numpy as np
from random import uniform
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .problem import Problem


class PSOAlgorithm(GeneralEvolutionaryAlgorithm):
    def __init__(self, problem: Problem, name="Classic PSO Algorithm"):
        super().__init__(problem, name)

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
        self.options.declare(name='max_iteration', default=200,
                             desc='maximum_iteration')

        self.init_pos = np.array(self.options['init_position'])
        self.particle_dim = len(self.options['init_position'])
        self.n_particles = self.options['n_particles']

        '''
        Uniform distribution for initializing particle position and velocity
        '''
        self.particle_pos = np.random.uniform(size=(self.n_particles, self.particle_dim)) * self.init_pos
        self.velocity = np.random.uniform(size=(self.n_particles, self.particle_dim))

        self.best_global = self.options['init_position']
        self.best_particle = self.particle_pos
        self.max_iteration = self.options['max_iteration']

    def Function(self, x):
        x = x
        func = self.problem.evaluate(x)
        return func

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
        random_number = uniform(0, 1)
        new_velocity = w * v + c1 * random_number * (best_particle - x) + c1 * random_number * (best_global - x)
        return new_velocity

    def run(self):
        for j in range(self.max_iteration):
            i: int
            for i in range(self.n_particles):
                x = self.particle_pos[i]
                v = self.velocity[i]
                best_particle = self.best_particle[i]
                self.particle_pos[i] = self.UpdatePosition(x, v)
                self.velocity[i] = self.UpdateVelocity(x, v, best_particle, self.best_global)

                if self.Function(self.particle_pos[i]) < self.Function(best_particle):
                    self.best_particle[i] = self.particle_pos[i]

                if self.Function(self.particle_pos[i]) < self.Function(self.best_global):
                    self.best_global = self.particle_pos[i]
        return self.best_global, self.Function(self.best_global)
