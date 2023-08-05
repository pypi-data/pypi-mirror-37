import fire


class GitTask:
    """Git-task is a task management system"""

    @staticmethod
    def add():
        print("add")

    @staticmethod
    def list():
        print("list")

    @staticmethod
    def remove():
        """Removes one todo item"""
        print("remove")


def main():
    fire.Fire(GitTask)


if __name__ == '__main__':
    main()
