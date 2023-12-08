
from abc import ABC, abstractmethod
from pymoo.core.problem import ElementwiseProblem
from ambiegen.executors.abstract_executor import AbstractExecutor
import numpy as np


class AbstractProblem(ElementwiseProblem, ABC):
    """
    This is the base class for performing solution evalaution
    """

    def __init__(self, executor: AbstractExecutor, n_var: int=29, n_obj=1, xl=None, xu=None, n_ieq_constr=1):
        self.executor = executor

        super().__init__(n_var=n_var, n_obj=n_obj, xl=xl, xu=xu, n_ieq_constr=n_ieq_constr)

    @abstractmethod
    def _evaluate(self, x, out, *args, **kwargs):

        pass