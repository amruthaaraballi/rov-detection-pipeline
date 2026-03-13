from setuptools import setup

package_name = 'gate_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='amrutha',
    maintainer_email='amrutha@todo.todo',
    description='Gate perception pipeline',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gate_pipeline_node = gate_perception.gate_pipeline_node:main',
            'image_publisher = gate_perception.image_publisher:main',
        ],
    },
)