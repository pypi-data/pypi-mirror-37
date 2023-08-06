from setuptools import setup

setup(
    name='VecStatsGraph3d',
    version='1.3',
    packages=['VecStatsGraph', 'VecStatsGraph.util', 'VecStatsGraph.manager', 'VecStatsGraph.manager.graphs'],
    url='https://github.com/IvanDragoJr/VecStatsGraph3d',
    license='Apache 2.0',
    author='Pedro Alfonso',
    author_email='p.alfonso.jimenez@gmail.com',
    description='Spherical statistcis analysis', install_requires=['matplotlib', 'scipy', 'numpy']
)
