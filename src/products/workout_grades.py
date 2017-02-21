# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from src.products.product_factory import DataProductFactory
factory = DataProductFactory()

daily_logs = factory.get_product("daily_logs")

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PRODUCT_NAME = "daily_logs"

grades = daily_logs.reset_index()[["workout_grade","Date"]]
as_num = {
        'A': 4,
        'B': 3,
        'B/A': 3, # only one of these values, dug in and assigned value
        'C': 2,
        'C, B': 2, # only one of these values, dug in and assigned value
        'D': 1,
        'F': 0
}

# get rid of any days where we didn't do a workout
grades = grades[grades != 0].replace(to_replace={'workout_grade': as_num})

print grades["workout_grade"]

# not very meaningful, or at least not a very obvious result
plt.plot(grades.index, grades["workout_grade"], '^')