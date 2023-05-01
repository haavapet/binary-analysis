from ..app.services.function_detection_service import (
    filter_valid_call_edges,
    find_potential_call_edges,
    probability_of_valid_call_edges,
)
from ..app.services.instruction_service import Instruction


def test_probability() -> None:
    assert probability_of_valid_call_edges(42, 42, 42) == 1

    assert probability_of_valid_call_edges(0, 0, 42) == 0

    assert probability_of_valid_call_edges(30, 40, 42) > 0.7


def test_valid_call_edges() -> None:
    # calls to first instruction are valid
    instructions = [Instruction(0x1000, 16, 4, 4),
                    Instruction(0x1000, 16, 4, 4),
                    Instruction(0x1000, 16, 4, 4)]
    assert filter_valid_call_edges(instructions, 0, [(2, 0)], 1)

    # Instruction index 1 is called by instruction index 4,
    # the instruction before index 1 is a valid return opcode
    instructions = [Instruction(0x1000, 16, 4, 4),
                    Instruction(0x0000, 16, 4, 4),
                    Instruction(0x0000, 16, 4, 4),
                    Instruction(0x0000, 16, 4, 4),
                    Instruction(0x2000, 16, 4, 4)]
    assert filter_valid_call_edges(instructions, 0x1000, [(4, 1)], 1) == [(4, 1)]

    # same as above but now there is no valid return before it, thus not valid
    instructions = [Instruction(0x0000, 16, 4, 4),
                    Instruction(0x0000, 16, 4, 4),
                    Instruction(0x0000, 16, 4, 4),
                    Instruction(0x0000, 16, 4, 4),
                    Instruction(0x2000, 16, 4, 4)]
    assert filter_valid_call_edges(instructions, 0x1000, [(4, 1)], 1) == []


def test_potential_call_edges() -> None:
    # calls to first instruction are potential
    instructions = [Instruction(0x0000, 16, 4, 4),
                     Instruction(0x0000, 16, 4, 4),
                     Instruction(0x2000, 16, 4, 4)]
    assert find_potential_call_edges(instructions, 0x2000, 1, 0) == [(2, 0)]

    # no potential calls
    instructions = [Instruction(0x0000, 16, 4, 4),
                     Instruction(0x0000, 16, 4, 4),
                     Instruction(0x0000, 16, 4, 4)]
    assert find_potential_call_edges(instructions, 0x2000, 1, 0) == []

