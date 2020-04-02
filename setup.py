from setuptools import Command, setup, find_packages
from setuptools.command.install import install
import os


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
            # "python-dateutil >= 2.6.1",
            # "pytz >= 2017.2",
            f"numpy >= {min_numpy_ver}",
            requirements,
            #"smt >= 0.3.4",
        ],
        "setup_requires": [f"numpy >= {min_numpy_ver}"],
        "zip_safe": False,
    }

    setup(
        name="artap",
        version="2020.4.02.1",
        author=u"Artap Team",
        author_email="artap.framework@gmail.com",
        description="Platform for robust design optimization",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="http://www.agros2d.org/artap/",
        python_requires='>=3.7',
        license="License :: OSI Approved :: MIT License",
        cmdclass={'install': CustomInstallCommand},
        packages=find_packages(),
        include_package_data=True,
        # data_files=[('artap/lib', ['artap/lib/bayesopt.so']),
        # install_requires=requirements,
        # scripts=['3rdparty/submodules.sh'],
        classifiers=[
            "Intended Audience :: Science/Research",
            "Operating System :: POSIX :: Linux",
            "Topic :: Scientific/Engineering",
            'Programming Language :: Python :: 3.7',
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        **setuptools_kwargs,
    )


if __name__ == "__main__":
    setup_package()
