import subprocess
from os import environ
from .utils import which, render


__all__ = ["Task", "BorgTask", "RcloneTask", "factory"]


class Task(object):
    def __init__(self, cmd, **kwargs):
        self._cmd = which(cmd)
        if not self._cmd:
            raise ValueError("Can't find '{}' binary".format(cmd))
        self._config = kwargs

    def _exec(self, cmds, env=None):
        return subprocess.run(
            cmds, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def _hook(self, hook_name):
        if hook_name in self._config.keys():
            hook = which(self._config[hook_name])
            if not hook:
                raise ValueError(
                    "Can't find '{}' binary for {} hook".format(hook, hook_name)
                )
        self._exec(hook)

    def start(self):
        self._hook("pre_hook")
        self.run()
        self._hook("post_hook")

    def run(self):
        self._exec(self._cmd)


class BorgTask(Task):
    def run(self):
        borg_env = environ.copy()
        borg_env["BORG_PASSPHRASE"] = self._config.get("pswd", "")
        borg_env["BORG_REPO"] = self._config.get("repo")

        compression = self._config.get("compression", "lzma")
        bak_name = render("::{hostname}-{date}")
        borg_cmds = [
            self._cmd,
            "create",
            "-v",
            "--stats",
            "--compression",
            compression,
            "--exclude-caches",
            bak_name,
        ]
        borg_cmds.extend(set(self._config.get("directories", [])))
        self._exec(borg_cmds, env=borg_env)

        prune_cmds = [self._cmd, "prune", "-v", "::"]
        prune_cmds.extend(self._config.get("prune", "-d 7 -w 4 -m 3 -y 1").split(" "))
        self._exec(prune_cmds, env=borg_env)


class RcloneTask(Task):
    def run(self):
        dist = render(self._config.get("dist", ""))
        repo = self._config.get("repo")
        rclone_cmds = [self._cmd, "-v", "sync", repo, dist]
        self._exec(rclone_cmds)


_tasks = {"task": Task, "borg": BorgTask, "rclone": RcloneTask}


def factory(task_name="Task"):
    return _tasks[task_name.lower()]
