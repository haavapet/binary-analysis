

# 1. Read file, extract binary data relating to code section
# 2. Heuristically split into instructions DONE
# 3. Do heuristic analysis on instruction, frequencies etc.
#           Find instruction frequencies based on ret opcode length (in this case 4 bytes) RET = 0EEE
#           Find instruction frequencies based on call opcode length (in this case 1 byte) CALL = 2NNN, where NNN is address
#           Among the top 20 most common, CALL instr will lead close to RET instr, i.e the operand of CALL will be address of RET plus 8 bytes etc.
#           We can put each RET candidate in a hashmap?


from instructions import Instruction, extract_instruction
from create_graphs import create_graphs
from find_best_candidates import find_best_candidates


def read_file(FILENAME):
    bin=open(FILENAME, "rb").read()
    return bin

class Base():
    instructionLength = 16
    retOpcodeLength = 16
    callOpcodeLength = 4
    fileOffset = 0x0
    fileOffsetEnd = 1072# 0xAAA
    pcOffset = 0x200
    pcIncPerInstr = 2 # how much PC increments per instruction, usually byter per instruction, but not sure
    endiannes = "little"
    nrCandidates = 4
    callCandidateRange = [3, 7]
    retCandidateRange = [5, 15]
    returnToFunctionPrologueDistance = 3


    
