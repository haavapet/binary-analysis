from dataclasses import asdict

from fastapi import Depends, FastAPI, File
from fastapi.middleware.cors import CORSMiddleware

from .models.base_form import Base
from .models.response_model import ControlFlowGraph, GraphNode, ResponseModel
from .services.function_detection_service import (
    filter_valid_call_edges,
    find_potential_call_edges,
    probability_of_valid_call_edges,
)
from .services.graph_service import create_graphs
from .services.instruction_service import (
    Instruction,
    extract_instructions,
    get_call_candidates_counter,
    get_ret_candidates_counter,
)
from .utils.heap import Heap

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

# TODO move this to /controllers folder, rest of services to /services
# TODO move all code inside here inside a new service (main), and just call it from controller
@app.post("/api", response_model=ResponseModel)
async def root(form: Base = Depends(), file: bytes = File(...)) -> ResponseModel:

    (instr_len, ret_len, call_len, file_offset,
     file_offset_end, pc_offset, pc_inc, endian,
     nr_cand, call_search_range, ret_search_range, ret_func_dist) = asdict(form).values()

    # Max heap that sorts based on the first value of tuple inserted (which is probability)
    candidates = Heap(nr_cand)

    # TODO this is where wer will iterate over if we need to search code entry in binary file
    # PROBLEM: different instruction values needs to be returned to frontend :((
    for i in range(1):
        instructions: list[Instruction] = extract_instructions(file[file_offset:file_offset_end],
                                                               endian,
                                                               instr_len,
                                                               call_len,
                                                               ret_len)

        for call_opcode, call_count in get_call_candidates_counter(instructions,
                                                                   call_search_range):
            # Find call edges, I.e the (address, call_address)
            # where address is the index of the call instruction, and call_address
            # is the instruction it points to
            potential_call_edges: list[tuple[int, int]] = find_potential_call_edges(instructions,
                                                                                    call_opcode,
                                                                                    pc_inc,
                                                                                    pc_offset)

            for ret_opcode, _ in get_ret_candidates_counter(instructions, ret_search_range):
                valid_call_edges = filter_valid_call_edges(instructions,
                                                           ret_opcode,
                                                           potential_call_edges,
                                                           ret_func_dist)
                probability = probability_of_valid_call_edges(len(potential_call_edges),
                                                              len(valid_call_edges),
                                                              call_count)
                candidates.append((probability, call_opcode, ret_opcode, valid_call_edges))


    # This needs to be refactored, only create graph after above for loop, but need to
    # append instruction values in above for loop
    candidates_with_graph: list[ControlFlowGraph] = []
    for prob, call, ret, valid_call_edges in candidates.values():
        graph_nodes: list[GraphNode] = create_graphs(instructions, valid_call_edges)
        graph: ControlFlowGraph = {
            "probability": prob,
            "ret_opcode": ret,
            "call_opcode": call,
            "graph": graph_nodes,
        }
        candidates_with_graph.append(graph)


    result: ResponseModel = {"instructions": instructions, "cfgs": candidates_with_graph}
    return result
