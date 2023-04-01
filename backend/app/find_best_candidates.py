from collections import Counter
from constants import *
import heapq

def find_best_candidates(instructions, pc_inc_per_instruction, pc_offset, nr_candidates):
    call_counter = Counter([e.call_opcode for e in instructions])

    hit_map = {e.ret_opcode: 0 for e in instructions}

    best_hits = []

    # hashmap (instr -> hits)   i.e 'ret' -> 10
    # TODO INSERT CALL_CANDIDATE_RANGE
    for call_candidate, counter in call_counter.most_common(7):
        # TODO insert RETURN TO FUNCTION PROLOGUE DISTANCE
        for step in range(1, 3): # distance from return to prologue. I.e if ret is the instruction above call operand, distance 1 will give hits
            valid_operand = 0
            for e in instructions:
                if e.call_opcode == call_candidate:
                    if (e.call_operand - step * pc_inc_per_instruction - pc_offset) % pc_inc_per_instruction != 0:
                        continue
                    valid_operand += 1
                    address = (e.call_operand - step * pc_inc_per_instruction - pc_offset) // pc_inc_per_instruction
                    if address < len(instructions):
                        hit_map[instructions[address].ret_opcode] += 1


            for ret_cand, hits in hit_map.items():
                # TODO: use RET_CANDIDATE_RANGE and check that opcode is popular
                # some random "probability" value. normalized between 0 and 1   
                probability_value = (2 * (hits / counter) + (valid_operand / counter)) / 3
                if len(best_hits) <= nr_candidates:
                    heapq.heappush(best_hits, (probability_value, hits, counter, call_candidate, ret_cand, step))
                else:
                    heapq.heappushpop(best_hits, (probability_value, hits, counter, call_candidate, ret_cand, step))

            # reset
            for key in hit_map.keys():
                hit_map[key] = 0
    
    return heapq.nlargest(nr_candidates, best_hits)