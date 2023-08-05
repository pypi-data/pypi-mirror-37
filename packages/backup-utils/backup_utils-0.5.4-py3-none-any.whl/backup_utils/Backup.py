import json
import subprocess

from sys import argv
from pathlib import Path

from .Task import factory as tasks
from .DatabaseTask import factory as databases
from .Notifier import factory as notifiers


class Backup:
    def __init__(self):
        self._ROOT = Path(argv[0]).resolve().parent
        self._config = {}
        self._logs = {}
        self._cfg_file = Path("~/.config/bak-utils/config.json").expanduser()
        self._load_cfg()

    def _load_cfg(self):
        self._cfg_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if not self._cfg_file.is_file():
            self._save_cfg()
        else:
            self._config = json.loads(self._cfg_file.read_text())

    def _save_cfg(self):
        self._cfg_file.write_text(json.dumps(self._config, indent=4))

    def _check(self):
        self._repo = Path(self._config.get("repo", ""))
        if not self._repo.is_dir():
            raise ValueError("'{}' is not a directory !".format(self._repo))

    def _database(self):
        driver = databases(
            task_name=self._config.get("database", {}).get("driver", "mysql")
        )
        task = driver(
            self._config.get("database", {}).get("cmd", "mysqldump"),
            repo=str(self._repo),
            **self._config.get("database", {})
        )
        task.start()
        self._config.get("directories", []).append(task.backup_dir)

    def _backup(self):
        driver = tasks(task_name=self._config.get("backup", {}).get("driver", "Borg"))
        task = driver(
            self._config.get("backup", {}).get("cmd", "borg"),
            directories=self._config.get("directories", []),
            repo=str(self._repo),
            **self._config.get("backup", {})
        )
        task.start()

    def _sync(self):
        driver = tasks(task_name=self._config.get("sync", {}).get("driver", "Rclone"))
        task = driver(
            self._config.get("sync", {}).get("cmd", "rclone"),
            repo=str(self._repo),
            **self._config.get("sync", {})
        )
        task.start()

    def run(self):
        try:
            self._check()
            if self._config.get("database", None):
                self._database()
            self._backup()
            self._sync()
        except subprocess.CalledProcessError as e:
            err = "Process fail, command : '{}'".format(" ".join(e.cmd))
            files = {"stdout.log": e.stdout, "stderr.log": e.stderr}
            self.notify(err, attachments=files)
            raise
        except Exception as e:
            self.notify(str(e))
            raise

    def notify(self, err, attachments={}):
        driver = notifiers(
            task_name=self._config.get("notifier", {}).get("driver", "print")
        )
        notifier = driver()
        notifier.send(err, attachments)

    def add_dir(self, dirs=[]):
        for d in dirs:
            d = Path(d).expanduser().resolve()
            if not d.is_dir():
                raise ValueError("'{}' must be a directory !".format(d))
            cfg_dirs = set(self._config.get("directories", []))
            cfg_dirs.add(str(d))
            self._config["directories"] = list(cfg_dirs)
        self._save_cfg()
