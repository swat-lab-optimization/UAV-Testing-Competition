from ambiegen.executors.abstract_executor import AbstractExecutor
from ambiegen.validators.abstract_validator import AbstractValidator
import logging
log = logging.getLogger(__name__)
class ObstacleSceneExecutor(AbstractExecutor):
    """
    Class for executing the test scenarios in the BeamNG simulator
    """
    def __init__(self, generator, test_validator: AbstractValidator= None):
        super().__init__(generator, test_validator)


    def _execute(self, test) -> float:
        fitness = 0
        try:
            test.execute()
            if len(test.test_results) > 0:

                distances = test.get_distances()
                distance = min(distances)
                if distance < 1.5:
                    self.test_dict[self.exec_counter]["outcome"] = "FAIL"
                else:
                    self.test_dict[self.exec_counter]["outcome"] = "PASS"
                log.info(f"Minimum_distance:{(distance)}")
                self.test_dict[self.exec_counter]["metric"] = distance
                fitness = -1/distance
                test.plot()
        except Exception as e:
                self.test_dict[self.exec_counter]["info"] = "ERROR"
                log.info("Exception during test execution, skipping the test")
                log.info(f"{e}")

        return fitness
            