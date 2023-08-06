import json
import os


class RallfArgs(object):

    def __init__(self):
        self.command = None
        self.task_dir = None
        self.robot = None
        self.mocks = None

    def __str__(self):
        return json.dumps({
            "command": self.command,
            "task_dir": self.task_dir,
            "robot": self.robot,
            "mocks": self.mocks,
        })

    def getProcessed(self):
        processed = RallfArgs()
        processed.command = self.command
        processed.task_dir = None if self.task_dir is None else os.path.abspath(self.task_dir)
        processed.robot = None if self.robot is None else os.path.abspath(self.robot)
        processed.mocks = None if self.mocks is None else os.path.abspath(self.mocks)
        return processed