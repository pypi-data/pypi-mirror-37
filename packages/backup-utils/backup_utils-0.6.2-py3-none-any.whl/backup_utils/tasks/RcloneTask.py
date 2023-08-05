from ..Task import Task
from ..utils import render


class RcloneTask(Task):
    """
    Task to synchronize with Rclone.

    .. seealso:: Task()
    """

    def _run(self):
        """
        Synchronize using repo.
        """
        dist = render(self._config.get("dist", ""))
        repo = self._config.get("repo")
        rclone_cmds = [self._cmd, "-v", "sync", repo, dist]
        self._exec(rclone_cmds)
