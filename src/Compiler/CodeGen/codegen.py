from .instructions import *
from ..Constants.constants import *
from .action_manager import ActionManager
from .symbol_table import SymbolTable
from .runtime_stack import RuntimeStack
from .register_file import RegisterFile
from ..Lexer.cminus_token import Token

class CodeGen:
    def __init__(self):
        self.i = 0
        self.data_address = DATA_SECTION_START_ADDRESS
        self.temp_address = TEMP_SECTION_START_ADDRESS
        self.semantic_stack = []
        self.data_and_temp_stack = []
        if DEBUG:
            self.line_map = []

        self.function_data_start_pointer = 0
        self.function_temp_start_pointer = 0

        self.program = []

        self.symbol_table = SymbolTable(self)
        self.register_file = RegisterFile(self)
        self.runtime_stack = RuntimeStack(self, self.register_file)
        self.action_manager = ActionManager(self, self.symbol_table)

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
            "#saveAndJpfFromLastSave": self.action_manager.save_and_jpf_from_last_save,
            "#assign": self.action_manager.assign,
            "#startNoPush": self.action_manager.start_no_push,
            "#endNoPush": self.action_manager.end_no_push,
            "#declareArray": self.action_manager.declare_array,
            "#array": self.action_manager.array,
            "#until": self.action_manager.until,
            "#handleBreaks": self.action_manager.handle_breaks,
            "#break": self.action_manager.add_break,
            "#pop": self.action_manager.pop,
            "#checkDeclaration": self.action_manager.check_declaration,
            "#uncheckDeclaration": self.action_manager.uncheck_declaration,
            "#declareFunction": self.action_manager.declare_function,
            "#openScope": self.action_manager.open_scope,
            "#closeScope": self.action_manager.close_scope,
            "#setFunctionScopeFlag": self.action_manager.set_function_scope_flag,
            "#popParam": self.action_manager.pop_param,
            "#declareFunction": self.action_manager.declare_function,
            "#call": self.action_manager.call,
            "#setReturnValue": self.action_manager.set_return_value,
            "#jumpBack": self.action_manager.jump_back,
            "#addArgumentCount": self.action_manager.add_argument_count,
            "#zeroInitialize": self.action_manager.zero_initialize,
            "#arrayParam": self.action_manager.array_param,
            "#startBreakScope": self.action_manager.start_break_scope,
            "#setForceDeclarationFlag": self.action_manager.set_force_declaration_flag,
            "#unsetForceDeclarationFlag": self.action_manager.unset_force_declaration_flag,
            "#voidCheck": self.action_manager.void_check,
            "#voidCheckThrow": self.action_manager.void_check_throw,
        }

        initialization_instructions = [
            Assign(f"#{STACK_START_ADDRESS}", self.register_file.stack_pointer_register_address),
            Assign("#0", self.register_file.return_address_register_address),
            Assign("#0", self.register_file.return_value_register_address),
        ]

        self.push_instructions(initialization_instructions)

        self.jump_to_main_address = len(self.program)
        self.program.append(None)
        self.i += 1

        self.add_output_function()

    def act(self, action, * args):
        if DEBUG:
            self.line_map.append((self.i, args))
        self.actions[action](* args)

    def check_program_size(self, size=None):
        if not size:
            size = self.i
        if type(size) == str:
            if size[0] == "#":
                size = size[1:]
            size = int(size)
        while len(self.program) <= size:
            self.program.append(None)

    def push_instruction(self, instruction):
        self.check_program_size()
        self.program[self.i] = instruction.to_code()
        self.i += 1
    
    def save_space(self):
        self.i += 1

    def insert_instruction(self, instruction, destination):
        if type(destination) == str:
            if destination[0] == "#":
                destination = destination[1:]
            destination = int(destination)
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

    def add_output_function(self):
        self.act("#pid", Token(lexeme="output"), None)
        self.act("#declareFunction", None, None)
        self.act("#openScope", None, None)
        self.act("#setFunctionScopeFlag", None, None)
        self.act("#pid", Token(lexeme="a"), None)
        self.act("#popParam", None, None)
        self.act("#pid", Token(lexeme="a"), None)
        self.act("#openScope", None, None)
        self.push_instruction(
            Print(self.semantic_stack.pop()))
        self.act("#closeScope", None, None)
        self.act("#jumpBack", None, None)
