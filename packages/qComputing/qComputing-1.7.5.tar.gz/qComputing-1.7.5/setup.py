from setuptools import setup, find_packages

setup(
    name='qComputing',
    version='1.7.5',
    py_modules=['Data', 'Gates', 'NoisyEvolution', 'Operations', 'QCircuit', 'qubit_class', 'SpecialStates', 'Graph'],
    description='A package which deals with light weight routine quantum computing stuff',
    author='Amara Katabarwa',
    author_email="Henriamaa@gmail.com",
    url='https://github.com/akataba/qComputing',
    packages=find_packages(),
    classifiers=[
                  "Programming Language :: Python :: 3",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
              ],
    )
