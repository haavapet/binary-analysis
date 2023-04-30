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
    get_code_start_and_end,
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

    binary_file: bytes = form.binary_data

    # Do not include instructions for files greater than 1mb
    if len(binary_file) > 10**6:
        form.do_not_include_instruction = True

    possible_code_start_end: list[tuple[int, int]] = get_code_start_and_end(len(binary_file),
                                                                            form.instr_len,
                                                                            form.unknown_code_entry,
                                                                            form.file_offset,
                                                                            form.file_offset_end)

    for start, end in possible_code_start_end:
        instructions: list[Instruction] = extract_instructions(binary_file[start:end],
                                                               form.endiannes,
                                                               form.instr_len,
                                                               form.call_len,
                                                               form.ret_len)

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
                valid_call_edges: list[tuple[int, int]] = filter_valid_call_edges(instructions,
                                                                                  ret_opcode,
                                                                                  potential_call_edges,
                                                                                  form.ret_func_dist)
                probability = probability_of_valid_call_edges(len(potential_call_edges),
                                                              len(valid_call_edges),
                                                              call_count)
                candidates.add((probability,
                                call_opcode,
                                ret_opcode,
                                valid_call_edges,
                                instructions))

    # This needs to be refactored, only create graph after above for loop, but need to
    # append instruction values in above for loop
    control_flow_graphs: list[ControlFlowGraph] = []
    for prob, call, ret, valid_call_edges, instructions in candidates.values():
        graph_nodes: list[GraphNode] = create_graphs(instructions, valid_call_edges)

        graph: ControlFlowGraph = {
            "instructions": instructions if not form.do_not_include_instruction  else [],
            "probability": prob,
            "ret_opcode": ret,
            "call_opcode": call,
            "graph": graph_nodes,
        }
        control_flow_graphs.append(graph)

    result: ResponseModel = {"cfgs": control_flow_graphs}
    return result

