
class Instruction():
    call_instruction = None # TODO rename this
    function_block = None
    # TODO: opcode may not be first bits, and operand is hardcoded, each needs start and stop index bits
    def __init__(self, instruction, instr_len, ret_len, call_len):
        self.value = instruction
        self.ret_opcode = instruction & ((0xFFFFFFFFFFFFFFFF >> (64-instr_len)) << (instr_len - ret_len))
        self.call_opcode = instruction & ((0xFFFFFFFFFFFFFFFF >> (64-instr_len)) << (instr_len - call_len))
        self.call_operand = instruction & (0x0FFF)


# split bytestream into instructions
#TODO this is only big(?) endian
def extract_instruction(bin, endiannes, instr_length):
    instructions = []

    # change name to byte_mask
    hash_mask_start = {
        0: int("0b11111111", 2),
        1: int("0b01111111", 2),
        2: int("0b00111111", 2),
        3: int("0b00011111", 2),
        4: int("0b00001111", 2),
        5: int("0b00000111", 2),
        6: int("0b00000011", 2),
        7: int("0b00000001", 2),
    }

    hash_mask_end = {
        0: int("0b11111111", 2),
        1: int("0b11111110", 2),
        2: int("0b11111100", 2),
        3: int("0b11111000", 2),
        4: int("0b11110000", 2),
        5: int("0b11100000", 2),
        6: int("0b11000000", 2),
        7: int("0b10000000", 2),
    }

    # TODO so far only big? endian here, but small? endian should be mostly the same, just some things switched
    # iterate through bits
    for i in range(0, len(bin) * 8, instr_length): 
        # i = 0, 16, 32, 48...
        # find start of instruction byte and offset into byte

        instr = 0
        start, start_offset = divmod(i, 8)
        end, end_offset = divmod(i + instr_length, 8)
        if end_offset != 0: end += 1 
        for i, e in enumerate(reversed((bin[start:end]))):
            # negate the first bits if not part of instruction
            # THIS IS THE LAST BYTE
            if i == 0: e = (e & hash_mask_end[end_offset]) >> end_offset

            # negate the last bits if not part of instruction
            # THIS IS THE FIRST BYTE
            if i == end - start - 1: e = (e & hash_mask_start[start_offset]) 

            # move bits to correct place
            # might need to add start_index or something when shifting
            if i != 0:
                instr |= e << (8*i - end_offset)
            else:
                instr = e
            # print(i, start, end, start_offset, end_offset, bin[start:end],hex(a), hex(instr))
        instructions.append(instr)

    return instructions
