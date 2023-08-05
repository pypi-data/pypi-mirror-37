from pathlib import Path

from .Task import Task


class DatabaseTask(Task):
    """
    Parent DatabaseTask class, if you create a DatabaseTask,
    you class must be a children of this class.
    This class is a child of `Task`.

    .. seealso:: Task()
    """

    def start(self):
        """
        Test if the directory to backup database file exist.

        .. seealso:: Task.start()
        """
        self._bak_dir = (
            Path(self._config.get("backup_directory", "")).expanduser().resolve()
        )
        if not self._bak_dir.exists():
            raise ValueError("'{}' directory don't exist !".format(self._bak_dir))
        super().start()

    @property
    def backup_dir(self):
        """
        Return the directory containing database backup.

        :return: Directory containing database backup.
        :rtype: str
        """
        return str(self._bak_dir)
