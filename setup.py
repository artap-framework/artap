import setuptools
from setuptools.command.build_ext import build_ext as _build_ext
import os


base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "artap", "__about__.py"), "rb") as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="artap",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description="Platform for robust design optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.agros2d.org/artap/",
    python_requires='>3.6',
    license=about["__license__"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    data_files=[('artap', ['artap/environment.json']), ('artap/lib', ['artap/lib/bayesopt.so']),
                ('artap/lib', ['artap/lib/_nlopt.so'])],
    install_requires=['numpy',
                      'scipy',
                      'sklearn',
                      'rpyc',
                      'matplotlib',
                      'optproblems',
                      'smt',
                      'cython',
                      'joblib',
                      'python-gdm'],
    scripts=['3rdparty/submodules.sh'],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering",
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)