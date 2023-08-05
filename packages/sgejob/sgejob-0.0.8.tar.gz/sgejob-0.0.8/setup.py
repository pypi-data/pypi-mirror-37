import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sgejob",
    version="0.0.8",
    author='Guanliang MENG',
    author_email='mengguanliang@foxmail.com',
    description="To collect SGE job information with a damemon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    url='https://github.com/linzhi2013',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['pandas'],

    entry_points={
        'console_scripts': [
            'sgejob_daemon=sgejob.daemon:main',
        ],
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ),
)