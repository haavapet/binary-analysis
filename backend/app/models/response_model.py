from typing import TypedDict

from ..services.instruction_service import Instruction


class GraphNode(TypedDict):
    start: int
    end: int
    f_id: int
    calls_f_id: list[int]

class ControlFlowGraph(TypedDict):
    probability: float
    ret_opcode: int
    call_opcode: int
    graph: list[GraphNode]

class ResponseModel(TypedDict):
    instructions: list[Instruction]
    cfgs: list[ControlFlowGraph]
