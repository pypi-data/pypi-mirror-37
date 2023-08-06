import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
#needed to avoid plot projection error
from mpl_toolkits.mplot3d.axes3d import Axes3D

from VecStatsGraph.manager.AngleStatisticsManager import AngleStatisticsManager
from VecStatsGraph.manager.FileManager import FileManager
from VecStatsGraph.util.ArithmeticUtil import ArithmeticUtil
from VecStatsGraph.util.DrawUtil import DrawUtil


class VectorGraph:

    @staticmethod
    def draw_vector_graph(dat):
        fileManager = FileManager()

        angle_statistics_manager = AngleStatisticsManager()
        module = np.array([row[0] for row in dat])
        x = np.array([row[6] for row in dat])
        y = np.array([row[7] for row in dat])
        z = np.array([row[8] for row in dat])

        x1 = np.array([row[9] for row in dat])
        y1 = np.array([row[10] for row in dat])
        z1 = np.array([row[11] for row in dat])

        coord_vectors = [x, y, z]

        mpl._get_configdir()
        R = np.math.sqrt((np.sum(x) * np.sum(x)) + (np.sum(y) * np.sum(y)) + (np.sum(z) * np.sum(z)))

        meanX = np.sum(x) / R
        meanY = np.sum(y) / R
        meanZ = np.sum(z) / R

        meanModule = ArithmeticUtil.arithmetic_mean(module)
        meanDirection = angle_statistics_manager.mean_direction(coord_vectors)

        if meanDirection[0] < 0:
            meanDirection[0] = meanDirection[0] + 180

        if meanX < 0:
            meanDirection[1] = meanDirection[1] + 180

        if meanDirection[1] < 0:
            meanDirection[1] = meanDirection[1] + 360

        Ax = meanModule * np.math.sin(ArithmeticUtil.to_radian(meanDirection[0])) * \
             np.math.cos(ArithmeticUtil.to_radian(meanDirection[1]))

        Ay = meanModule * np.math.sin(ArithmeticUtil.to_radian(meanDirection[0])) * \
             np.math.sin(ArithmeticUtil.to_radian(meanDirection[1]))

        Az = meanModule * np.math.cos(ArithmeticUtil.to_radian(meanDirection[0]))

        w = 80
        h = 80

        # define 3d plot
        fig = plt.figure(frameon=False)
        fig.set_size_inches(w, h)

        ax = fig.add_subplot(111, projection='3d')

        max_x = ArithmeticUtil.max_value(abs(x))
        max_y = ArithmeticUtil.max_value(abs(y))
        max_z = ArithmeticUtil.max_value(abs(z))
        max_x1 = ArithmeticUtil.max_value(abs(x1))
        max_y1 = ArithmeticUtil.max_value(abs(y1))
        max_z1 = ArithmeticUtil.max_value(abs(z1))

        min_x = ArithmeticUtil.min_value(x)
        min_y = ArithmeticUtil.min_value(y)
        min_z = ArithmeticUtil.min_value(z)
        min_x1 = ArithmeticUtil.min_value(x1)
        min_y1 = ArithmeticUtil.min_value(y1)
        min_z1 = ArithmeticUtil.min_value(z1)

        max_absolute = max(max_x, max_y, max_z, max_x1, max_y1, max_z1)
        min_value = min(min_x, min_y, min_z, min_x1, min_y1, min_z1)

        # DrawUtil.draw_sphere(max_absolute*1.25, 0.08, 0, ax)
        # DrawUtil.draw_axis_vectors(max_absolute*1.25, 0.05, ax)


        ax.quiver(x, y, z, x1, y1, z1, arrow_length_ratio=0.01, linewidths=0.422)
        ax.set_xlim(min_value, max_absolute)
        ax.set_ylim(min_value, max_absolute)
        ax.set_zlim(min_value, max_absolute)
        ax.set_aspect('equal')
        # fig, ax = plt.subplots(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        # plt.axis('off')

        path = fileManager.get_output_path_file()

        if path != "":
            if not os.path.exists(path):
                os.makedirs(path)
            fig.savefig(path + "/vectorGraph.svg")

        # plt.tight_layout()

        plt.show()

