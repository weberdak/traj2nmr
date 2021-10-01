from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='nmrfamsim',
    version='0.1.0',
    install_requires=[
        'mdtraj>=1.9.6',
        'matplotlib>=3.4.3',
        'pandas>=1.3.3',
        'numpy>=1.21.2',
        'jupyter>=1.0.0',
    ],
    description='NMR spectral predictions from molecular dynamics simulation',
    long_description=readme,
    author='Daniel Weber',
    author_email='dkweber@webersc.com',
    url='https://github.com/weberdak/druglord',
    license=license,
)
