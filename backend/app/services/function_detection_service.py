from .instruction_service import Instruction


def find_potential_call_edges(
        instructions: list[Instruction],
        call_candidate: int,
        pc_inc: int,
        pc_offset: int,
    ) -> list[tuple[int, int]]:
    """
    Returns a list of edges (from_instruction, to_instruction) for a call candidate
    Note that to_instruction is the exact instruction it calls, and the previous return instruction
    will usually be a few instructions above that

    This finds call edges assuming that the call opcode is an absolute address,
    If one instead assumes the call opcode is a relative address, then changes needs to be made here
    """

    valid_call_edges: list[tuple[int, int]] = []

    for i, e in enumerate(instructions):
        # call opcode is the call candidate,
        # and call operand adresses a valid pc counter
        # and the pc counter it addresses is not outside the length of instructions we have
        if (e.call_opcode == call_candidate
            and (e.call_operand - pc_offset) % pc_inc == 0
            and 0 < (address := (e.call_operand - pc_offset) // pc_inc) < len(instructions)):
                valid_call_edges += [(i, address)]

    return valid_call_edges


def filter_valid_call_edges(
          instructions: list[Instruction],
          ret_opcode: int,
          potential_call_edges: list[tuple[int, int]],
          ret_func_dist: int) -> list[tuple[int, int]]:

    valid_call_edges = set()
    for from_edge, to_edge in potential_call_edges:
        is_first_instruction = to_edge == 0
        for i in range(1, ret_func_dist + 1):
            if instructions[to_edge - i].ret_opcode == ret_opcode or is_first_instruction:
                valid_call_edges.add((from_edge, to_edge))
    return list(valid_call_edges)


def probability_of_valid_call_edges(
          len_valid_call_edges: int,
          len_potential_call_edges: int,
          call_count: int) -> float:
     ratio_valid_call_edges: float = (len_valid_call_edges / call_count)
     ratio_potential_call_edges: float = (len_potential_call_edges / call_count)
     probability: float = ( (2 * ratio_valid_call_edges) + ratio_potential_call_edges) / 3
     return probability
