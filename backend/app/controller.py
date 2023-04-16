from fastapi import Depends, FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as run_server

from .create_graphs import create_graphs
from .find_best_candidates import find_best_candidates
from .instructions import extract_instruction
from .models.base_form import Base, checker
from .models.instruction import Instruction

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
    run_server("app.controller:app", host="0.0.0.0", port=8000, reload=True)