if __name__ == "__main__":
    FILENAME = 'quar.ch8'
    binary = read_file(FILENAME)
    form = Base()
    print(binary[0])
    #bin = "0x24 0xC6 0x24 0xFE 0xF1 0x0A 0x24 0xC6 0x64 0x00 0x63 0x00 0x6B 0x00 0x6E 0xFF 0x6A 0x14 0x6D 0x40 0x6C 0x64 0x67 0x01 0x66 0x00 0x4E 0x00 0x24 0x5C 0x46 0x03 0x13 0x38 0x34 0x00 0x12 0x3C 0xC1 0x03 0x37 0x01 0x12 0x32 0x88 0x14 0x78 0x01 0x12 0x36 0x88 0x15 0x78 0xFF 0xC9 0x0F 0x79 0x06 0x25 0x24 0x34 0x02 0x12 0x50 0xA6 0x3F 0xD0 0x56 0x72 0xFF 0x32 0x00 0x12 0x50 0xA6 0x39 0xD0 0x56 0x64 0x00 0x34 0x06 0x12 0x64 0x35 0x00 0x12 0x62 0x00 0xE0 0x24 0xFE 0x25 0x0E 0x25 0x24 0x64 0x00 0x75 0xFF 0x34 0x03 0x12 0xE8 0x35 0x0A 0x12 0x74 0xA7 0x0D 0x61 0x25 0x62 0x0B 0xD1 0x21 0x35 0x08 0x12 0x80 0xA7 0x0E 0x61 0x25 0x62 0x0B 0xD1 0x21 0x35 0x06 0x12 0x8C 0xA7 0x0F 0x61 0x25 0x62 0x0B 0xD1 0x21 0x35 0x04 0x12 0xE6 0xA7 0x10 0x61 0x25 0x62 0x0B 0xD1 0x21 0xC1 0x01 0xC2 0x01 0x81 0x24 0x71 0x01 0x30 0x03 0x12 0xAC 0x41 0x02 0x7D 0x02 0x41 0x01 0x7D 0xFF 0x30 0x01 0x12 0xB8 0x41 0x02 0x7D 0xFF 0x41 0x03 0x7D 0x02 0x30 0x02 0x12 0xC4 0x41 0x03 0x7D 0xFF 0x41 0x01 0x7D 0x02 0x4D 0xFF 0x6D 0x00 0x60 0x64 0x80 0xD5 0x4F 0x00 0x6D 0x64 0x24 0xBA 0x80 0x10 0x61 0x24 0x62 0x08 0xD1 0x27 0x30 0x03 0x12 0xE4 0x61 0x2C 0xA6 0xDA 0xD1 0x26 0x64 0x06 0x75 0xFF 0x34 0x01 0x13 0x1C 0x61 0x00 0x62 0x00 0x39 0x06 0x62 0xFF 0x98 0x00 0x13 0x02 0x81 0x80 0x81 0x07 0x81 0xF0 0x41 0x00 0x61 0xFF 0x25 0x24 0x88 0x14 0x89 0x24 0x67 0x00 0x41 0x01 0x67 0x01 0x25 0x24 0x81 0x21 0x31 0x00 0x13 0x1C 0xA6 0x33 0xD0 0x56 0x64 0x00 0x61 0x1E 0xF1 0x15 0x23 0x8E 0xF1 0x07 0x41 0x00 0x13 0x2A 0x13 0x20 0x34 0x00 0x13 0x36 0x25 0x24 0x24 0x44 0x73 0x01 0x23 0x3E 0x12 0x1A 0x00 0xE0 0x24 0xE2 0x13 0x3C 0x33 0x00 0x13 0x4C 0x61 0x48 0x81 0xD5 0x4F 0x00 0x36 0x03 0x76 0x01 0x61 0x02 0x8C 0x15 0x4F 0x00 0x6C 0x00 0x3A 0x64 0x7A 0x01 0x61 0x50 0x81 0xA7 0x3F 0x01 0x13 0x68 0x3E 0x00 0x7E 0xFF 0x3D 0x00 0x7D 0xFF 0x61 0xF8 0x81 0xB2 0x31 0xF8 0x13 0x78 0x3E 0x00 0x7E 0xFF 0x3D 0x00 0x7D 0xFF 0x4B 0xFF 0x13 0x8C 0x61 0x0F 0x81 0x32 0x31 0x0F 0x13 0x8C 0x25 0x0E 0x8B 0xB6 0x7B 0x80 0x25 0x0E 0x00 0xEE 0x34 0x00 0x14 0x0E 0x62 0x0B 0xE2 0x9E 0x13 0xB0 0x4C 0x00 0x00 0xEE 0x25 0x24 0x68 0x30 0x69 0x10 0x67 0x00 0x25 0x24 0x24 0x78 0x60 0x01 0x24 0xA4 0x65 0x0E 0x64 0x03 0x62 0x0C 0xE2 0x9E 0x13 0xBE 0x25 0x0E 0x8B 0xBE 0x25 0x0E 0x00 0xEE 0x62 0x0D 0xE2 0x9E 0x13 0xE6 0x80 0x80 0x70 0xFF 0x37 0x01 0x13 0xD6 0x70 0x06 0x46 0x01 0x70 0x04 0x46 0x02 0x70 0x0A 0x85 0x90 0x75 0xFA 0xA6 0x39 0xD0 0x56 0x64 0x02 0x6C 0x64 0x62 0x0A 0x00 0xEE 0x62 0x0E 0xE2 0x9E 0x13 0xF4 0x64 0x04 0x00 0xE0 0x25 0x40 0x00 0xEE 0x62 0x0F 0xE2 0x9E 0x14 0x0E 0x4C 0x00 0x00 0xEE 0xC0 0x1F 0x70 0x10 0x65 0x00 0xA6 0x33 0xD0 0x56 0x64 0x01 0x6A 0x00 0x00 0xEE 0x34 0x04 0x14 0x1E 0xF1 0x0A 0x00 0xE0 0x24 0xFE 0x25 0x0E 0x25 0x24 0x64 0x00 0x34 0x03 0x14 0x42 0x62 0x02 0xE2 0x9E 0x14 0x32 0x24 0xA4 0x70 0x01 0x40 0x04 0x60 0x01 0x24 0xA4 0x62 0x08 0xE2 0x9E 0x14 0x42 0x24 0xA4 0x70 0xFF 0x40 0x00 0x60 0x03 0x24 0xA4 0x00 0xEE 0x81 0x80 0x71 0x10 0x62 0xC0 0x81 0x22 0x31 0x00 0x67 0x00 0x81 0x80 0x62 0xF8 0x81 0x22 0x41 0x00 0x67 0x01 0x00 0xEE 0x44 0x05 0x00 0xEE 0x64 0x05 0x69 0x00 0x67 0x01 0x25 0x32 0xA6 0x83 0x61 0x34 0x62 0x17 0xD1 0x25 0xA6 0x88 0x61 0x3C 0xD1 0x25 0x00 0xEE 0x61 0x08 0x62 0x0A 0xA6 0xF7 0xD1 0x2B 0x61 0x10 0xA7 0x02 0xD1 0x2B 0x61 0x0C 0x62 0x06 0xA6 0xBF 0xD1 0x23 0x62 0x16 0xA6 0xC2 0xD1 0x23 0x61 0x22 0x62 0x06 0xA6 0xE0 0xD1 0x2B 0x61 0x2A 0xA6 0xEB 0xD1 0x2C 0x00 0xEE 0x81 0x00 0x24 0xBA 0x61 0x0A 0x62 0x0C 0xD1 0x27 0x30 0x03 0x14 0xB8 0x61 0x12 0xA6 0xDA 0xD1 0x26 0x00 0xEE 0xA6 0xC5 0x41 0x03 0xA6 0xD3 0x41 0x02 0xA6 0xCC 0x00 0xEE 0x61 0x00 0x62 0x04 0x60 0x04 0xA7 0x11 0xD1 0x24 0x71 0x08 0x31 0x40 0x14 0xDA 0x61 0x00 0x72 0x04 0xF0 0x1E 0x32 0x1C 0x14 0xCE 0x00 0xEE 0x61 0x00 0x62 0x00 0x60 0x08 0xA7 0xD1 0xD1 0x28 0x71 0x08 0x31 0x40 0x14 0xF6 0x61 0x00 0x72 0x08 0xF0 0x1E 0x32 0x20 0x14 0xEA 0x00 0xEE 0xA6 0x30 0x62 0x1F 0x61 0x00 0xD1 0x21 0x71 0x08 0x31 0x40 0x15 0x04 0x00 0xEE 0xA6 0x31 0x60 0x00 0x65 0x1D 0x81 0xB0 0x81 0x1E 0x3F 0x00 0xD0 0x52 0x70 0x08 0x31 0x00 0x15 0x16 0x00 0xEE 0x46 0x00 0x25 0xF4 0x46 0x01 0x25 0xFE 0x46 0x02 0x26 0x0E 0x00 0xEE 0x46 0x00 0x25 0xF4 0x46 0x01 0x26 0x08 0x46 0x02 0x26 0x24 0x00 0xEE 0x62 0x04 0xA6 0x8D 0xD2 0x25 0x61 0x0C 0xA6 0x92 0xD1 0x25 0x61 0x14 0xA6 0x97 0xD1 0x25 0x62 0x0D 0x61 0x04 0xA6 0x9C 0xD1 0x25 0x61 0x0C 0xA6 0xA1 0xD1 0x25 0x61 0x14 0xA6 0xA6 0xD1 0x25 0x62 0x16 0x61 0x04 0xA6 0xAB 0xD1 0x25 0x61 0x0C 0xA6 0xB0 0xD1 0x25 0x61 0x14 0xA6 0xB5 0xD1 0x25 0x61 0x1C 0xA6 0xBA 0xD1 0x25 0xA8 0xD1 0x81 0xA0 0xF1 0x33 0xA8 0xD1 0xF0 0x65 0xF0 0x29 0x61 0x2E 0x62 0x04 0xD1 0x25 0xA8 0xD2 0xF0 0x65 0xF0 0x29 0x61 0x33 0xD1 0x25 0xA8 0xD3 0xF0 0x65 0xF0 0x29 0x61 0x38 0xD1 0x25 0xA8 0xD1 0x81 0xD0 0xF1 0x33 0xA8 0xD1 0xF0 0x65 0xF0 0x29 0x61 0x2E 0x62 0x0D 0xD1 0x25 0xA8 0xD2 0xF0 0x65 0xF0 0x29 0x61 0x33 0xD1 0x25 0xA8 0xD3 0xF0 0x65 0xF0 0x29 0x61 0x38 0xD1 0x25 0xA8 0xD1 0x81 0xC0 0xF1 0x33 0xA8 0xD1 0xF0 0x65 0xF0 0x29 0x61 0x2E 0x62 0x16 0xD1 0x25 0xA8 0xD2 0xF0 0x65 0xF0 0x29 0x61 0x33 0xD1 0x25 0xA8 0xD3 0xF0 0x65 0xF0 0x29 0x61 0x38 0xD1 0x25 0x00 0xEE 0xA6 0x45 0x47 0x01 0xA6 0x48 0xD8 0x93 0x00 0xEE 0xA6 0x4B 0x47 0x01 0xA6 0x4F 0xD8 0x94 0x00 0xEE 0xA6 0x53 0xD8 0x94 0x00 0xEE 0xA6 0x57 0x47 0x01 0xA6 0x67 0xD8 0x98 0x78 0x08 0xA6 0x5F 0x47 0x01 0xA6 0x6F 0xD8 0x98 0x78 0xF8 0x00 0xEE 0xA6 0x77 0xD8 0x96 0x78 0x08 0xA6 0x7D 0xD8 0x96 0x00 0xEE"
    #bin = bin.split()
    #instr = [Instruction(int(e + a[2:], 16), 16, 4) for e, a in zip(bin[::2], bin[1::2])]

    instruction_values = extract_instruction(binary[form.fileOffset:form.fileOffsetEnd], form.endiannes, form.instructionLength)
    instructions = [Instruction(e, form.instructionLength, form.retOpcodeLength, form.callOpcodeLength) for e in instruction_values]
    candidates = find_best_candidates(instructions, form.pcIncPerInstr, form.pcOffset, form.nrCandidates, form.callCandidateRange, form.retCandidateRange)

    # Line too long for oneliner :(
    # candidates_with_graph = [{"probability": prob, "ret_opcode": ret, "call_opcode": call, "graphs": create_graphs(instructions, call, ret, step)} for prob, _, _, call, ret, step in candidates]
    
    candidates_with_graph = []
    for prob, _, _, call, ret, step in candidates:
        graph = create_graphs(instructions, call, ret, form.pcIncPerInstr, form.pcOffset, step)
        candidates_with_graph += [{"probability": prob, "ret_opcode": ret, "call_opcode": call, "graph": graph}]
    
    print({"instructions": instruction_values, "cfgs": candidates_with_graph})
    # TODO, after having found function edges
    #       Find common function prologue, and if a function has multiple returns, attempt to split into multiple functions


def test(instr):
    for i, e in enumerate(instr):

        call_mask = int("".join(["1" for _ in range(4)]), 2) << (INSTR_LENGTH - 4)
        if e == "0x00EE":
            print("ADDR:",hex((512 + i*2)), "RET")
        #print(hex(512 + i*16), e)
        elif hex(int(e, 16) & call_mask) == hex(0x2000):
            print("ADDR:", hex((512 + i*2)), "CALL", e, hex(int(e, 16) & 0x0FFF))
        # else:
        #     if hex(int(e, 16) & call_mask) == hex(0xF000):
        #         print("ADDR:", (512 + i*16), "LD")
        #     elif hex(int(e, 16) & call_mask) == hex(0x8000):
        #         print("ADDR:", (512 + i*16), "math")
        #     print("ADDR:", (512 + i*16), hex(int(e, 16) & call_mask))

