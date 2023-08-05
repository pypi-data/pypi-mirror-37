import subprocess
import time


class Task:
    def __init__(self, cmd):
        self.cmd = self.set_command(cmd)

    @staticmethod
    def set_command(command):
        return command

    def print_command(self):
        print(self.cmd)

    def run_command(self):

        f_stdout = open("/tmp/full.stdout.log", "w+")
        f_stderr = open("/tmp/full.stderr.log", "w+")

        # Using pipe in command could block the stdout, see this post:
        # https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
        # https://www.reddit.com/r/Python/comments/1vbie0/subprocesspipe_will_hang_indefinitely_if_stdout/
        process = subprocess.Popen(self.cmd, shell=True, executable='/bin/bash',
                                   stdout=f_stdout, stderr=f_stderr)

        while process.poll() is None:
            time.sleep(5)

        f_stdout.close()
        f_stderr.close()

        if process.returncode != 0:
            raise Exception(f"Process {type(self).__name__} failed. Command '{self.cmd}' failed running")
