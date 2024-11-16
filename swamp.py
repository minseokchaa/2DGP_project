from pico2d import *
from state_machine import StateMachine, right_down, left_down, left_up, right_up, d_down, a_down, out_of_width
import server

WIDTH =960
HEIGHT = 800

class bg_Idle:

    @staticmethod
    def enter(Bg_swamp, e):
        pass

    @staticmethod
    def exit(Bg_swamp,e):
            pass

    @staticmethod
    def do(Bg_swamp):
        pass

    @staticmethod
    def draw(Bg_swamp):
        Bg_swamp.Back_ground_swamp.draw(Bg_swamp.x, HEIGHT // 2)
        pass

class bg_move:

    @staticmethod
    def enter(Bg_swamp, e):
        if right_down(e):
            Bg_swamp.move_x = -1
        if right_up(e):
            Bg_swamp.move_x = 0
        elif left_down(e):
            Bg_swamp.move_x = 1
        if left_up(e):
            Bg_swamp.move_x = 0
        pass

    @staticmethod
    def exit(Bg_swamp,e):
            pass

    @staticmethod
    def do(Bg_swamp):
        if WIDTH > Bg_swamp.x + Bg_swamp.scroll_speed * Bg_swamp.move_x > -1920 + WIDTH*2:
            Bg_swamp.x += Bg_swamp.scroll_speed * Bg_swamp.move_x
        else:
            Bg_swamp.state_machine.add_event(('OUT_OF_WIDTH', 0))
        pass

    @staticmethod
    def draw(Bg_swamp):
        Bg_swamp.Back_ground_swamp.draw(Bg_swamp.x, HEIGHT // 2)
        pass

class Bg_swamp:

    def __init__(self):

        self.x = WIDTH
        self.Back_ground_swamp = load_image('bg_tile_chapter_02_02x2.png')
        self.scroll_speed = 2
        self.move_x = 0
        self.state_machine = StateMachine(self)  # 늪배경 객체의 state machine 생성
        self.state_machine.start(bg_Idle)
        self.state_machine.set_transitions(
            {bg_Idle: {right_down: bg_move, left_down:bg_move},
             bg_move: {right_up: bg_Idle, left_up: bg_Idle, a_down: bg_Idle, d_down: bg_Idle, out_of_width: bg_Idle}
             }
        )
        pass
    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()

class Tile_ground_swamp:
    def __init__(self):

        self.tile_swamp = load_image('tile_chapter_0000_tile1_.png')

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.tile_swamp.w
        self.h = self.tile_swamp.h


    def draw(self):
        self.tile_swamp.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.ch // 2, self.h - self.ch - 1)


