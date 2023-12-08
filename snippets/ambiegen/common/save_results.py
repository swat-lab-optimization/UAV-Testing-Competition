import numpy as np
from itertools import combinations
import logging #as log
import os
import json
from datetime import datetime
log = logging.getLogger(__name__)

def save_all_tests(all_tests, path, algo, problem, name):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y")

    stats_path = dt_string + "_" + path + "_" + algo + "_" + problem + "_" + name

    if not os.path.exists(stats_path):
        os.makedirs(stats_path)

    with open(
        os.path.join(stats_path, dt_string + "-all_tests.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(all_tests, f, indent=4)
        log.info(
            "Stats saved as %s", os.path.join(stats_path, dt_string + "-all_tests.json")
        )

    