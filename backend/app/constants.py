FILENAME = 'quar.ch8'
# TODO there is both file offset to read from, and also "PC offset ish thingy", i.e we need to offset 0x200 when converting operand to address, but not when reading file
FILE_OFFSET = 0x200
FILE_OFFSET_END = 0xAAA
INSTR_LENGTH = 16
PC_INC_PER_INSTR = 2 # how much PC increments per instruction, usually byter per instruction, but not sure
ENDIANNES = "little"
NR_CANDIDATES = 4

# INFO NEEDED
# file name, eg binary.exe
# Instruction length, eg. 16 bits
# ret opcode length, eg. 16 bits
# call opcode length, eg 8 bits.
# where code starts in binary file, eg adress 0x260
# endianness, big or little