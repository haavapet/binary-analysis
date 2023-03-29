from fastapi import FastAPI, status, Form, UploadFile, File, Depends, Request
from pydantic import BaseModel, ValidationError
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from fastapi.middleware.cors import CORSMiddleware

from program import find_hits, create_graph
from instructions import Instruction, extract_instruction

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


def checker(data: str = Form(...)):
    try:
        model = Base.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return model

@app.get("/")
async def test():
    return "test"

@app.post("/api")
async def root(form: Base = Depends(checker), file: bytes = File(...)):

    # TODO: make docker stuff
    result = {"cfgs": []}
    instr2 = [Instruction(e, 16, 4) for e in extract_instruction(file, "big", form.instructionLength)[:536]] # slicing because end of binary is sprites
    result["instructions"] = [e.value for e in instr2]
    candidates = find_hits(instr2, 16, 4)

    for prob, hits, nr_call_opcodes, call, ret, step in candidates:
        #print(f"prob: {prob}, hits: {hits}, nr_calls: {nr_call_opcodes}. call opcode: {call}, ret opcode: {ret}")
        graph = create_graph(instr2, call, ret, step)
        result["cfgs"].append({"probability": prob, "ret_opcode": ret, "call_opcode": call, "graph": graph})

    return result