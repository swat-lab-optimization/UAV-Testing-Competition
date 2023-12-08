from ambiegen.executors.abstract_executor import AbstractExecutor
from ambiegen.validators.abstract_validator import AbstractValidator
import logging
log = logging.getLogger(__name__)
class FakeExecutor(AbstractExecutor):
    """
    Class for executing the test scenarios in the BeamNG simulator
    """
    def __init__(self, generator, test_validator: AbstractValidator= None):
        super().__init__(generator, test_validator)


    def _execute(self, test) -> float:
        fitness = 0


        return fitness
            