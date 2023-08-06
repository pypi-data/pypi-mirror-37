#!/usr/bin/env python3
import codecs
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
about = {}  # type: Dict[str, Any]


with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


with open(os.path.join(here, "wdid", "__version__.py")) as v:
    exec(v.read(), about)  # noqa: S102


required = ["pytz", "click", "attrs"]

setup(
    name="wdid",
    version=about["__version__"],
    description="Recall what you did on a certian day.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Opal Symes",
    author_email="opal@catalyst.net.nz",
    python_requires=">=3.6",
    install_requires=required,
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        "console_scripts": ["wdid=wdid.__main__:cli", "wdid-ts=wdid.ts.__main__:cli"]
    },
    license="GPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
)
