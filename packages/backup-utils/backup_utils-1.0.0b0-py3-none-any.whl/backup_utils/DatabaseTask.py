from pathlib import Path

from .Task import Task


class DatabaseTask(Task):
    """
    Parent DatabaseTask class, if you create a DatabaseTask,
    your class must be a child of this class.
    This class is a child of `Task`.

    .. seealso:: Task()
    """

    def start(self):
        """
        Test if the directory to backup database file exists.

        .. seealso:: Task.start()
        """
        self._bak_dir = (
            Path(self._config.get("backup_directory", "")).expanduser().resolve()
        )
        if not self._bak_dir.exists():
            raise ValueError("'{}' directory don't exists !".format(self._bak_dir))
        super().start()

    @property
    def backup_dir(self):
        """
        Return the directory containing database backup.

        :return: Directory containing database backup.
        :rtype: str
        """
        return str(self._bak_dir)
