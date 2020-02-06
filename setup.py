import setuptools
import os


base_dir = os.path.abspath(os.path.dirname(__file__))
os.system('pip3 install numpy')
os.system('pip3 install cython')


# long description
with open("README.md", "r") as fh:
    long_description = fh.read()

# requirements
with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")



setuptools.setup(
    name="artap",
    version="2020.2.5",
    author=u"Artap Team",
    author_email="artap.framework@gmail.com",
    description="Platform for robust design optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.agros2d.org/artap/",
    python_requires='>3.6',
    license="License :: OSI Approved :: MIT License",
    packages=setuptools.find_packages(),
    include_package_data=True,
    data_files=[('artap/lib', ['artap/lib/bayesopt.so']),
                ('artap/lib', ['artap/lib/_nlopt.so'])],
    install_requires=requirements,
    # scripts=['3rdparty/submodules.sh'],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering",
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
