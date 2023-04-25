from .models.instruction import Instruction
from .models.response_model import GraphNode


def create_graphs(instrs: list[Instruction],
                  call_candidate: int,
                  ret_candidate: int,
                  pc_inc_per_instr: int,
                  pc_offset: int,
                  step: int) -> list[GraphNode]:
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
    function_prologues = sorted({0} | set(function_prologues) | {len(instrs)})

    # list of nodes of function blocks
    function_blocks: list[GraphNode] = []

    # fill function block values of all instructions in a function block
    fbs = [(instrs[start:end], start, end)
           for start, end in zip(function_prologues, function_prologues[1:])]
    for i, (fb, start, end) in enumerate(fbs):
        for instr in fb:
            instr.function_block = i
        function_blocks += [GraphNode({"f_id": i, "start": start, "end": end, "calls_f_id": set()})]

    # point the function block to all other function block it calls
    #   (using the pointer to the other instruction, which states the function block it belongs to)
    for function_block in function_blocks:
        start, end = function_block["start"], function_block["end"]
        for instr in instrs[start:end]:
            if (instr.call_instruction is not None
                and instr.call_instruction.function_block is not None):
                function_block["calls_f_id"].add(instr.call_instruction.function_block)

    return function_blocks
