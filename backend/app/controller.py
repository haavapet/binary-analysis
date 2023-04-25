from dataclasses import asdict

from fastapi import Depends, FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as run_server

from .create_graphs import create_graphs
from .extract_instructions import extract_instruction
from .find_best_candidates import Candidate, find_best_candidates
from .models.base_form import Base
from .models.instruction import Instruction
from .models.response_model import ControlFlowGraph, GraphNode, ResponseModel

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


@app.post("/api", response_model=ResponseModel)
async def root(form: Base = Depends(), file: bytes = File(...)) -> ResponseModel:

    (instr_len, ret_len, call_len, file_offset,
     file_offset_end, pc_offset, pc_inc, endian,
     nr_cand, call_range, ret_range, ret_func_dist) = asdict(form).values()

    instruction_values: list[int] = extract_instruction(file[file_offset:file_offset_end],
                                                        endian,
                                                        instr_len)

    instructions: list[Instruction] = [Instruction(e, instr_len, ret_len, call_len)
                                       for e in instruction_values]


    candidates: list[Candidate] = find_best_candidates(instructions,
                                                       pc_inc,
                                                       pc_offset,
                                                       nr_cand,
                                                       call_range,
                                                       ret_range,
                                                       ret_func_dist)

    candidates_with_graph: list[ControlFlowGraph] = []
    for prob, _, _, call, ret, step in candidates:
        graph_nodes: list[GraphNode] = create_graphs(instructions, call, ret,
                                                     pc_inc, pc_offset, step)
        graph: ControlFlowGraph = {
            "probability": prob,
            "ret_opcode": ret,
            "call_opcode": call,
            "graph": graph_nodes,
        }
        candidates_with_graph.append(graph)


    result: ResponseModel = {"instructions": instruction_values, "cfgs": candidates_with_graph}
    return result

def start() -> None:
    """Launched with `poetry run start` at root level"""
    run_server("app.controller:app", host="0.0.0.0", port=8000, reload=True)
