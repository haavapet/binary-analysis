from dataclasses import astuple, dataclass
from typing import Iterator

import uvicorn
from create_graphs import create_graphs
from fastapi import Depends, FastAPI, File, Form, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from find_best_candidates import find_best_candidates
from instructions import Instruction, extract_instruction
from pydantic import BaseModel, ValidationError

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/api")
async def root(form: Base = Depends(checker), file: bytes = File(...)) -> dict:
    (instr_len, ret_len, call_len, file_offset,
     file_offset_end, pc_offset, pc_inc, endian,
     nr_cand, call_range, ret_range, ret_func_dist) = form

    instruction_values = extract_instruction(file[file_offset:file_offset_end], endian, instr_len)
    instructions = [Instruction(e, instr_len, ret_len, call_len) for e in instruction_values]

    candidates = find_best_candidates(instructions, pc_inc, pc_offset, nr_cand,
                                      call_range, ret_range, ret_func_dist)

    candidates_with_graph = []
    for prob, _, _, call, ret, step in candidates:
        graph = create_graphs(instructions, call, ret, pc_inc, pc_offset, step)
        candidates_with_graph.append([{"probability": prob, "ret_opcode": ret,
                                       "call_opcode": call, "graph": graph}])

    return {"instructions": instruction_values, "cfgs": candidates_with_graph}

def start() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.controller:app", host="0.0.0.0", port=8000, reload=True)
