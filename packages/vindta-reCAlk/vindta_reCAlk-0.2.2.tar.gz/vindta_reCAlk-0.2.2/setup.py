from setuptools import setup, find_packages
import vindta_reCAlk
import os


def read(fname):
    fpath = os.path.join(os.path.dirname(__file__), fname)
    return open(fpath).read()


def find_version_from_readme():
    s = read("README.md")
    i0 = s.lower().find('version')
    i1 = i0 + 20
    v = s[i0:i1].splitlines()[0]  # removes next line
    v = v.split(' ')[1]  # finds version number
    return v


def walker(base, *paths):
    file_list = set([])
    cur_dir = os.path.abspath(os.curdir)

    os.chdir(base)
    try:
        for path in paths:
            for dname, dirs, files in os.walk(path):
                for f in files:
                    file_list.add(os.path.join(dname, f))
    finally:
        os.chdir(cur_dir)

    return list(file_list)


setup(
    # Application name:
    name="vindta_reCAlk",

    # Version number (initial):
    version=find_version_from_readme(),

    # Application author details:
    author="Luke Gregor",
    author_email="lukegre@gmail.com",

    # Packages
    packages=find_packages(),

    package_data={
        vindta_reCAlk.__name__: walker(
            os.path.dirname(vindta_reCAlk.__file__),
            'templates', 'static'
        ),
    },
    # Include additional files into the package
    include_package_data=True,

    # this creates a command line thingy
    entry_points={
        'console_scripts': ['vindta_reCAlk = vindta_reCAlk.__main__:main']
    },
    # scripts=["vindta_reCAlk/__main__.py"],

    # Details
    url="http://luke-gregor.github.io",

    license="MIT License",
    description="Recalculate VINDTA 3C TA and DIC from CRMs",

    long_description=read("README.md"),

    # Dependent packages (distributions)
    install_requires=[
        "Flask",
        "requires",
        "numpy",
        "scipy",
        "pandas",
        "openpyxl",
        "xlrd",
    ],
)
