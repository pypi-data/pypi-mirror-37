
from uperations.operation import Operation
import subprocess

class Command(Operation):

    @staticmethod
    def name():
        return "Command"

    @staticmethod
    def description():
        return "Run any command from the terminal"

    def _parser(self, main_parser):
        main_parser.add_argument('command', help="Command to be run")
        return

    def _run(self):
        command = [self.args.command]+ self.unknown_args
        subprocess.check_output(command, stderr=subprocess.STDOUT)