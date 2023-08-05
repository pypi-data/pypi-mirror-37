from pathlib import Path
from ..utils import load


__all__ = ["databases"]


databases = load(
    path=Path(__file__).resolve(), pkg="backup_utils.databases", suffix="Task"
)
