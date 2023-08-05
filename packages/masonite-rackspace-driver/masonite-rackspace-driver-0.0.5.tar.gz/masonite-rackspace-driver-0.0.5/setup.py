from setuptools import setup

setup(
    name="masonite-rackspace-driver",
    packages=[
        'masonite.contrib.rackspace',
        'masonite.contrib.rackspace.drivers',
        'masonite.contrib.rackspace.providers',
    ],
    version='0.0.5',
    install_requires=[
        'rackspace',
    ],
    classifiers=[],
    author='Joseph Mancuso',
    author_email='idmann509@gmail.com',
    url='https://github.com/josephmancuso/masonite-rackspace-driver',
    description='Rackspace upload driver for the Masonite framework',
    keywords=['python web framework', 'python3', 'masonite', 'rackspace'],
    include_package_data=True,
)
