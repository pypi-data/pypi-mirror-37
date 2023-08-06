import math
from __builtin__ import raw_input
from array import array
import itertools

import numpy as np

from VecStatsGraph.util.ArithmeticUtil import ArithmeticUtil
from VecStatsGraph.util.VectorUtil import VectorUtil


class FileManager:

    def __init__(self):
        self.__vectorsMatrix = []
        self.__fixedVectorsMatrix = []
        self.__axis_increment_vector = []

    def get_vectorsMatrix(self):
        return self.__vectorsMatrix

    def get_fixedVectorsMatrix(self):
        return self.__fixedVectorsMatrix

    def get_axisIncrementVector(self):
        return self.__axis_increment_vector

    def set_vectorMatrix(self, vectorMatrix):
        self.__vectorsMatrix = vectorMatrix

    def set_fixedVectorMatrix(self, fixedVectorMatrix):
        self.__fixedVectorsMatrix = fixedVectorMatrix


    def get_input_path_file(self):
        path = raw_input("Enter coordinates file path: ")
        return path

    def get_output_path_file(self):
        path = ""
        isSaving = raw_input("Do you want to save scene scene image?(s/n): ")
        if isSaving == "s":
            path = raw_input("Enter path for image output: ")
        return path

    def read_file(self):

        # path = '/home/pedro/PycharmProjects/VecStatsGraph3d/test/XYZcoor.txt'
        path = self.get_input_path_file()
        vectors_array = []

        with open(path) as f:
            for line in f:
                for coordinate in line.split():
                    vectors_array.append(float(coordinate))

                self.get_vectorsMatrix().append(np.array(vectors_array))
                vectors_array = []


    def transformData(self, vectorsMatrix):

        for vector in vectorsMatrix:
            fixedVector = [float(vector.__getitem__(0)),
                           float(vector.__getitem__(1)),
                           float(vector.__getitem__(2)),
                           float(vector.__getitem__(3)) - float(vector.__getitem__(0)),
                           float(vector.__getitem__(4)) - float(vector.__getitem__(1)),
                           float(vector.__getitem__(5)) - float(vector.__getitem__(2))]
            self.get_fixedVectorsMatrix().append(fixedVector)

    def load_data(self, vectors_matrix):
        data = []
        axis_inc = self.calculateAxisIncrementVector(vectors_matrix)
        polar_vectors = self.calculatePolarFormVector(axis_inc)
        rectangular_vectors = axis_inc

        i = 0
        for polar_element in polar_vectors:
            vector = [VectorUtil.calculate_vector_module(vectors_matrix[i][0],
                                                         vectors_matrix[i][1],
                                                         vectors_matrix[i][2],
                                                         vectors_matrix[i][3],
                                                         vectors_matrix[i][4],
                                                         vectors_matrix[i][5]
                                                         ),    #module
                      polar_element[0],                      #colatitud
                      polar_element[1],                      #longitud
                      rectangular_vectors.__getitem__(i)[0], #Ax
                      rectangular_vectors.__getitem__(i)[1], #Ay
                      rectangular_vectors.__getitem__(i)[2], #Az
                      vectors_matrix[i][0],                  #x0
                      vectors_matrix[i][1],                  #y0
                      vectors_matrix[i][2],                  #z0
                      vectors_matrix[i][3],                  #x1
                      vectors_matrix[i][4],                  #y1
                      vectors_matrix[i][5]]                  #z1
            i += 1
            data.append(vector)

        return data




    def simpleLoad(self):
        path = '/home/pedro/PycharmProjects/test2.7/test/XYZcoor.txt'

        vectorsArray = []
        vectorsMatrix = []
        with open(path) as f:
            for line in f:
                for coordinate in line.split():
                    vectorsArray.append(float(coordinate))
                vectorsMatrix.append(vectorsArray)
                vectorsArray = []

        return vectorsMatrix

    def calculateAxisIncrementVector(self, vectors_matrix):
        fixed_vector = []

        for vector in vectors_matrix:
            fixed_vector.append(np.array([float(vector.__getitem__(3)) - float(vector.__getitem__(0)),
                                 float(vector.__getitem__(4)) - float(vector.__getitem__(1)),
                                 float(vector.__getitem__(5)) - float(vector.__getitem__(2))]))
        return fixed_vector

    def calculatePolarFormVector(self, incremental_vectors):
        modules_2d = []
        colatitude = []
        xy_atan = []
        polar_vectors = []
        for x, y, z in incremental_vectors:
            modules_2d.append(math.sqrt(x ** 2 + y ** 2))
            xy_atan.append(math.atan(x / y))
        i = 0

        for x in modules_2d:
            z = incremental_vectors[i][2]
            colatitude.append(math.atan(x / z))
            i += 1
        # TODO colatitud y latitud negativa

        colatitude = ArithmeticUtil.to_sexagesimal_3d(colatitude)
        latitude = ArithmeticUtil.to_sexagesimal_3d(xy_atan)

        i = 0

        for x, y, z in incremental_vectors:
            polar_vectors.append([math.sqrt(x ** 2 + y ** 2 + z ** 2),
                                  colatitude[i],
                                  latitude[i]])
            i += 1

        return polar_vectors

    def getColumnAsArray(self, column_index, matrix):
        column = []
        for vector in matrix:
            for i in range(len(vector)):
                if i == column_index:
                    column.append(vector[i])
        return column

