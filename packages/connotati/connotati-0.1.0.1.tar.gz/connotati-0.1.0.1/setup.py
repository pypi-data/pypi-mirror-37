import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connotati",
    version="0.1.0.1",
    author="Pellegrino Prevete",
    author_email="pellegrinoprevete@gmail.com",
    description="Start gtk apps with given theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tallero/connotati",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['connotati = connotati:main']
    },
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
    ],
)
