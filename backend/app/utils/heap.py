import heapq
from dataclasses import dataclass, field


@dataclass(order=True)
class SortableTuple:
    probability: float
    obj: tuple = field(compare=False)


class Heap():
    def __init__(self, nr_candidates: int) -> None:
        self.candidates: list = []
        self.nr_candidates = nr_candidates

    def append(self, candidate: tuple) -> None:
        sortable_candidate = SortableTuple(candidate[0], candidate)
        if len(self.candidates) <= self.nr_candidates:
            heapq.heappush(self.candidates, sortable_candidate)
        else:
            heapq.heappushpop(self.candidates, sortable_candidate)

    def values(self) -> list[tuple]:
        return [e.obj for e in heapq.nlargest(self.nr_candidates, self.candidates)]
