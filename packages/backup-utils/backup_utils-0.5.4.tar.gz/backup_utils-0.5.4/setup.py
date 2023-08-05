from pathlib import Path

import setuptools

from backup_utils import __VERSION__, __AUTHOR__

ROOT = Path(__file__).resolve().parent.parent

setuptools.setup(
    name="backup_utils",
    version=__VERSION__,
    author=__AUTHOR__.split(" <")[0],
    author_email=__AUTHOR__.split(" <")[1].strip("<>"),
    description="The goal of the project is to simplify backup creation.",
    long_description=Path(ROOT / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Oprax/backup-utils",
    packages=setuptools.find_packages(),
    license="MIT",
    entry_points={"console_scripts": ["backup-utils = backup_utils:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
