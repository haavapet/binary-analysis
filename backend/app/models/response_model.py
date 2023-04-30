from typing import TypedDict

from ..services.instruction_service import Instruction


class GraphNode(TypedDict):
    start: int
    end: int
    f_id: int
    calls_f_id: list[int]

class ControlFlowGraph(TypedDict):
    instructions: list[Instruction]
    probability: float
    ret_opcode: int
    call_opcode: int
    graph: list[GraphNode]

class ResponseModel(TypedDict):
    cfgs: list[ControlFlowGraph]
