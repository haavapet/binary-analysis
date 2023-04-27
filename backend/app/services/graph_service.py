from ..models.response_model import GraphNode
from .instruction_service import Instruction


# TODO make step be max distance and not exact distance, for better modularity
def create_graphs(
        instrs: list[Instruction],
        valid_call_edges: list[tuple[int, int]],
    ) -> list[GraphNode]:

    # Assume first instruction is entry point, and take unique function prologues and sort them
    function_prologues = sorted({0} | {end for _, end in valid_call_edges})

    # list of nodes of function blocks
    function_blocks: list[GraphNode] = []

    # fill function block values of all instructions in a function block
    fbs = zip(function_prologues, function_prologues[1:] + [len(instrs)])
    for i, (start, end) in enumerate(fbs):
        calls = set()
        for from_edge, to_edge in valid_call_edges:
            if start < from_edge < end:
                calls.add(function_prologues.index(to_edge))

        function_blocks += [GraphNode({
                                        "f_id": i,
                                        "start": start,
                                        "end": end,
                                        "calls_f_id": list(calls),
                                      })]

    return function_blocks
