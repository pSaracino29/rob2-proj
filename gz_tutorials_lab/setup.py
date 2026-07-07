import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'gz_tutorials_lab'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # File di configurazione, mondi e lanciatori
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'sdf_ws'), glob('sdf_ws/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
        (os.path.join('share', package_name, 'rviz_ws'), glob('rviz_ws/*')),
        *[(os.path.join('share', package_name, root), [os.path.join(root, f) for f in files])
          for root, dirs, files in os.walk('models')],
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'odom_tf_broadcaster = gz_tutorials_lab.odom_tf_broadcaster:main',
            'auto_drive = gz_tutorials_lab.movingController:main'
        ],
    },
)
