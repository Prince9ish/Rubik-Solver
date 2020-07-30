from queue import PriorityQueue
from state import *


class Searcher:

    def __init__(self):
        self.states = []
        self.queue = PriorityQueue()

    def search(self, init, goal, limit=10000000):
        init_state = State(init)
        self.queue.put(init_state)
        round = 0
        while not self.queue.empty():
            cur = self.queue.get()

            limit -= 1
            if limit <= 0:
                print("NO!")
                print(self._add_to_queue(s))
                break

            if cur.measurable == goal:
                print("GOAL!")
                return self._reverse_result(cur)

            next_state = filter(lambda state: not self._is_state_existed(state), cur.next_states())

            # print("next_state: ")
            for s in next_state:
                # print(s)
                self._add_to_queue(s)

            print(round, self.queue.qsize())
            round += 1

        return None

    def _reverse_result(self, state):
        results = []
        while state is not None and state.payload is not None:
            results.append((state.measurable, state.payload))
            state = state.prev
        return filter(lambda x: x is not None, results)

    def _add_to_queue(self, state):
        self.queue.put(state)
        self.states.append(state.serialize())

    def _is_state_existed(self, state):
        key = state.serialize()
        return key in self.states
