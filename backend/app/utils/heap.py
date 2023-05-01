import heapq
from dataclasses import dataclass, field


@dataclass(order=True)
class SortableTuple:
    probability: float
    obj: tuple = field(compare=False)


class Heap():
    """
    Heapq wrapper class that stores only the nr_candidates most probable values
    """
    def __init__(self, nr_candidates: int) -> None:
        self.candidates: list = []
        self.nr_candidates = nr_candidates

    def add(self, candidate: tuple) -> None:
        """
        Add the tuple to the heap IFF its probability values is higher than at least
        one other element in the heap, or the heap is not at max size
        """
        sortable_candidate = SortableTuple(candidate[0], candidate)
        if len(self.candidates) <= self.nr_candidates:
            heapq.heappush(self.candidates, sortable_candidate)
        else:
            heapq.heappushpop(self.candidates, sortable_candidate)

    def values(self) -> list[tuple]:
        """
        Return the nr_candidates most probable tuple
        """
        return [e.obj for e in heapq.nlargest(self.nr_candidates, self.candidates)]
