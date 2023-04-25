from ..app.find_best_candidates import find_best_candidates
from .binary_data import get_test_instructions


def test_find_best_candidate() -> None:
    instructions = get_test_instructions()

    candidates = find_best_candidates(instructions, 2, 0x200, 1, [0, 10], [0, 10], 5)

    _, _, _, call_cand, ret_cand, _ = candidates[0]

    # Top candidate should have 0x2000 as call candidate
    assert call_cand == 0x2000

    # Top candidate should have 0x00EE as ret candidate
    assert ret_cand == 0x00EE
