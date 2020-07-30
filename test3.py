from rubik import *
from queue import Queue

set = {None}
rubik = Rubik().standard()
actions = Action.all_possible_actions()

q = Queue()
q.put(rubik)
while not q.empty():
    print(len(set))
    next = q.get()
    s = next.serialize()
    if s in set:
        continue
    for action in actions:
        n = next.clone()
        action.exec(n)
        q.put(n)