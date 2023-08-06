import numpy as np
from scipy import stats


class ArithmeticUtil:

    @staticmethod
    def arithmetic_mean(data):
        return np.sum(data) / len(data)

    @staticmethod
    def to_sexagesimal_3d(radians):
        grades = []
        if isinstance(radians, list):
            for item in radians:
                grades.append(180 * item / np.math.pi)
            return grades

        else:
            return radians * 180 / np.math.pi

    @staticmethod
    def to_radian(grades):
        radians = []
        if isinstance(grades, list):
            for item in grades:
                radians.append(item / 180 * np.math.pi)
            return radians
        else:
            radians = (grades / 180 * np.math.pi)
            return radians

    @staticmethod
    def number_of_elements(dat):
        return len(dat)

    @staticmethod
    def max_value(dat):
        return max(dat)

    @staticmethod
    def min_value(dat):
        return min(dat)

    @staticmethod
    def range(dat):
        element_range = ArithmeticUtil.max_value(dat) - ArithmeticUtil.min_value(dat)
        if element_range < 0:
            element_range = element_range * -1

        return element_range

    @staticmethod
    def module_sum(dat):
        return np.math.fsum(dat)

    @staticmethod
    def standard_error(dat):
        """ TESTED
        """
        return stats.sem(dat)


