from typing import TypedDict


class GraphNode(TypedDict):
    start: int
    end: int
    f_id: int
    calls_f_id: set[int]

class ControlFlowGraph(TypedDict):
    probability: float
    ret_opcode: int
    call_opcode: int
    graph: list[GraphNode]

class ResponseModel(TypedDict):
    instructions: list[int]
    cfgs: list[ControlFlowGraph]
