
from uperations.operation import Operation
from ..utils import create_observer
from uperations.kernel import Kernel

class MakeObserver(Operation):

    @staticmethod
    def name():
        return "make_observer"

    @staticmethod
    def description():
        return "Create an observer"

    def _parser(self, main_parser):
        main_parser.add_argument('library', help="Library name")
        main_parser.add_argument('observer', help="Observer name - No special characters")
        return

    def _run(self):
        create_observer(Kernel.get_instance().find_library(self.args.library), self.args.observer)
        return
