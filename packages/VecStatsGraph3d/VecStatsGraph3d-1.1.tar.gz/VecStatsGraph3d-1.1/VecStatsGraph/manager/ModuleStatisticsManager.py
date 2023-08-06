import numpy as np

from VecStatsGraph.util.ArithmeticUtil import ArithmeticUtil


class ModuleStatisticsManager:

    def module_variance(self, dat):
        """ TEST SMALL ERROR
        """
        m_arit = ArithmeticUtil.arithmetic_mean(dat)
        n = ArithmeticUtil.number_of_elements(dat)
        return np.math.fsum(((dat - m_arit) ** 2)) / (n - 1)

    def module_standard_deviation(self, dat):
        """ TEST SMALL ERROR
                """
        m_arit = ArithmeticUtil.arithmetic_mean(dat)
        n = ArithmeticUtil.number_of_elements(dat)
        return np.math.sqrt((np.math.fsum((dat - m_arit) ** 2)) / (n - 1))

    def module_population_variance(self, dat):
        """ TEST SMALL ERROR
        """
        m_arit = ArithmeticUtil.arithmetic_mean(dat)
        n = ArithmeticUtil.number_of_elements(dat)
        return sum(((dat - m_arit) ** 2)) / n

    def module_population_standard_deviation(self, dat):
        """ TEST SMALL ERROR
        """
        m_arit = ArithmeticUtil.arithmetic_mean(dat)
        n = ArithmeticUtil.number_of_elements(dat)
        return np.math.sqrt((np.math.fsum((dat - m_arit) ** 2)) / n)

    def skewness_module_coefficient(self, dat):
        """ TEST SMALL ERROR
        """
        n = ArithmeticUtil.number_of_elements(dat)
        mean = ArithmeticUtil.arithmetic_mean(dat)
        s = self.module_standard_deviation(dat)
        return (n / float(((n - 1) * (n - 2)))) * np.math.fsum(((dat - mean) / s) ** 3)

    def kurtois_module_coefficient(self, dat):
        """ TEST STRANGE ERROR
        """

        n = ArithmeticUtil.number_of_elements(dat)
        mean = ArithmeticUtil.arithmetic_mean(dat)
        s = self.module_standard_deviation(dat)

        a = (n * (n + 1)) / float(((n - 1) * (n - 2) * (n - 3)))
        b = sum(((dat - mean) / float(s)) ** 4)
        c = (3 * (n - 1) ** 2) / float(((n - 2) * (n - 3)))
        return ((a *
                 b) -
                c)
