#!/usr/bin/python3
from argparse import ArgumentParser
from datetime import datetime
import logging
import os
import shutil
import sys
from decouple import config
from ambiegen.generators.obstacle_generator import ObstacleGenerator
from ambiegen.validators.obstacle_scene_validator import ObstacleSceneValidator
from ambiegen.executors.obstacle_scene_executor import ObstacleSceneExecutor
from ambiegen.problems.obstacle_scene_problem import ObstacleSceneProblem
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.random_search import RandomSearch
from ambiegen.sampling.abstract_sampling import AbstractSampling
from aerialist.px4.obstacle import Obstacle
from ambiegen.common.get_random_seed import get_random_seed
from ambiegen import ALGORITHMS, CROSSOVERS, MUTATIONS
from ambiegen.common.duplicate_removal import AbstractDuplicateElimination
from ambiegen.executors.fake_executor import FakeExecutor
from ambiegen.executors.rrt_executor import RRTExecutor
from ambiegen.common.save_results import save_all_tests
from ambiegen.common.termination import UAVTermination

import logging  # as log

TESTS_FOLDER = config("TESTS_FOLDER", default="./generated_tests-01/")
if not (os.path.exists(TESTS_FOLDER)):
    os.makedirs(TESTS_FOLDER, exist_ok=True)
logger = logging.getLogger(__name__)


def arg_parse():
    main_parser = ArgumentParser(
        description="UAV Test Generator",
    )
    subparsers = main_parser.add_subparsers()
    parser = subparsers.add_parser(name="generate", description="generate tests")
    parser.add_argument("test", help="initial test description file address")

    parser.add_argument(
        "budget",
        type=int,
        help="test generation budget (total number of simulations allowed)",
    )

    args = main_parser.parse_args()
    return args


def config_loggers():
    os.makedirs("logs/", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        filename="logs/debug.txt",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    root = logging.getLogger()
    # terminal logs
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)
    root.addHandler(c_handler)

    # file logs
    f_handler = logging.FileHandler("logs/info.txt")
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    f_handler.setFormatter(f_format)
    root.addHandler(f_handler)


if __name__ == "__main__":
    config_loggers()
    args = arg_parse()
    all_tests_dict = {}

    run = 0

    try:
        logger.info("Starting test generation")

        pop_size = 50
        n_offspring = int(pop_size / 2)
        algo = "ga"
        crossover = "one_point"  # "sbx"
        mutation = "obstacle"  # "pm"

        seed = get_random_seed()

        budget = args.budget
        n_eval = budget
        min_size = Obstacle.Size(2, 2, 15)
        max_size = Obstacle.Size(20, 20, 25)
        min_position = Obstacle.Position(-40, 10, 0, 0)
        max_position = Obstacle.Position(30, 40, 0, 90)

        # Set up the algortihm

        generator = ObstacleGenerator(
            min_size, max_size, min_position, max_position, case_study_file=args.test
        )
        validator = ObstacleSceneValidator(
            min_size, max_size, min_position, max_position
        )
        executor = RRTExecutor(generator, validator)
        problem = ObstacleSceneProblem(
            executor,
            n_var=generator.size,
            l_b=generator.l_b,
            u_p=generator.u_b,
            n_obj=1,
            n_ieq_constr=1,
            min_fitness=30,
        )  # 0.66

        method = ALGORITHMS[algo](
            pop_size=pop_size,
            n_offsprings=n_offspring, 
            sampling=AbstractSampling(generator),
            crossover=CROSSOVERS[crossover](),
            mutation=MUTATIONS[mutation](),
            n_points_per_iteration=pop_size,
            eliminate_duplicates=AbstractDuplicateElimination(
                generator=generator, threshold=0.02
            ),
        )

        res = minimize(
            problem,
            method,
            termination=UAVTermination(budget),
            seed=seed,
            verbose=True,
            eliminate_duplicates=True,
            save_history=True,
        )

        logger.info("Execution time: %f" % res.exec_time)

        all_tests = executor.test_dict

        test_cases = []
        for tc in all_tests:
            if all_tests[tc]["info"] == "simulation":
                test_cases.append(all_tests[tc]["test"]) # save only the simulated test cases

        ### copying the test cases to the output folder
        tests_fld = f'{TESTS_FOLDER}{datetime.now().strftime("%d-%m-%H-%M-%S")}/'

        os.mkdir(tests_fld)
        for i in range(len(test_cases)):
            test_cases[i].save_yaml(f"{tests_fld}/test_{i}.yaml")
            shutil.copy2(test_cases[i].log_file, f"{tests_fld}/test_{i}.ulg")
            shutil.copy2(test_cases[i].plot_file, f"{tests_fld}/test_{i}.png")
        print(f"{len(test_cases)} test cases generated")
        print(f"output folder: {tests_fld}")

    except Exception as e:
        logger.exception("program terminated:" + str(e), exc_info=True)
        sys.exit(1)
