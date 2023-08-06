import os

import numpy as np

from scipy import stats
from VecStatsGraph.manager.FileManager import FileManager
import matplotlib.pyplot as plt

# read file
from VecStatsGraph.util.DrawUtil import DrawUtil


class DensityGraph:

    @staticmethod
    def draw_density_graph(dat):
        fileManager = FileManager()
        # define 3d plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        w = 80
        h = 80
        # define 3d plot
        # fig = plt.figure(frameon=False)
        fig.set_size_inches(w, h)
        # calculate density fields
        mu, sigma = 0, 0.1
        x = np.array([row[3] for row in dat])
        y = np.array([row[4] for row in dat])
        z = np.array([row[5] for row in dat])

        xyz = np.vstack([x, y, z])
        density = stats.gaussian_kde(xyz)(xyz)

        idx = density.argsort()
        x, y, z, density = x[idx], y[idx], z[idx], density[idx]

        # margins
        margin = DrawUtil.calculate_margin_max_coordinates(x, y, z)

        # sphere
        DrawUtil.draw_sphere(margin, 0.08, 0, ax)
        DrawUtil.draw_axis_vectors(margin, 0.1, ax)

        # draw density fields
        ax.scatter(x, y, z, c=density)

        ax.set_xlim(margin * -1, margin)
        ax.set_ylim(margin * -1, margin)
        ax.set_zlim(margin * -1, margin)

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.axis('off')

        path = fileManager.get_output_path_file()

        if path != "":
            if not os.path.exists(path):
                os.makedirs(path)
            fig.savefig(path + "/densityGraph.svg")

        plt.show()
