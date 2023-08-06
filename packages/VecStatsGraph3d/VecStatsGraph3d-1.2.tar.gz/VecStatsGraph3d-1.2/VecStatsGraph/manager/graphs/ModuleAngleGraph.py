import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
#needed to avoid plot projection error
from mpl_toolkits.mplot3d.axes3d import Axes3D

from VecStatsGraph.manager.AngleStatisticsManager import AngleStatisticsManager
from VecStatsGraph.util.ArithmeticUtil import ArithmeticUtil
from VecStatsGraph.util.DrawUtil import DrawUtil


class ModuleAngleGraph:

    @staticmethod
    def draw_module_angle_distrib(dat):
        angle_statistics_manager = AngleStatisticsManager()
        module = np.array([row[0] for row in dat])
        x = np.array([row[3] for row in dat])
        y = np.array([row[4] for row in dat])
        z = np.array([row[5] for row in dat])

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
        max_x = ArithmeticUtil.max_value(x)
        max_y = ArithmeticUtil.max_value(y)
        max_z = ArithmeticUtil.max_value(z)
        max_absolute = max(max_x, max_y, max_z)

        DrawUtil.draw_sphere(max_absolute*1.25, 0.08, 0, ax)
        DrawUtil.draw_axis_vectors(max_absolute*1.25, 0.05, ax)


        ax.quiver(0, 0, 0, x, y, z, arrow_length_ratio=0.01, linewidths=0.422)
        ax.set_xlim(max_absolute*-1, max_absolute)
        ax.set_ylim(max_absolute*-1, max_absolute)
        ax.set_zlim(max_absolute*-1, max_absolute)

        # fig, ax = plt.subplots(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.axis('off')

        fig.savefig("moduleGraph.svg")

        plt.show()

