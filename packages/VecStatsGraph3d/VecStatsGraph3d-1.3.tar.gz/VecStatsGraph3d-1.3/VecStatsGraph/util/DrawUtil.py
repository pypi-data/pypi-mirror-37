import numpy as np

from VecStatsGraph.util.VectorUtil import VectorUtil


class DrawUtil:

    @staticmethod
    def calculate_margin_max_coordinates(x, y, z):
        """ Will calculate max element from three integers vectors

        :param x: integer vector x
        :param y: integer vector y
        :param z: integer vector z
        :return: Double of max value found in three parameters

        """
        margin = max(VectorUtil.find_max(abs(x)), VectorUtil.find_max(abs(y)), VectorUtil.find_max(abs(z)))
        margin = margin * 2
        return margin

    @staticmethod
    def draw_sphere(max_coordinates, alpha, line_width, ax):
        """ Will draw a sphere which center is coordinate center

        :param max_coordinates: integer radius value
        :param alpha: float alpha value for sphere surface
        :param line_width: float line width
        :param ax: Axis object where sphere will be displayed
        """
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x_sphere = max_coordinates * np.outer(np.cos(u), np.sin(v))
        y_sphere = max_coordinates * np.outer(np.sin(u), np.sin(v))
        z_sphere = max_coordinates * np.outer(np.ones(np.size(u)), np.cos(v))
        # ax.plot_surface(x_sphere,
        #                 y_sphere,
        #                 z_sphere,
        #                 rstride=4,
        #                 cstride=4,
        #                 color='none',
        #                 linewidth=line_width,
        #                 alpha=alpha)

        # draw sphere
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = np.cos(u) * np.sin(v)
        y = np.sin(u) * np.sin(v)
        z = np.cos(v)
        ax.plot_wireframe(x_sphere, y_sphere, z_sphere, color="b", alpha=alpha)

    @staticmethod
    def draw_axis_vectors(margin, head_ratio, ax):
        """ Will draw three vectors from coordinates origin to max z, x, y values

        :param margin: float max value for three vectos
        :param head_ratio: float head-arrow ratio value
        :param ax: Axis object where vectors will be displayed
        """
        soa = np.array([[0, 0, 0, margin, 0, 0], [0, 0, 0, 0, margin, 0],
                        [0, 0, 0, 0, 0, margin]])

        OX, OY, OZ, OU, OV, OW = zip(*soa)
        ax.set_aspect('equal')
        ax.quiver(OX, OY, OZ, OU, OV, OW, arrow_length_ratio=head_ratio, color="k")
        ax.text(margin, 0, 1, "X", color='red')
        ax.text(0, margin, 1, "Y", color='red')
        ax.text(1, 0, margin, "Z", color='red')


