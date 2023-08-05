

from uperations.operation import Operation
import shutil
import os
from termcolor import cprint

class MakeOperationType(Operation):

    @staticmethod
    def name():
        return "make_operationtype"

    @staticmethod
    def description():
        return "Create a new operation type"

    def _parser(self, main_parser):
        main_parser.add_argument('type', help="Name of the operation type")
        return

    def _run(self):

        #Retrieve the library name and path
        operation_type = self.args.type

        template_path = os.path.join(os.path.dirname(os.path.relpath(__file__)),'resources','template')
        new_init_path = os.path.join('operation_types',operation_type,'__init__.py')

        shutil.copytree(template_path, os.path.join('operation_types', operation_type))
        with open(new_init_path,'r') as f:
            new_text = f.read().replace('OPERATIONTYPE', MakeOperationType.to_camel_case(operation_type).capitalize())

        with open(new_init_path,'w') as f:
            f.write(new_text)

        cprint("Operation type successfully created under: %s" % new_init_path,'green')
        return True


    @staticmethod
    def to_camel_case(snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])