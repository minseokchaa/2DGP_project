from pico2d import load_image
from state_machine import StateMachine, right_down, left_down, left_up, right_up, d_down, a_down, out_of_width

WIDTH =960
HEIGHT = 800

class Idle:

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

class background_move:

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
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            { Idle: {right_down: background_move, left_down:background_move},
              background_move: {right_up: Idle, left_up: Idle, a_down: Idle, d_down: Idle, out_of_width: Idle}
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

class Tile_Idle:

    @staticmethod
    def enter(tile_ground_swamp, e):
        pass

    @staticmethod
    def exit(tile_ground_swamp,e):
            pass

    @staticmethod
    def do(tile_ground_swamp):
        pass

    @staticmethod
    def draw(tile_ground_swamp):
        for i in range(37):
            tile_ground_swamp.tile_swamp.draw(tile_ground_swamp.x + 128 * i, 50, 192, 136)
        pass

class Tile_move:

    @staticmethod
    def enter(tile_ground_swamp, e):
        if right_down(e):
            tile_ground_swamp.move_x = -1
        if right_up(e):
            tile_ground_swamp.move_x = 0
        elif left_down(e):
            tile_ground_swamp.move_x = 1
        if left_up(e):
            tile_ground_swamp.move_x = 0
        pass

    @staticmethod
    def exit(tile_ground_swamp,e):
            pass

    @staticmethod
    def do(tile_ground_swamp):
        if 0 < tile_ground_swamp.world - tile_ground_swamp.scroll_speed * tile_ground_swamp.move_x <1920:
            tile_ground_swamp.world -= tile_ground_swamp.scroll_speed * tile_ground_swamp.move_x
        if 480 < tile_ground_swamp.world + 5 * tile_ground_swamp.move_x <= 1440:
            tile_ground_swamp.x += tile_ground_swamp.scroll_speed * tile_ground_swamp.move_x

            pass

    @staticmethod
    def draw(tile_ground_swamp):
        for i in range(37):
            tile_ground_swamp.tile_swamp.draw(tile_ground_swamp.x + 128 * i, 50, 192, 136)
        pass

class Tile_ground_swamp:
    i =0
    def __init__(self):
        self.x = 11
        self.tile_swamp = load_image('tile_chapter_0000_tile1_.png')
        self.scroll_speed = 5
        self.move_x, self.world = 0, 11
        self.state_machine = StateMachine(self)  # 늪배경 객체의 state machine 생성
        self.state_machine.start(Tile_Idle)
        self.state_machine.set_transitions(
            {Tile_Idle: {right_down: Tile_move, left_down: Tile_move},
             Tile_move: {right_up: Tile_Idle, left_up: Tile_Idle, a_down: Tile_Idle, d_down: Tile_Idle}
             }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()