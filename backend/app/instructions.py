
class Instruction():
    call_instruction = None # TODO rename this
    function_block = None
    # TODO: opcode may not be first bits, and we are assuming that call instruction only consists of opcode and operand
    def __init__(self, instruction, instr_len, ret_len, call_len):
        self.value = instruction
        self.ret_opcode = instruction & ((0xFFFFFFFFFFFFFFFF >> (64-instr_len)) << (instr_len - ret_len))
        self.call_opcode = instruction & ((0xFFFFFFFFFFFFFFFF >> (64-instr_len)) << (instr_len - call_len))
        self.call_operand = instruction & (0xFFFFFFFFFFFFFFFF >> (64-instr_len+call_len))

def extract_instruction(bin, endiannes, instr_length):
    if endiannes == "big":
        return _extract_instruction_big_endian(bin, instr_length)
    elif endiannes == "little":
        return "NOT IMPLEMENTED" #_extract_instruction_little_endian(bin, instr_length)
    else: pass # TODO throw exception?

def _extract_instruction_big_endian(bin, instr_length):
    instructions = []

    # iterate through instructions
    for j in range(0, len(bin) * 8, instr_length): 
        instr = 0
        start, start_offset = divmod(j, 8)
        end, end_offset = divmod(j + instr_length, 8)

        if end_offset == 0:
            end -= 1
            end_offset = 8

        instruction_bits = list(bin[start:end + 1])

        # negate the last bits of last byte if not part of instruction
        instruction_bits[0] &= 0xFF << ((8 - end_offset) & 0xFF)
        # negate the first bits of the first byte if not part of instruction
        instruction_bits[-1] &= 0xFF >> start_offset

        # shift each bit of the instruction to the correct place
        for i, e in enumerate(reversed((instruction_bits))):
            # align by end, f.ex if byte is 0b00101000 and end offset is 5, then correctly shifted instr is 0b00101
            e >>= 8 - end_offset
            # if instruction is multiple bytes we also need to set the bytes in the correct place
            e <<= 8*i
            instr |= e

        instructions.append(instr)

    return instructions
