
from pymoo.operators.crossover.sbx import SBX
from ambiegen.mutation.obstacle_mutation import ObstacleMutation
from ambiegen.crossover.one_point_crossover import OnePointCrossover

from pymoo.operators.mutation.pm import PM


from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.de import DE
from pymoo.algorithms.soo.nonconvex.es import ES
from pymoo.algorithms.soo.nonconvex.random_search import RandomSearch

ALGORITHMS = {
    "ga": GA, # Genetic Algorithm,
    "de": DE, # Differential Evolution
    "es": ES, # Evolution Strategy
    "random": RandomSearch
    }

CROSSOVERS = {
    "sbx": SBX,
    "one_point": OnePointCrossover
}

MUTATIONS = {
    "pm": PM,
    "obstacle": ObstacleMutation
}