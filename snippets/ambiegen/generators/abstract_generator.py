import abc
import typing
import numpy as np

class AbstractGenerator(abc.ABC):
    """Abstract class for all generators."""

    def __init__(self):
        """Initialize the generator.

        Args:
            config (dict): Dictionary containing the configuration parameters.
        """

        pass
    @abc.abstractmethod
    def generate_random_test(self):
        pass

    @abc.abstractmethod
    def get_genotype(self):
        pass

    @abc.abstractmethod
    def get_phenotype():
        pass


    @abc.abstractmethod
    def visualize_test():
        pass

