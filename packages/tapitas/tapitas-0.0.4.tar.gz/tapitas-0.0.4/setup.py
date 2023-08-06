from setuptools import setup
from setuptools import find_packages

setup(
    name="tapitas",

    version="0.0.4",

    author="Benny Chin",
    author_email="wcchin.88@gmail.com",

    packages=['tapitas', 'tapitas.core_objs', 'tapitas.utils', 'tapitas.utils.exporter'],

    include_package_data=True,

    url="https://bitbucket.org/wcchin/TaPiTaS",

    license="LICENSE.txt",
    description="A data exploration and visualization algorithm for understanding diffusion process.",

    long_description=open("README.md").read(),

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',

         'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],

    keywords='point diffusion subcluster progress',

    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "geopandas",
        "shapely",
        "descartes",
        "matplotlib",
        "seaborn",
    ],
)
