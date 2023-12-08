import os
import numpy as np
import abc
import logging #as log

from abc import ABC, abstractmethod
from ambiegen.validators.abstract_validator import AbstractValidator
from ambiegen.generators.abstract_generator import AbstractGenerator
from typing import Tuple, Dict
log = logging.getLogger(__name__)
import time
class  AbstractExecutor(ABC):
    """
    Class for evaluating the fitness of the test scenarios
    """
    def __init__(
        self,
        generator: AbstractGenerator,
        test_validator: AbstractValidator = None
        #results_path: str = None
    ):
        #self.results_path = results_path
        self.test_validator = test_validator
        self.test_dict = {}
        self.generator = generator

        #if results_path:
            #logger.debug("Creating folder for storing simulation results.")
        #    os.makedirs(results_path, exist_ok=True)

        self.exec_counter = -1  # counts how many executions have been

    def execute_test(self, test) -> Tuple[float, str]:
        """
        The function `execute_test` executes a test and returns the fitness score and information about the
        test execution.
        
        :param test: The `test` parameter in the `execute_test` method is a test case that will be executed.
        It is passed as an argument to the method
        :return: The function `execute_test` returns a tuple containing two values: `fitness` and `info`.
        """
        #logger.debug(f"Execution of a test #{self.exec_counter} (generation method: {test_dict['method']})")
        self.exec_counter += 1  # counts how many executions have been

        fitness = 0

        #if self.test_validator:


        test = self.generator.genotype2phenotype(test)
        self.test_dict[self.exec_counter] = {"test": test, "fitness": None, "info": None, "time": None, "outcome":None, "metric":None}
        valid, info = self.test_validator.is_valid(test)
        #log.info(f"Test: {test}")
        log.info(f"Test validity: {valid}")
        log.info(f"Test info: {info}")
        self.test_dict[self.exec_counter]["info"] = info
        if not valid:
            #logger.debug("The generated road is invalid")
            self.test_dict[self.exec_counter]["fitness"] = fitness

            return float(fitness)

        try:
            start = time.time()
            fitness = self._execute(test)
            duration = time.time() - start
            self.test_dict[self.exec_counter]["fitness"] = fitness
            self.test_dict[self.exec_counter]["time"] = duration
            log.info(f"Executuion time: {duration}")

        except Exception as e:
            print(e)
            #logger.error("Error during execution of test.", exc_info=True)
            self.test_dict[self.exec_counter]["info"] = "Error during execution of test"


        return float(fitness)

    @abc.abstractmethod
    def _execute(self, test) -> float:
        pass