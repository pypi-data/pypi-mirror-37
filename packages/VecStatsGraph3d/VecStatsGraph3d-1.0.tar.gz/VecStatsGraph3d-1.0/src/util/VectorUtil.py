import numpy as np

from src.util.ArithmeticUtil import ArithmeticUtil


class VectorUtil:

    @staticmethod
    def find_max(numbers):
        max_element = numbers[0]
        for element in numbers:
            if element < 0:
                element = element * -1
            if element > max_element:
                max_element = element
        return max_element

    @staticmethod
    def vectors_to_rectangular(vectors):
        module    = vectors[:, 0]
        colatitud = vectors[:, 1]
        longitude = vectors[:, 2]

        x = np.math.sin(ArithmeticUtil.to_radian(colatitud)) * np.math.cos(ArithmeticUtil.to_radian(longitude)) * module
        y = np.math.sin(ArithmeticUtil.to_radian(colatitud)) * np.math.sin(ArithmeticUtil.to_radian(longitude)) * module
        z = np.math.cos(ArithmeticUtil.to_radian(colatitud)) * module

        rectangular_vectors = [x, y, z]
        return rectangular_vectors

    @staticmethod
    def vector_to_polar(vector_matrix):
        modules_2d = []
        colatitud = []
        xy_atan = []
        polar_vectors = []
        for x, y, z in vector_matrix:
            modules_2d.append(np.math.sqrt(x ** 2 + y ** 2))
            xy_atan.append(np.math.atan(x / y))
        i = 0

        for x in modules_2d:
            z = vector_matrix[i][2]
            colatitud.append(np.math.atan(x / z))
            i += 1
        # TODO colatitud y latitud negativa

        colatitud = ArithmeticUtil.to_sexagesimal_3d(colatitud)
        latitude = ArithmeticUtil.to_sexagesimal_3d(xy_atan)

        i = 0

        for x, y, z in vector_matrix:
            polar_vectors.append([np.math.sqrt(x ** 2 + y ** 2 + z ** 2),
                                  colatitud[i],
                                  latitude[i]])
            i += 1

        return polar_vectors