import fire
import os
import subprocess
import shlex
from .GitTask import GitTask


class GitTaskInstaller(GitTask):
    @staticmethod
    def install():
        subprocess.check_call(
            shlex.split(
                "git config --global alias.task '!python3 " + os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "GitTask.py") + "'"))

    @staticmethod
    def uninstall():
        subprocess.check_call(
            shlex.split("git config --global --unset-all alias.task"))


if __name__ == '__main__':
    fire.Fire(GitTaskInstaller)
