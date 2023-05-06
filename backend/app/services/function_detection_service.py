from .instruction_service import Instruction


def find_potential_call_edges(
        instructions: list[Instruction],
        call_candidate: int,
        pc_inc: int,
        pc_offset: int,
        is_relative: bool,
        call_operand_len: int,
    ) -> list[tuple[int, int]]:
     """
    Returns a list of edges (from_instruction, to_instruction) for a call candidate
    Note that to_instruction is the exact instruction it calls, and the previous return instruction
    will usually be a few instructions above that
    """
     if is_relative:
          return _find_potential_call_edges_relative(instructions,
                                                     call_candidate,
                                                     pc_inc,
                                                     call_operand_len)
     else:
          return _find_potential_call_edges_absolute(instructions,
                                                     call_candidate,
                                                     pc_inc,
                                                     pc_offset)
# Immediate vs absolute addressing, register addressing not possible
def _find_potential_call_edges_absolute(
        instructions: list[Instruction],
        call_candidate: int,
        pc_inc: int,
        pc_offset: int,
    ) -> list[tuple[int, int]]:
    """
    This finds call edges assuming that the call operand is an absolute address,
    """

    valid_call_edges: list[tuple[int, int]] = []

    for i, e in enumerate(instructions):
        # call opcode is the call candidate,
        # and call operand adresses a valid pc counter
        # and the pc counter it addresses is not outside the length of instructions we have
        if (e.call_opcode == call_candidate
            and (e.call_operand - pc_offset) % pc_inc == 0
            and 0 <= (address := (e.call_operand - pc_offset) // pc_inc) < len(instructions)):
                valid_call_edges += [(i, address)]

    return valid_call_edges


def _find_potential_call_edges_relative(
        instructions: list[Instruction],
        call_candidate: int,
        pc_inc: int,
        call_operand_len: int,
    ) -> list[tuple[int, int]]:
    """
    This finds call edges assuming that the call operand is a relative address,
    """
    # int to signed integer
    def itosi(x: int, num_bits: int) -> int:
        f = ((1 << (num_bits-1)) - 1)
        if (x > f):
            x = x | ~f
        return x

    valid_call_edges: list[tuple[int, int]] = []

    for i, e in enumerate(instructions):
        # call opcode is the call candidate,
        # and call operand adresses a valid pc counter
        # and the pc counter it addresses is not outside the length of instructions we have
        signed_operand = itosi(e.call_operand, call_operand_len)
        if (e.call_opcode == call_candidate
            and 0 <= (address := (int(signed_operand / pc_inc) + i)) < len(instructions)):
                valid_call_edges += [(i, address)]

    return valid_call_edges


def filter_valid_call_edges(
          instructions: list[Instruction],
          ret_opcode: int,
          potential_call_edges: list[tuple[int, int]],
          ret_func_dist: int) -> list[tuple[int, int]]:
    """
    Returns a list of edges (from_instruction, to_instruction) that are valid, i.e there is a
    return instructions at most "ret_func_dist" before it.
    """
    valid_call_edges = set()
    for from_edge, to_edge in potential_call_edges:
        is_first_instruction = to_edge == 0
        for i in range(1, ret_func_dist + 1):
            if (to_edge - i >= 0
                and instructions[to_edge - i].ret_opcode == ret_opcode
                or is_first_instruction):
                valid_call_edges.add((from_edge, to_edge))
    return list(valid_call_edges)


def probability_of_valid_call_edges(
          len_valid_call_edges: int,
          len_potential_call_edges: int,
          call_count: int) -> float:
    """
    Returns a value between 0 and 1, representing the probability of the call and ret opcodes
    being valid, based on the ratio of valid and potential edges and the number of instructions
    with this call opcode
    """
    ratio_valid_call_edges: float = (len_valid_call_edges / call_count)
    ratio_potential_call_edges: float = (len_potential_call_edges / call_count)
    probability: float = ( (2 * ratio_valid_call_edges) + ratio_potential_call_edges) / 3
    return probability
