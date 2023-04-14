from fastapi import FastAPI, status, Form, File, Depends
from pydantic import BaseModel, ValidationError
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from instructions import Instruction, extract_instruction
from create_graphs import create_graphs
from find_best_candidates import find_best_candidates

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


def checker(data: str = Form(...)):
    try:
        model = Base.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return model

@app.post("/api")
async def root(form: Base = Depends(checker), file: bytes = File(...)):
    instruction_values = extract_instruction(file[form.fileOffset:form.fileOffsetEnd], form.endiannes, form.instructionLength)
    instructions = [Instruction(e, form.instructionLength, form.retOpcodeLength, form.callOpcodeLength) for e in instruction_values]

    candidates = find_best_candidates(instructions, form.pcIncPerInstr, form.pcOffset, form.nrCandidates, form.callCandidateRange, form.retCandidateRange, form.returnToFunctionPrologueDistance)

    candidates_with_graph = []
    for prob, _, _, call, ret, step in candidates:
        graph = create_graphs(instructions, call, ret, form.pcIncPerInstr, form.pcOffset, step)
        candidates_with_graph += [{"probability": prob, "ret_opcode": ret, "call_opcode": call, "graph": graph}]
    
    return {"instructions": instruction_values, "cfgs": candidates_with_graph}