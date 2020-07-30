face(['Face.TOP','Face.LEFT','Face.FRONT','Face.RIGHT','Face.BACK']).
direction(['Direction.TURN_CLOCKWISE', 'Direction.TURN_COUNTER_CLOCKWISE']).

random_actions(Actions, Count) :-
	foreach(between(1,Count,_), random_action(Actions)).

random_action(Actions) :-
	random_face(F),
	random_direction(D),
	Actions = [F,D].

random_face([], []).
random_face(Result) :-
    length(['Face.TOP','Face.LEFT','Face.FRONT','Face.RIGHT','Face.BACK'], Length),
    random(0, Length, Index),
    nth0(Index, ['Face.TOP','Face.LEFT','Face.FRONT','Face.RIGHT','Face.BACK'], Result).

random_direction([], []).
random_direction(Result) :-
    length(['Direction.TURN_CLOCKWISE', 'Direction.TURN_COUNTER_CLOCKWISE'], Length),
    random(0, Length, Index),
    nth0(Index, ['Direction.TURN_CLOCKWISE', 'Direction.TURN_COUNTER_CLOCKWISE'], Result).



