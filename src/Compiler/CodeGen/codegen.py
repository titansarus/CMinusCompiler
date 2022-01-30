from .instructions import *
from ..Constants.constants import *
from .action_manager import ActionManager
from .symbol_table import SymbolTable
from .runtime_stack import RuntimeStack

class CodeGen:
    def __init__(self):
        self.i = 0
        self.data_address = DATA_SECTION_START_ADDRESS
        self.temp_address = TEMP_SECTION_START_ADDRESS
        self.semantic_stack = []

        self.symbol_table = SymbolTable(self)
        self.runtime_stack = RuntimeStack(self)
        self.action_manager = ActionManager(self, self.symbol_table)

        self.program = []
        self.push_instruction(
            Assign(f"#{STACK_START_ADDRESS}", self.runtime_stack.sp_address))

        self.actions = {
            "#pid": self.action_manager.pid,
            "#pnum": self.action_manager.pnum,
            "#label": self.action_manager.label,
            "#save": self.action_manager.save,
            "#pushOperation": self.action_manager.push_operation,
            "#execute": self.action_manager.execute,
            "#startArgumentList": self.action_manager.start_argument_list,
            "#endArgumentList": self.action_manager.end_argument_list,
            "#jpfFromSaved": self.action_manager.jpf_from_saved,
            "#jpFromSaved": self.action_manager.jp_from_saved,
            "#assign": self.action_manager.assign,
            "#startNoPush": self.action_manager.start_no_push,
            "#endNoPush": self.action_manager.end_no_push,
        }

    def act(self, action, * args):
        self.actions[action](* args)

    def check_program_size(self, size=None):
        if not size:
            size = self.i
        while len(self.program) <= size:
            self.program.append(None)

    def push_instruction(self, instruction):
        self.check_program_size()
        self.program[self.i] = instruction.to_code()
        self.i += 1
    
    def save_space(self):
        self.i += 1

    def insert_instruction(self, instruction, destination):
        self.check_program_size(destination)
        self.program[destination] = instruction.to_code()

    def push_instructions(self, instructions):
        for instruction in instructions:
            self.push_instruction(instruction)

    def get_next_data_address(self, size = WORD_SIZE):
        address = self.data_address
        self.data_address += size
        return address

    def get_next_temp_address(self, size = WORD_SIZE):
        address = self.temp_address
        self.temp_address += size
        return address
