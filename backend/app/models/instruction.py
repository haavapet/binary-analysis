class Instruction():
    call_instruction = None # TODO rename this
    function_block = None
    # TODO: opcode may not be first bits, and we are assuming that
    #  call instruction only consists of opcode and operand
    def __init__(self: "Instruction",
                 instruction: int,
                 instr_len: int,
                 ret_len: int,
                 call_len: int) -> None:
        self.value = instruction
        self.ret_opcode = (instruction &
                           ((0xFFFFFFFFFFFFFFFF >> (64-instr_len)) << (instr_len - ret_len)))
        self.call_opcode = (instruction &
                            ((0xFFFFFFFFFFFFFFFF >> (64-instr_len)) << (instr_len - call_len)))
        self.call_operand = (instruction &
                             (0xFFFFFFFFFFFFFFFF >> (64-instr_len+call_len)))
