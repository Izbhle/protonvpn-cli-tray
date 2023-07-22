#!/usr/bin/env python3

import threading
import subprocess
import time

class SubprocessWatcher(threading.Thread):
    def __init__(self, cmd, action, actionTimeSpan=0.2, actionDelay=1):
        self.action = action
        self.cmd = cmd
        self.actionTimeSpan = actionTimeSpan
        self.actionDelay = actionDelay
        self.exitFlag = False
        self.callTime = time.time()
        threading.Thread.__init__(self)

    def exit(self):
        self.process.terminate()
        self.exitFlag = True

    def run(self):
        self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE)
        for c in iter(lambda: self.process.stdout.readlines(1), b''):
            if self.exitFlag:
                return
            if (time.time() - self.callTime) >= self.actionTimeSpan:
                self.callTime = time.time()
                time.sleep(self.actionDelay)
                self.action()
