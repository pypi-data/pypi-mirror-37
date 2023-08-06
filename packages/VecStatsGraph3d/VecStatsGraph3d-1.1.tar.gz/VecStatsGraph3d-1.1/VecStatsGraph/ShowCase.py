from VecStatsGraph.manager.FileManager import FileManager
from VecStatsGraph.manager.ModuleStatisticsManager import ModuleStatisticsManager
from VecStatsGraph.manager.AngleStatisticsManager import AngleStatisticsManager
from VecStatsGraph.util.ArithmeticUtil import ArithmeticUtil
from VecStatsGraph.manager.graphs.ModuleAngleGraph import ModuleAngleGraph
from VecStatsGraph.manager.graphs.DensityGraph import DensityGraph
from VecStatsGraph.manager.graphs.VectorGraph import VectorGraph

moduleStatisticsManager = ModuleStatisticsManager()
angleStatisticsManager = AngleStatisticsManager()
moduleAngleGraph = ModuleAngleGraph()
densityGraph = DensityGraph()
vectorGraph = VectorGraph

fileManager = FileManager()
fileManager.read_file()
dat = fileManager.load_data(fileManager.get_vectorsMatrix())
modules = fileManager.getColumnAsArray(0, dat)

n_elements = ArithmeticUtil.number_of_elements(modules)
min_value = ArithmeticUtil.min_value(modules)
max_value = ArithmeticUtil.max_value(modules)
range_value = ArithmeticUtil.range(modules)
module_sum = ArithmeticUtil.module_sum(modules)
m_arithmetic = ArithmeticUtil.arithmetic_mean(modules)
s_error = ArithmeticUtil.standard_error(modules)
s_d_module = moduleStatisticsManager.module_standard_deviation(modules)
s_d_module_p = moduleStatisticsManager.module_population_standard_deviation(modules)
v_module = moduleStatisticsManager.module_variance(modules)
v_module_p = moduleStatisticsManager.module_population_variance(modules)
cs = moduleStatisticsManager.skewness_module_coefficient(modules)
ca = moduleStatisticsManager.kurtois_module_coefficient(modules)

print("  ---------------------------  ")
print("  LINEAR STATISTICS - MODULES  ")
print("  ---------------------------  ")
print("  NUMBER OF ELEMENTS            =", n_elements)
print("  MIN VALUE                     =", min_value)
print("  MAX VALUE                     =", max_value)
print("  RANGE                         =", range_value)
print("  ARITHMETIC MEAN               =", m_arithmetic)
print("  MEAN STANDARD ERROR           =", s_error)
print("  STANDARD DEVIATION            =", s_d_module)
print("  VARIANCE                      =", v_module)
print("  POPULATION STANDARD DEVIATION =", s_d_module)
print("  POPULATION VARIANCE           =", v_module_p)
print("  SKEWNESS COEFFICIENT          =", cs)
print("  KURTOSIS COEFFICIENT          =", ca)

coordinates = (fileManager.getColumnAsArray(3, dat), fileManager.getColumnAsArray(4, dat), fileManager.getColumnAsArray(5, dat))


vm_direction   = angleStatisticsManager.mean_direction(coordinates)
vm_module      = angleStatisticsManager.mean_module(coordinates)
unit_incr      = angleStatisticsManager.real_mod_to_unit_mod(coordinates)
um_direction   = angleStatisticsManager.mean_direction(unit_incr)
um_module   = angleStatisticsManager.mean_module(unit_incr)
conc_parameter = angleStatisticsManager.concentration_parameter(unit_incr)
sphericalErr   = angleStatisticsManager.spherical_error(unit_incr)

print("  -------------------------------  ")
print("  SPHERICAL STATISTICS - ANGLES    ")
print("  -------------------------------  ")
print("  NUMBER OF ELEMENTS =", n_elements)
print("                                   ")
print("  Statistics for real (non-unit) vectors  ")
print("  --------------------------------------  ")
print("  COLATITUDE  =", vm_direction[1])
print("  LONGITUDE   =", vm_direction[0])
print("  MEAN MODULE =", vm_module)
print("                                 ")
print("  Statistics for unit vectors    ")
print("  -----------------------------  ")
print("  COLATITUDE                =", um_direction[1])
print("  LONGITUDE                 =", um_direction[0])
print("  MEAN MODULE               =", um_module)
print("  CONCENTRATION PARAMETER   =", conc_parameter)
print("  SPHERICAL STANDARD ERROR  =", sphericalErr)

moduleAngleGraph.draw_module_angle_distrib(dat)
densityGraph.draw_density_graph(dat)
vectorGraph.draw_vector_graph(dat)
