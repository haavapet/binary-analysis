
from dataclasses import dataclass

from fastapi import Form

# TODO update docstrings here

@dataclass
class Base:
    """ Form input for the API

    Attributes:
        instructionLength (str): (class attribute) Length of instruction in bits
        instance_attribute (str): The instance attribute
    """
    # Length of instructions in bits
    instructionLength: int = Form(...)
    # Length of return opcode in bits
    retOpcodeLength: int = Form(...)
    # Length of call opcode in bits
    callOpcodeLength: int = Form(...)
    # File offset for where code section starts (first instruction)
    fileOffset: int = Form(...)
    # File offset for where code section ends (last instruction)
    fileOffsetEnd: int = Form(...)
    # Location of first instruction in virtual memory
    pcOffset: int = Form(...)
    # How much PC increments per instruction (usually 1 per byte)
    pcIncPerInstr: int = Form(...)
    # Endiannes big/little
    endiannes: str = Form(...)
    # How many candidates/graphs to return from the API
    nrCandidates: int = Form(...)
    # Search space for call candidates,
    # [x, y] -> call instruction is among the x to y most popular instructions
    callCandidateRange: list[int] = Form(...)
    # Search space for ret candidates,
    # [x, y] -> ret instruction is among the x to y most popular instructions
    retCandidateRange: list[int] = Form(...)
    # Distance between function prologue and ret opcode of previous function.
    # If this variable is i.e 4, then we search 1,2,3,4 as distance in our search space
    returnToFunctionPrologueDistance: int = Form(...)
