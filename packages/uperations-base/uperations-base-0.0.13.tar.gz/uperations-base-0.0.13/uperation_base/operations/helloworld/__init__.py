
from uperations.operation import Operation

class Helloworld(Operation):

    @staticmethod
    def name():
        return "hello_world"

    @staticmethod
    def description():
        return "Print Hello world!"

    def _parser(self, main_parser):
        return

    def _run(self):
        print("Hello world!")