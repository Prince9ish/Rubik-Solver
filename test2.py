from __future__ import print_function,division
from searcher import *
from rubik import *
from graphics import GUI
from cube import Cube
from pyswip import Prolog

class RubikMeasurable(Measurable):

    def __init__(self, rubik):
        self.goal = Rubik
        self.rubik = rubik

    def init(self, state):
        state.set_goal(Rubik().standard())

    def heuristic(self, goal):
        h = self.rubik.compare_to(goal)
        #print("              " + str(h))
        return h

    def next_possible(self):
        actions = Action.all_possible_actions()
        cost = 21
        return [(
            RubikMeasurable(action.exec(self.rubik.clone())), cost, action
        ) for action in actions]

    def serialize(self):
        return self.rubik.serialize()

    def __eq__(self, other):
        return self.serialize() == other.serialize()

    def __repr__(self):
        return self.rubik.serialize()


searcher = Searcher()

rubik1 = RubikFacade(Rubik().standard())
print(rubik1)
rubik2 = Rubik().standard()

randomList = []

def isEmpty(lst):
    return len(lst) == 0

def readResult(rList, var):
    read = list(rList)[0][var]
    pair=[]
    for i in read:
        pair.append(str(i))
    return { pair[0] : pair[1] }

# def randomRubik(time):
#     for i in range(time):
#         a = prolog.query("random_action(X)")
#         randomList.append(readResult(a, "X"))

#prolog = Prolog()
#prolog.consult("Random.pl")
#randomRubik(3)

for item in randomList:
    f = list(item.keys())[0]
    d = list(item.values())[0]
    #print(f, d)
    rubik2.get_face(eval(f)).turn(eval(d))


rubik2 = RubikFacade(rubik2)
step = rubik2.random(3)
print(rubik2)


# rubik2 = RubikFacade(Rubik().standard())
#rubik2.top().c()
#rubik2.left().c()
#rubik2.top().cc()
#rubik2.right().cc()

init = RubikMeasurable(rubik1.to_rubik())
goal = RubikMeasurable(rubik2.to_rubik())

results = searcher.search(init, goal)

c=Cube()
graphics=GUI(c)
c.registerGraphicsHandler(graphics)
c.startRecording()

print(step)
c.action('X Z X Z Z')
#for i in step:
    #c.action(i.translate())

print(RubikFacade(rubik2.to_rubik()))
result = []

print(step)
for rubik, action in results:
    #print(action.get_reverse_action(), rubik)
    print("-----------------------------------")
    print("Step - " + str(action.get_reverse_action()))
    #result.append((action.get_reverse_action()).translate())
    print(RubikFacade(rubik.rubik))
    print("-----------------------------------")

graphics.begin1(result)

