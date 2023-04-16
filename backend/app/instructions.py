from functools import reduce
from operator import ior

BYTE_LENGTH = 8

def extract_instruction(binary: bytes, endiannes: str, instr_length: int) -> list:
    instructions = []

    # iterate through instructions
    for j in range(0, len(binary) * BYTE_LENGTH, instr_length):

        start, start_offset = divmod(j, BYTE_LENGTH)
        end, end_offset = divmod(j + instr_length, BYTE_LENGTH)

        if end_offset == 0:
            end -= 1
            end_offset = 8

        instruction_bits = list(binary[start:end + 1])

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
