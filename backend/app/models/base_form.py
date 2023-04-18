
from dataclasses import dataclass

from fastapi import Form


@dataclass
class Base:
    instructionLength: int = Form(...)
    retOpcodeLength: int = Form(...)
    callOpcodeLength: int = Form(...)
    fileOffset: int = Form(...)
    fileOffsetEnd: int = Form(...)
    pcOffset: int = Form(...)
    pcIncPerInstr: int = Form(...)
    endiannes: str = Form(...)
    nrCandidates: int = Form(...)
    callCandidateRange: list[int] = Form(...)
    retCandidateRange: list[int] = Form(...)
    returnToFunctionPrologueDistance: int = Form(...)
