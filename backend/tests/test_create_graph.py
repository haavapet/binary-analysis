from ..app.services.graph_service import create_graphs
from .binary_data import get_test_instructions, get_test_valid_call_edges


def test_create_graph() -> None:
    instructions = get_test_instructions()
    valid_call_edges = get_test_valid_call_edges()


    graph = create_graphs(instructions, valid_call_edges)

    # There are 19 functions in total
    assert len(graph) == 19

    # Function 1 calls all function ids in the tuple below
    assert all(f_id in graph[0]["calls_f_id"] for f_id in (2, 6, 7, 8, 9, 10, 1, 11, 3))

    # The first function starts with instruction 0 and ends with 199
    assert graph[0]["start"] == 0
    assert graph[0]["end"] == 199
