from os import path
import sys

from setuptools import setup, find_namespace_packages

cwd = path.abspath(path.dirname(__file__))

# get the long description from README.md
with open(path.join(cwd, "README.md"), encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    # published project name
    name="utoolbox",

    # from dev to release
    #   bumpversion release
    # to next version
    #   bump patch/minor/major
    version='0.1.5',

    # one-line description for the summary field
    description="A Python image processing package for LLSM.",

    long_description=long_description,
    long_description_content_type='text/markdown',

    # project homepage
    url="https://github.com/liuyenting/utoolbox",

    # name or organization
    author="Liu, Yen-Ting",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research'
    ],

    keywords="microscopy",

    packages=find_namespace_packages(include=['utoolbox.*']),

    python_requires='>=3.6',

    # other packages the build system would require during compilation
    setup_requires=[
    ],

    # other packages the project depends on to run
    #   install_requires -> necessity
    #   requirements.txt -> deployment (use conda environent.yml)
    install_requires=[
        # core
        'cython',
        'ipykernel',

        # numeric and processing
        'numpy',
        'scipy',
        'pandas',

        # file io
        'imageio',
        'tifffile',

        # gui
        'pyqt5',

        # parallel
        'dask',
        'pycuda',

        # utils
        'mako',
        'click',
        'coloredlogs',
        'tqdm',
        'jinja2' # template engine used by pycuda
    ],

    dependency_links=[
    ],

    # additional groups of dependencies here for the "extras" syntax
    extras_require={
    },

    # data files included in packages
    package_data={
        '': ['*.cu']
    },
    # include all package data found implicitly
    #include_package_data=True,

    # data files outside of packages, installed into '<sys.prefix>/my_data'
    data_files=[
    ],

    # executable scripts
    entry_points={
        'console_scripts': [
            'deskew=utoolbox.cli.deskew:main',
            'zpatch=utoolbox.cli.zpatch:main'
        ]
    }
)
