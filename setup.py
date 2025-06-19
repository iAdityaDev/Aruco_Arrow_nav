#  build configuration script used in Python packages
from setuptools import setup   # used to define package metadata and installation behaviour , This tells setuptools where to install non-Python files
import os
from glob import glob   # Used to match file paths using wildcards (e.g., *.launch.py).

package_name = 'mr_robot_description'

setup(
    extras_require={
        'test': ['pytest']    # pytest is included for running tests (can be installed with pip install -e .[test]
    },
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Aditya Dev SIngh',
    maintainer_email='adityadevsingh16@gmail.com',
    description='The ' + package_name + ' package',
    license='TODO: License declaration',
    # tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
