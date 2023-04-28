from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.form_data_model import FormDataModel
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api", response_model=ResponseModel)
async def root(form: FormDataModel = Depends(FormDataModel.as_form)) -> ResponseModel:

    # Max heap that sorts based on the first value of tuple inserted (which is probability)
    candidates = Heap(form.nr_cand)

    # If unknown code section, then we iterate over instr_len bits to ensure we have
    #   all possible start indices to get the correct instructions
    for bit_index in range(form.instr_len if form.unknown_code_entry else 1):
        instructions: list[Instruction] = extract_instructions(form.binary_data,
                                                               form.endiannes,
                                                               form.instr_len,
                                                               form.call_len,
                                                               form.ret_len,
                                                               bit_index)


        for call_opcode, call_count in get_call_candidates_counter(instructions,
                                                                   form.call_search_range):
            # Find call edges, I.e the (address, call_address)
            # where address is the index of the call instruction, and call_address
            # is the instruction it points to
            potential_call_edges: list[tuple[int, int]] = find_potential_call_edges(instructions,
                                                                                    call_opcode,
                                                                                    form.pc_inc,
                                                                                    form.pc_offset)

            for ret_opcode, _ in get_ret_candidates_counter(instructions, form.ret_search_range):
                valid_call_edges = filter_valid_call_edges(instructions,
                                                           ret_opcode,
                                                           potential_call_edges,
                                                           form.ret_func_dist)
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

