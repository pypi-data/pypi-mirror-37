
# load data from file
from VecStatsGraph.manager.FileManager import FileManager
from VecStatsGraph.manager.graphs.ModuleAngleGraph import ModuleAngleGraph
from VecStatsGraph.manager.ModuleStatisticsManager import ModuleStatisticsManager

fileManager = FileManager()
fileManager.read_file()
dat = fileManager.load_data(fileManager.get_vectorsMatrix())

moduleStatisticsManager = ModuleStatisticsManager()
# DensityGraph.draw_density_graph(dat)
ModuleAngleGraph.draw_module_angle_distrib(dat)
# moduleStatisticsManager.kurtois_module_coefficient(fileManager.getColumnAsArray(0, dat))
