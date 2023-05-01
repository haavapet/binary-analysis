from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.form_data_model import FormDataModel
from .models.response_model import ControlFlowGraph, ResponseModel
from .services.function_detection_service import (
    filter_valid_call_edges,
    find_potential_call_edges,
    probability_of_valid_call_edges,
)
from .services.graph_service import create_graphs
from .services.instruction_service import (
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

    # Get the binary data
    binary_data = form.binary_data

    # Get either (form.file_offset, form.file_offset_end) or a list of tuples of possible offsets
    possible_code_start_end = get_code_start_and_end(len(binary_data),
                                                     form.instr_len,
                                                     form.unknown_code_entry,
                                                     form.file_offset,
                                                     form.file_offset_end)

    # For byte alignment, ie if instrlen is 16 we iterate over 0 and 1 to get the correct alignment
    for byte_index in range(form.instr_len // 8):

        # Extract instructions based on byte alignment
        instructions = extract_instructions(binary_data[byte_index:],
                                            form.endiannes,
                                            form.instr_len,
                                            form.call_len,
                                            form.ret_len)

        # Iterate over all possible file offsets
        for start, end in possible_code_start_end:

            # Get the correct slice of instructions
            current_instructions = instructions[start:end]

            # Iterate over possible call candidates based on the range provided
            for call_opcode, call_count in get_call_candidates_counter(current_instructions,
                                                                       form.call_search_range):

                # Find potential edges for the call instructions
                potential_call_edges = find_potential_call_edges(current_instructions,
                                                                 call_opcode,
                                                                 form.pc_inc,
                                                                 form.pc_offset)

                # Iterate over possible ret candidates based on the range provided
                for ret_opcode, _ in get_ret_candidates_counter(current_instructions,
                                                                form.ret_search_range):

                    # Determine if the potential call edges are valid, i.e close enough to a return
                    valid_call_edges = filter_valid_call_edges(current_instructions,
                                                               ret_opcode,
                                                               potential_call_edges,
                                                               form.ret_func_dist)

                    # Calculate probability of this combination of call and ret being correct
                    probability = probability_of_valid_call_edges(len(potential_call_edges),
                                                                  len(valid_call_edges),
                                                                  call_count)

                    # Add to the heap
                    candidates.add((probability,
                                    call_opcode,
                                    ret_opcode,
                                    valid_call_edges,
                                    current_instructions))


    control_flow_graphs = []

    # Iterate over all candidates remaining in heap and create graph
    for prob, call, ret, valid_call_edges, instructions in candidates.values():
        graph_nodes = create_graphs(instructions, valid_call_edges)

        graph: ControlFlowGraph = {
            "instructions": instructions if form.include_instruction  else [],
            "probability": prob,
            "ret_opcode": ret,
            "call_opcode": call,
            "graph": graph_nodes,
        }
        control_flow_graphs.append(graph)

    return {"cfgs": control_flow_graphs}
