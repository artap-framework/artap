import setuptools
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
    packages=setuptools.find_packages(),
    description="Platform for robust design optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://edison.fel.zcu.cz:444/agros/RDOLab/Artap",
    python_requires='>3.6',
    license=about["__license__"],
    data_files=[('artap', ['artap/environment.json']), ('artap/lib', ['artap/lib/bayesopt.so']),
                ('artap/lib', ['artap/lib/_nlopt.so'])],
    install_requires=['numpy',
                      'scipy',
                      'dash>=0.39.0',
                      'dash-core-components>=0.44.0',
                      'dash-html-components>=0.14.0',
                      'dash-table>=3.4.0',
                      'sklearn',
                      "paramiko",
                      'matplotlib',
                      'optproblems',
                      'smt'],
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