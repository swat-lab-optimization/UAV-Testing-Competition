from pymoo.core.mutation import Mutation
import numpy as np
import abc

class AbstractMutation(Mutation, abc.ABC):
    """
    Abstract base class for mutation operations.

    Args:
        mut_rate (float): The mutation rate, representing the probability of mutation for each individual.

    Attributes:
        mut_rate (float): The mutation rate.

    """

    def __init__(self, mut_rate: float = 0.4):
        super().__init__()
        self.mut_rate = mut_rate

    def _do(self, problem, X, **kwargs):
        """
        Perform mutation on the given population.

        Args:
            problem: The problem instance.
            X (np.ndarray): The population to be mutated.
            **kwargs: Additional keyword arguments.

        Returns:
            np.ndarray: The mutated population.

        """
        # for each individual
        for i in range(len(X)):
            r = np.random.random()

            # with a probability of mut_rate, change the order of characters
            if r < self.mut_rate:
                X[i] = self._do_mutation(X[i], problem)

        return X

    @abc.abstractmethod
    def _do_mutation(self, x) -> np.ndarray:
        """
        Perform mutation on an individual.

        Args:
            x: The individual to be mutated.

        Returns:
            np.ndarray: The mutated individual.

        """
        pass