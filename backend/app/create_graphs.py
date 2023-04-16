class FunctionBlockNode():
    def __init__(self, instructions, id, start, end):
        self.instructions = instructions
        self.id = id
        self.called_function_blocks = []
        self.start = start
        self.end = end

def create_graphs(instrs, call_candidate, ret_candidate, pc_inc_per_instr, pc_offset, step):
    # Find all function prologues
    function_prologues = []
    for e in instrs:
        # remove call pointers from previous iterations of this function call
        e.call_instruction = None
        if (e.call_opcode == call_candidate and 
                (e.call_operand - step * pc_inc_per_instr - pc_offset) % pc_inc_per_instr == 0):
            address = (e.call_operand - step * pc_inc_per_instr - pc_offset) // pc_inc_per_instr
            if address < len(instrs) and instrs[address].ret_opcode == ret_candidate:
                function_prologues += [address + step]
                # we link the call instruction to the function prologue it calls
                e.call_instruction = instrs[address + step] 

    # Assume first instruction is entry point, and take unique function prologues and sort them
    # TODO add end of file variable
    function_prologues = sorted(list({0} | set(function_prologues) | {len(instrs)}))

    # list of nodes of function blocks
    function_blocks = []

    # fill function block values of all instructions in a function block
    fbs = [(instrs[start:end], start, end) 
           for start, end in zip(function_prologues, function_prologues[1:])]
    for i, (fb, start, end) in enumerate(fbs):
        for instr in fb:
            instr.function_block = i
        function_blocks += [FunctionBlockNode(fb, i, start, end)]

    # point the function block to all other function block it calls 
    #   (using the pointer to the other instruction, which states the function block it belongs to)
    for fb in function_blocks:
        called_functions = []
        for instr in fb.instructions:
            if instr.call_instruction is not None:
                called_functions += [instr.call_instruction.function_block]
        fb.called_function_blocks = called_functions

    return [{"f_id": e.id, "calls_f_id": list(set(e.called_function_blocks)), 
             "start": e.start, "end": e.end} for e in function_blocks]
