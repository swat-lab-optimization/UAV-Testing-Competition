import numpy as np
from abc import ABC, abstractmethod


class AbstractValidator(ABC):
    def __init__(self, ):
        pass

    @abstractmethod
    def is_valid(self, test) -> (bool, str):
        pass

        