from collections import Counter
import heapq

def find_best_candidates(
        instructions, pc_inc, pc_offset, 
        nr_candidates, call_candidate_range, 
        ret_candidate_range, return_to_function_prologue_distance
    ):
    valid_call_candidates = (Counter([e.call_opcode for e in instructions])
                             .most_common(call_candidate_range[1])[call_candidate_range[0]:])
    valid_ret_candidates = ([e for e, _ in Counter([e.ret_opcode for e in instructions])
                             .most_common(ret_candidate_range[1])[ret_candidate_range[0]:]])

    hit_map = {e.ret_opcode: 0 for e in instructions}

    best_hits = []

    # hashmap (instr -> hits)   i.e 'ret' -> 10
    # TODO INSERT CALL_CANDIDATE_RANGE
    for call_candidate, counter in valid_call_candidates:
        # distance from return to prologue. 
        # I.e if ret is the instruction above call operand, distance 1 will give hits
        for step in range(1, return_to_function_prologue_distance): 
            valid_operand = 0
            for e in instructions:
                if e.call_opcode == call_candidate:
                    if (e.call_operand - step * pc_inc - pc_offset) % pc_inc != 0:
                        continue
                    valid_operand += 1
                    address = (e.call_operand - step * pc_inc - pc_offset) // pc_inc
                    if address < len(instructions):
                        hit_map[instructions[address].ret_opcode] += 1


            for ret_cand, hits in hit_map.items():
                # some random "probability" value. normalized between 0 and 1   
                probability_value = (2 * (hits / counter) + (valid_operand / counter)) / 3
                if ret_cand in valid_ret_candidates and ret_cand != call_candidate:
                    if len(best_hits) <= nr_candidates:
                        heapq.heappush(best_hits, 
                                       (probability_value, hits, counter, 
                                        call_candidate, ret_cand, step))
                    else:
                        heapq.heappushpop(best_hits, 
                                          (probability_value, hits, counter, 
                                           call_candidate, ret_cand, step))

            # reset
            for key in hit_map.keys():
                hit_map[key] = 0
    
    return heapq.nlargest(nr_candidates, best_hits)