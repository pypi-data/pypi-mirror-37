import os

import fire
import logging
import shlex
import subprocess
import yaml


class GitTask:
    """Git-task is a task management system"""

    TASKS_FILE_NAME = ".tasks"
    task_list = None

    def __init__(self):
        try:
            with(open(self.TASKS_FILE_NAME, 'r')) as tasks_file:
                self.task_list = yaml.load(tasks_file)
        except FileNotFoundError:
            logging.info("No " + self.TASKS_FILE_NAME +
                         " file found. Proceeding with empty task list.")

    def __list_default_tasks(self):
        return self.task_list or []

    def save(self):
        if self.task_list is not None:
            with(open(self.TASKS_FILE_NAME, 'w')) as tasks_file:
                yaml.dump(self.task_list, stream=tasks_file,
                          default_flow_style=False)

    def add(self, summary, assignee=None, deadline=None):
        print("Adding new item with summary: \"" + summary + "\"")
        self.task_list = self.__list_default_tasks() + [summary]
        self.save()

    def list(self):
        if self.task_list is None:
            print("No " + self.TASKS_FILE_NAME
                  + " present  in current directory.")
        if self.task_list is None or self.task_list == []:
            print("Hooray, task list is empty!")
            return
        for item in self.task_list:
            print(item)

    @staticmethod
    def remove():
        """Removes one task"""
        print("remove")

    @staticmethod
    def install_git_alias():
        subprocess.check_call(
            shlex.split(
                "git config --global alias.task '!python3 " + os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "GitTask.py") + "'"))

    @staticmethod
    def uninstall_git_alias():
        subprocess.check_call(
            shlex.split("git config --global --unset-all alias.task"))


def main():
    fire.Fire(GitTask)


if __name__ == '__main__':
    main()
