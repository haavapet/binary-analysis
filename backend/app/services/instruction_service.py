from collections import Counter
from functools import reduce
from operator import ior

BYTE_LENGTH = 8
MAX_INSTRUCTION_VALUE = 0xFFFFFFFFFFFFFFFF
MAX_INSTRUCTION_LENGTH = 64

class Instruction(int):
    def __new__(cls,
                instruction: int,
                instr_len: int,
                call_len: int,
                ret_len: int) -> "Instruction":
        return super().__new__(cls, instruction)

    def __init__(self,instruction: int,
                 instr_len: int,
                 call_len: int,
                 ret_len: int) -> None:

        self.ret_opcode = (instruction &
                           ((MAX_INSTRUCTION_VALUE >> (MAX_INSTRUCTION_LENGTH-instr_len))
                             << (instr_len - ret_len)))
        self.call_opcode = (instruction &
                            ((MAX_INSTRUCTION_VALUE >> (MAX_INSTRUCTION_LENGTH-instr_len))
                             << (instr_len - call_len)))
        self.call_operand = (instruction &
                             (MAX_INSTRUCTION_VALUE >> (MAX_INSTRUCTION_LENGTH-instr_len+call_len)))


def extract_instructions(
        binary: bytes,
        endiannes: str,
        instr_len: int,
        call_len: int,
        ret_len: int,
    ) -> list[Instruction]:

    instruction_values: list[int] = _extract_instruction(binary, endiannes, instr_len)
    return [Instruction(e, instr_len, call_len, ret_len) for e in instruction_values]


def _extract_instruction(
        binary: bytes,
        endiannes: str,
        instr_length: int,
    ) -> list[int]:

    instructions: list[int] = []

    # iterate through instructions
    for j in range(0, len(binary) * BYTE_LENGTH, instr_length):

        start, start_offset = divmod(j, BYTE_LENGTH)
        end, end_offset = divmod(j + instr_length, BYTE_LENGTH)

        if end_offset == 0:
            end -= 1
            end_offset = 8

        instruction_bits: list[int] = list(binary[start:end + 1])

        # If overflow (i.e last instruction has fewer than instr_len bits) then pad empty bytes
        if len(instruction_bits) != end - start + 1:
            overflow_bits = j + instr_length - len(binary) * BYTE_LENGTH
            overflow_bytes = (overflow_bits // BYTE_LENGTH)
            overflow_aligned_byte = (overflow_bits % BYTE_LENGTH == 0)
            instruction_bits += [0x0] * (overflow_bytes - overflow_aligned_byte + 1)

        # negate the first bits of the first byte if not part of instruction
        instruction_bits[0] &= 0xFF >> start_offset

        # negate the last bits of last byte if not part of instruction
        instruction_bits[-1] &= (0xFF << (BYTE_LENGTH - end_offset)) & 0xFF

        # reverse bytes if endiannes is big
        if endiannes == "big":
            instruction_bits = list(reversed(instruction_bits))

        # if instruction is multiple bytes we also need to set the bytes in the correct place
        instruction_bits = [e << (BYTE_LENGTH * i) for i, e in enumerate(instruction_bits)]

        # align by end, f.ex if byte is 0b00101000 and end offset is 5,
        # then correctly shifted instr is 0b00101
        instruction_bits = [e >> (BYTE_LENGTH - end_offset) for e in instruction_bits]

        # bitwise or all bytes of array together into a single instruction value
        instructions.append(reduce(ior, instruction_bits))

    return instructions


def get_call_candidates_counter(
        instructions: list[Instruction],
        call_search_range: tuple[int, int],
    ) -> list[tuple[int, int]]:

    call_opcodes = [e.call_opcode for e in instructions]
    call_candidates = (Counter(call_opcodes)
        .most_common(call_search_range[1]+1)[call_search_range[0]:])

    return call_candidates

def get_ret_candidates_counter(
        instructions: list[Instruction],
        ret_search_range: tuple[int, int],
    ) -> list[tuple[int, int]]:

    ret_opcodes = [e.ret_opcode for e in instructions]
    ret_candidates = (Counter(ret_opcodes)
        .most_common(ret_search_range[1]+1)[ret_search_range[0]:])

    return ret_candidates
