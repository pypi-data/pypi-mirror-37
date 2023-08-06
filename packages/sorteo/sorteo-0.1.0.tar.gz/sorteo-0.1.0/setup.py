from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sorteo",
    version="0.1.0",
    description="Sorteos usando los asistentes de un evento de Meetup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Santos Gallegos",
    author_email="santos_g@outlook.com",
    url="https://sorteo.readthedocs.io",
    license="MIT",
    packages=["sorteo"],
    install_requires=["tortilla>=0.5.0,<0.6.0"],
    extras_require={
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx-argparse",
            "sphinx-autobuild",
        ]
    },
    entry_points={"console_scripts": ["sorteo = sorteo.main:main"]},
    project_urls={
        "Documentation": "https://sorteo.readthedocs.io",
        "Source Code": "https://github.com/stsewd/sorteo",
        "Bug Tracker": "https://github.com/stsewd/sorteo/issues",
    },
    python_requires=">=3.6",
)
