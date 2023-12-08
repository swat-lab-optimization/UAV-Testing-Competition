from pymoo.core.termination import Termination

class UAVTermination(Termination):
    """
    Termination condition based on the number of evaluations.

    Args:
        n_max_evals (float): The maximum number of evaluations. Defaults to infinity.

    Attributes:
        n_max_evals (float): The maximum number of evaluations.

    Methods:
        _update: Updates the termination condition based on the algorithm's progress.
    """

    def __init__(self, n_max_evals=float("inf")) -> None:
        super().__init__()
        self.n_max_evals = n_max_evals

    def _update(self, algorithm):
        """
        Updates the termination condition based on the algorithm's progress.
        """
        if self.n_max_evals is None:
            return 0.0
        else:
            return algorithm.problem.executor.n_sim_evals / self.n_max_evals