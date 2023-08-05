from pathlib import Path

import setuptools

from backup_utils import __version__, __AUTHOR__

ROOT = Path(__file__).resolve().parent.parent

setuptools.setup(
    name="backup_utils",
    version=__version__,
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
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: POSIX",
        "Topic :: System :: Archiving :: Backup",
        "Intended Audience :: System Administrators",
    ],
)
