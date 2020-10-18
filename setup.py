from setuptools import Command, setup, find_packages
from setuptools.command.install import install
import os
import datetime


class CustomInstallCommand(install):
    """Custom install setup to help run shell commands (outside shell) before installation"""

    def run(self):
        os.system('python3 -m pip install numpy')
        os.system('python3 -m pip install cython')
        install.run(self)


base_dir = os.path.abspath(os.path.dirname(__file__))

# long description
with open("README.md", "r") as fh:
    long_description = fh.read()

# requirements
with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")

min_numpy_ver = "1.13.3"


def setup_package():
    setuptools_kwargs = {
        "install_requires": [
            f"numpy >= {min_numpy_ver}",
            requirements,
        ],
        "extras_require" : {'full': [f"agrossuite >= 0.01"]},
        "setup_requires": [f"numpy >= {min_numpy_ver}",
                           f"tqdm >= 4.14",
                           f"pkginfo>=1.4.2",
                           f"bleach>=2.1.0"],
        "zip_safe": False,
    }

    dt = datetime.datetime.now()
    version = "{}.{}".format(dt.strftime('%Y.%m.%d'), dt.hour*60+dt.minute*60+dt.second)

    # replace version in __init__.py
    import fileinput
    for line in fileinput.input("artap/__init__.py", inplace=True):
        if str(line).startswith("__version__"):
            print("__version__ = '{}'".format(version))

    setup(
        name="artap",
        version=version,
        author=u"Artap Team",
        author_email="artap.framework@gmail.com",
        description="Platform for robust design optimization",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="http://www.agros2d.org/artap/",
        python_requires='>=3.6',
        license="License :: OSI Approved :: MIT License",
        cmdclass={'install': CustomInstallCommand},
        packages=find_packages(),
        include_package_data=True,
        # data_files=[('artap/lib', 'artap/lib/bayesopt.so']),
        # install_requires=requirements,
        # scripts=['3rdparty/submodules.sh'],
        classifiers=[
            "Intended Audience :: Science/Research",
            "Operating System :: POSIX :: Linux",
            "Topic :: Scientific/Engineering",
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        **setuptools_kwargs,
    )


if __name__ == "__main__":
    setup_package()
