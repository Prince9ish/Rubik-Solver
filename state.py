class State(object):
    def __init__(self, measurable, prev=None, payload=None, total_cost=0):
        self.measurable = measurable
        self.total_cost = total_cost
        self.prev = prev
        self.payload = payload
        self.goal = None

        self.measurable.init(self)

    def set_goal(self, goal):
        self.goal = goal
        return self

    def __lt__(self, other):
        return (self.measurable.heuristic(self.goal) + self.total_cost) < (other.measurable.heuristic(self.goal) + other.total_cost)

    def next_states(self):
        nexts = self.measurable.next_possible()
        states = []
        for next, cost, payload in nexts:
            s = State(next, self, payload, self.total_cost + cost)
            states.append(s)
        return states

    def serialize(self):
        return self.measurable.serialize()

    def __str__(self):
        return self.measurable.__str__()

    def __repr__(self):
        return self.measurable.__repr__()


class Measurable:

    def init(self, state):
        pass

    def heuristic(self, goal):
        return 0

    def next_possible(self):
        #return array of (next:Measurable, cost:number, payload?:any)
        return []

    def serialize(self):
        return ""

    def __eq__(self, other):
        return False
