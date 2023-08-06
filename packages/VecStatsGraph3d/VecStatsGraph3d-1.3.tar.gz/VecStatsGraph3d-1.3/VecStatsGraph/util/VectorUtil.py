import numpy as np

from VecStatsGraph.util.ArithmeticUtil import ArithmeticUtil


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
        module    = vectors[0]
        colatitud = vectors[1]
        longitude = vectors[2]

        radian_colatitude = ArithmeticUtil.to_radian(colatitud)
        radian_longitude = ArithmeticUtil.to_radian(longitude)

        x = np.sin(radian_colatitude) * np.cos(radian_longitude) * module
        y = np.sin(ArithmeticUtil.to_radian(colatitud)) * np.sin(ArithmeticUtil.to_radian(longitude)) * module
        z = np.cos(ArithmeticUtil.to_radian(colatitud)) * module

        rectangular_vectors = (x, y, z)
        return rectangular_vectors

    @staticmethod
    def vector_to_polar(vector_matrix):
        modules_2d = []
        colatitud = []
        xy_atan = []
        polar_vectors = []
        z = []
        i = 0

        while i < ArithmeticUtil.number_of_elements(vector_matrix[0]):
            x = vector_matrix[0][i]
            y = vector_matrix[1][i]
            z = vector_matrix[2][i]
            modules_2d.append(np.math.sqrt(x ** 2 + y ** 2))
            xy_atan.append(np.arctan(y / x))
            i +=1

        i = 0

        for x in modules_2d:
            z = vector_matrix[2][i]
            aux = np.math.atan(x / z)
            if aux < 0:
                aux += np.math.pi
            colatitud.append(aux)
            i += 1

        colatitud = ArithmeticUtil.to_sexagesimal_3d(colatitud)
        longitud = ArithmeticUtil.to_sexagesimal_3d(xy_atan)

        fixed_longitud = []
        for aux in longitud:
            if aux < 0:
                aux +=360
            fixed_longitud.append(aux)


        i = 0

        while i < ArithmeticUtil.number_of_elements(vector_matrix[0]):
            x = vector_matrix[0][i]
            y = vector_matrix[1][i]
            z = vector_matrix[2][i]
            polar_vectors.append([np.math.sqrt(x ** 2 + y ** 2 + z ** 2),
                                  colatitud[i],
                                  fixed_longitud[i]])
            i += 1

        return polar_vectors

    @staticmethod
    def calculate_vector_module(x, y, z, x1, y1, z1):
        return np.math.sqrt(((x - x1)**2) + ((y - y1)**2) + ((z-z1)**2))