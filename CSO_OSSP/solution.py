import numpy as np
from ossp import ossp

class solution:
    def __init__(self, p: ossp):
        self.problem = p
        self.cells = np.zeros(self.problem.size, int)
        self.fitness = 0.0

    def from_solution(self, origin):
        self.problem = origin.problem
        self.cells = np.copy(origin.cells)
        self.fitness = origin.fitness

    def Initialization(self):
        self.cells = np.random.choice(
            self.problem.size, self.problem.size, replace=False)
        self.cells = [x + 1 for x in self.cells]
        self.fitness = self.problem.evaluate(self.cells)
        n_velocities = np.random.randint(1, 4)
        self.velocity = self.generate_velocity(n_velocities,len(self.cells))
        return [self.cells, self.fitness, False,self.velocity]

    def generate_velocity(self, num_subarrays, max_component_value):
        max_components = min(2, max_component_value)
        v = np.zeros((num_subarrays, max_components), dtype=int)
        for i in range(num_subarrays):
            v[i] = np.random.choice(range(1, max_component_value + 1), size=max_components, replace=False)
        
        return v


    def __str__(self):
        return "cells:" + str(self.cells) + \
               "-fit:" + str(self.fitness)
