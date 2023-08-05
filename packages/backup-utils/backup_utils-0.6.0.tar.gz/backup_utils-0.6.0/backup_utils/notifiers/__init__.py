from pathlib import Path
from ..utils import load


__all__ = ["notifiers"]


notifiers = load(
    path=Path(__file__).resolve(), pkg="backup_utils.notifiers", suffix="Notifier"
)
