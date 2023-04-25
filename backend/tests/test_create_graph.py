from ..app.create_graphs import create_graphs
from .binary_data import get_test_instructions


def test_create_graph() -> None:
    instructions = get_test_instructions()

    graph = create_graphs(instructions, 0x2000, 0x00EE, 2, 0x200, 1)

    # There are 19 functions in total
    assert len(graph) == 19

    # Function 1 calls all function ids in the tuple below
    for f_id in (2, 6, 7, 8, 9, 10, 1, 11, 3):
        assert f_id in graph[0]["calls_f_id"]

    # The first function starts with instruction 0 and ends with 199
    assert graph[0]["start"] == 0
    assert graph[0]["end"] == 199
