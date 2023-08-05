from pathlib import Path
from ..utils import load


__all__ = ["tasks"]


tasks = load(path=Path(__file__).resolve(), pkg="backup_utils.tasks", suffix="Task")
