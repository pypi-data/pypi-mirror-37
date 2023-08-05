from pathlib import Path
from datetime import date
from gzip import compress

from ..DatabaseTask import DatabaseTask


class MysqlDb(DatabaseTask):
    """
    Mysql driver for DatabaseTask.
    """

    default_cmd = "mysqldump"

    def _run(self):
        """
        Create a backup of a database in mysql using mysqldump
        """
        extra_file = (
            Path(self._config.get("extra_file", "~/.my.cnf")).expanduser().resolve()
        )
        if not extra_file.exists():
            raise ValueError("'{}' file don't exist !".format(extra_file))
        now = str(date.today())
        for db in self._config.get("database", []):
            bak_name = "{database}-{date}.sql.gz".format(database=db, date=now)
            bak_file = Path(self.backup_dir) / bak_name
            cmds = [
                self._cmd,
                "--defaults-extra-file={}".format(str(extra_file)),
                "--single-transaction",
                "--quick",
                "--lock-tables={}".format(
                    str(self._config.get("lock_tables", False)).lower()
                ),
                db,
            ]
            proc = self._exec(cmds)
            bak_file.write_bytes(compress(proc.stdout))
