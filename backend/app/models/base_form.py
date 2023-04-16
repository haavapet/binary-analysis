from dataclasses import astuple, dataclass
from typing import Iterator

from fastapi import Form, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ValidationError


@dataclass
class Base(BaseModel):
    instructionLength: int
    retOpcodeLength: int
    callOpcodeLength: int
    fileOffset: int
    fileOffsetEnd: int
    pcOffset: int
    pcIncPerInstr: int
    endiannes: str
    nrCandidates: int
    callCandidateRange: list
    retCandidateRange: list
    returnToFunctionPrologueDistance: int

    def __iter__(self: "Base") -> Iterator:
        return iter(astuple(self))


def checker(data: str = Form(...)) -> Base:
    try:
        model = Base.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return model
