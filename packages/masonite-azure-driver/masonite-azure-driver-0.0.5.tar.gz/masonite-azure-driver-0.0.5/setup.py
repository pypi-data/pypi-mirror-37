from setuptools import setup

setup(
    name="masonite-azure-driver",
    packages=[
        'masonite.contrib.azure',
        'masonite.contrib.azure.drivers',
        'masonite.contrib.azure.providers',
    ],
    version='0.0.5',
    install_requires=[
        'azure',
    ],
    classifiers=[],
    author='Joseph Mancuso',
    author_email='idmann509@gmail.com',
    url='https://github.com/josephmancuso/masonite-azure-driver',
    description='Azure upload driver for the Masonite framework',
    keywords=['python web framework', 'python3', 'masonite', 'azure'],
    include_package_data=True,
)
