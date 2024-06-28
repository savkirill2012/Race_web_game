from enum import Enum
from random import randrange
from copy import deepcopy


IN = 1
OUT = 0
DEFAULT_ROW = [IN, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, IN]
CAR_X = 5
CAR_Y = 14
DEFAULT_CAR_POS = [
        [CAR_Y-1, CAR_X],
        [CAR_Y, CAR_X-1], [CAR_Y, CAR_X], [CAR_Y, CAR_X+1],
        [CAR_Y+1, CAR_X],
        [CAR_Y+2, CAR_X-1], [CAR_Y+2, CAR_X], [CAR_Y+2, CAR_X+1]
    ]


class Action(Enum):
    START = 1
    PAUSE = 2
    TERMINATE = 3
    LEFT = 4
    RIGTH = 5
    UP = 6
    DOWN = 7
    ACTION = 8


class Car():
    def __init__(self):
        self.car_pos = deepcopy(DEFAULT_CAR_POS)
        self.prev_car_pos = deepcopy(DEFAULT_CAR_POS)

    def _copy_car_pos(self):
        self.prev_car_pos = deepcopy(self.car_pos)

    def move_rigth(self):
        self._copy_car_pos()
        if self.car_pos[3][1] != 9:
            for elem in self.car_pos:
                elem[1] += 1

    def move_left(self):
        self._copy_car_pos()
        if self.car_pos[1][1] != 1:
            for elem in self.car_pos:
                elem[1] -= 1

    def move_up(self):
        self._copy_car_pos()
        if self.car_pos[0][0] != 0:
            for elem in self.car_pos:
                elem[0] -= 1

    def move_down(self):
        self._copy_car_pos()
        if self.car_pos[6][0] != 19:
            for elem in self.car_pos:
                elem[0] += 1

    def to_default(self):
        self.car_pos = deepcopy(DEFAULT_CAR_POS)
        self.prev_car_pos = deepcopy(DEFAULT_CAR_POS)


class State():
    def __init__(self):
        self.field: list[list] = [DEFAULT_ROW[:] for _ in range(20)]
        self.next: list[list] = [DEFAULT_ROW[:] for _ in range(20)]
        self.score: int = 0
        self.higthScore: int = 0
        self.level: int = 1
        self.speed: int = 1
        self.pause: bool = 0
        self.shift_new_row = 0
        self.cycle: int = 0
        self.car = Car()

    def state_to_default(self):
        if self.score > self.higthScore:
            self.higthScore = self.score
        self.score = 0
        self.speed = 1
        self.pause = 1
        self.field = self.next[:]
        self.shift_new_row = 0
        self.cycle = 0
        self.car.to_default()


def _car_pos_upd(state: State):
    for elem in state.car.prev_car_pos:
        state.field[elem[0]][elem[1]] = OUT

    for elem in state.car.car_pos:
        if state.field[elem[0]][elem[1]] == IN:
            state.state_to_default()
            break
        else:
            state.field[elem[0]][elem[1]] = IN

    return state


def userInput(action: Action, hold: bool, state: State) -> State:
    print('inloop')
    print(action)
    if action == Action.PAUSE.value:
        state.pause = 1
    elif action == Action.START.value:
        state.pause = 0

    if state.pause == 0:
        if action == Action.TERMINATE.value:
            for elem in state.car.car_pos:
                state.field[elem[0]][elem[1]] = OUT
            state.state_to_default()
            state.pause = 0
        elif action == Action.LEFT.value:
            state.car.move_left()
            state = _car_pos_upd(state)
        elif action == Action.RIGTH.value:
            state.car.move_rigth()
            state = _car_pos_upd(state)
        elif action == Action.UP.value:
            state.car.move_up()
            state = _car_pos_upd(state)
        elif action == Action.DOWN.value:
            state.car.move_down()
            state = _car_pos_upd(state)

    return state


def _check_to_get_score(state: State):
    last_row = state.field[-1][1:-1]
    bf_last_row = state.field[-2][1:-1]

    for i in range(1, len(last_row) - 1):
        if last_row[i] == IN and bf_last_row[i] == OUT and \
                last_row[i + 1] == OUT and last_row[i - 1] == OUT:
            state.score += 10


def _gen_new_row(state: State) -> list[bool]:
    cur_cycle = state.cycle % 14
    ret_row = DEFAULT_ROW[:]

    if cur_cycle == 0:
        state.shift_new_row = randrange(0, 3)

    if cur_cycle < 5:
        if cur_cycle % 2 == 0:
            ret_row[2 + state.shift_new_row * 3] = IN
        else:
            ret_row[1 + state.shift_new_row * 3] = IN
            ret_row[state.shift_new_row * 3 + 2] = IN
            ret_row[state.shift_new_row * 3 + 3] = IN

    state.cycle += 1

    return ret_row


def updateCurrentState(state: State) -> State:
    if state.pause == 0:
        for elem in state.car.car_pos:
            state.field[elem[0]][elem[1]] = OUT

        new_row = _gen_new_row(state)

        for i in range(19, 0, -1):
            state.field[i] = state.field[i-1]
        state.field[0] = new_row

        for elem in state.car.car_pos:
            if state.field[elem[0]][elem[1]] == IN:
                state.state_to_default()
                break
            else:
                state.field[elem[0]][elem[1]] = IN

        _check_to_get_score(state)
        state.speed = state.score // 100 + 1

    return state
