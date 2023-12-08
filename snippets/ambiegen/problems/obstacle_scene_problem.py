from ambiegen.problems.abstract_problem import AbstractProblem
import logging #as log
from ambiegen.executors.abstract_executor import AbstractExecutor
import numpy as np
import time
log = logging.getLogger(__name__)

class ObstacleSceneProblem(AbstractProblem):
    def __init__(self, executor: AbstractExecutor, n_var: int=29, l_b:np.ndarray=None, u_p:np.ndarray=None, n_obj=1, n_ieq_constr=1, min_fitness = 1.25):
        super().__init__(executor, n_var, n_obj, l_b, u_p, n_ieq_constr)
        self.min_fitness = min_fitness


    def _evaluate(self, x, out, *args, **kwargs):
        test = x
        start = time.time()
        fitness = self.executor.execute_test(test)
        log.debug(f"Time to evaluate: {time.time() - start}")
        log.info(f"Fitness output: {fitness}")
        out["F"] = fitness
        out["G"] = self.min_fitness - fitness * (-1)