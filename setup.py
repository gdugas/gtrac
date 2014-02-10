from setuptools import find_packages, setup

setup(
    name='Gtrac', version='0.0',
    packages=find_packages(exclude=['*.tests*']),
    entry_points = {
        'trac.plugins': [
            'gtrac = gtrac.monitor',
        ],
    },
)
