from uperations.operation import Operation

class OPERATIONTYPE(Operation):

    def _parser(self, main_parser):
        return main_parser

    def _before_start(self):
        super(OPERATIONTYPE, self)._before_start()
        return True

    def _on_running(self):
        super(OPERATIONTYPE, self)._on_running()
        return True

    def _on_error(self, exception):
        super(OPERATIONTYPE, self)._on_error(exception)
        return True

    def _on_completed(self):
        super(OPERATIONTYPE, self)._on_completed()
        return True