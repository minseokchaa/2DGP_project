#이벤트 체크 함수를 정의
# 상태이벤트 e = (종류, 실제 값) 튜플로 정의
from tabnanny import check

from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_d


def start_event(e):
    return e[0] == 'START'
    pass

def space_down(e):       # e가 space down 인지 판단? true or false
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key ==SDLK_SPACE

def space_up(e):       # e가 space down 인지 판단? true or false
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key ==SDLK_SPACE

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def a_down(e):       # e가 space down 인지 판단? true or false
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def d_down(e):       # e가 space down 인지 판단? true or false
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def d_up(e):       # e가 space down 인지 판단? true or false
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def time_out(e):         #e가 time out인지 판단
    return e[0] == 'TIME_OUT'

def landing(e):         #e가 time out인지 판단
    return e[0] == 'LAND'

def attack_end(e):         #e가 time out인지 판단
    return e[0] == 'Attack_end'

def no_stamina(e):         #e가 time out인지 판단
    return e[0] == 'No_stamina'

def out_of_width(e):         #e가 time out인지 판단
    return e[0] == 'OUT_OF_WIDTH'




class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []

    def start(self, state):
        self.cur_state = state

        print(f'Enter into {state}')
        self.cur_state.enter(self.o, ('START', 0))

    def add_event(self, e):
        # print(f'    DEBUG: New event {e} added to event Que')
        self.event_que.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.o)

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                print(f'Exit from {self.cur_state}')
                self.cur_state.exit(self.o, e)
                self.cur_state = next_state
                print(f'Enter into {self.cur_state}')
                self.cur_state.enter(self.o, e)
                return

        # print(f'        Warning: Event [{e}] at State [{self.cur_state}] not handled')