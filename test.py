from rubik import *

rubik = Rubik().standard()
# rubik = Rubik().from_serialize_str("yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww")
print(rubik.serialize())

print(rubik)
print("=" * 100)

rubik.get_face(Face.FRONT).turn(Direction.TURN_CLOCKWISE)
rubik.get_face(Face.FRONT).turn(Direction.TURN_CLOCKWISE)
print(rubik)
print("=" * 100)

rubik.get_face(Face.BACK).turn(Direction.TURN_COUNTER_CLOCKWISE)
rubik.get_face(Face.BACK).turn(Direction.TURN_COUNTER_CLOCKWISE)
print(rubik)
print("=" * 100)

rubik.get_face(Face.TOP).turn(Direction.TURN_CLOCKWISE)
rubik.get_face(Face.TOP).turn(Direction.TURN_CLOCKWISE)
print(rubik)
print("=" * 100)


#with facade
rubik2 = rubik.clone()
rubik2 = RubikFacade(rubik2)
rubik2.bottom().counter_clockwise()
rubik2.bottom().counter_clockwise()

rubik2.left().clockwise()
rubik2.left().clockwise()

rubik2.right().counter_clockwise()
rubik2.right().counter_clockwise()

print(rubik2)
print("=" * 100)

print(rubik2.to_rubik().serialize())

#random
rubik3 = RubikFacade(Rubik().standard())
print(rubik3.random(3))
print(rubik3)
print(rubik3.to_rubik().serialize())
print("=" * 100)
