from pico2d import *
from state_machine import StateMachine, too_far_to_first, right_up, right_down, left_down, left_up, arrive_at_first
import game_world
import server
import random
import game_framework

PIXEL_PER_METER = (10.0 / 0.12)                     # 10 pixel 12 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour                  #시속 km/h
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)    #분속 m/m
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)              #초속 m/s
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)   #초속 pixel/s

TIME_PER_ACTION = 0.05
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Idle:
    @staticmethod
    def enter(small_slime1, e):
        pass

    @staticmethod
    def exit(small_slime1, e):
        pass

    @staticmethod
    def do(small_slime1):
        if small_slime1.frame_Idle_timer >= 13:  # idle 애니메이션
            small_slime1.frame_Idle = (small_slime1.frame_Idle + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            small_slime1.frame_Idle_timer = 0
        else:
            small_slime1.frame_Idle_timer += 1

        if small_slime1.timer > 200:     #2초마다 방향전환
            if small_slime1.face_dir == 1:
                small_slime1.face_dir = -1
                small_slime1.timer = 0
            else:
                small_slime1.face_dir = 1
                small_slime1.timer = 0
        small_slime1.timer +=1

        if  int(small_slime1.frame_Idle) == 0:
            small_slime1.get_bb_x1, small_slime1.get_bb_y1, small_slime1.get_bb_x2, small_slime1.get_bb_y2 = small_slime1.x - 42, small_slime1.y-27, small_slime1.x+40, small_slime1.y+40
        if  int(small_slime1.frame_Idle) == 1:
            small_slime1.get_bb_x1, small_slime1.get_bb_y1, small_slime1.get_bb_x2, small_slime1.get_bb_y2 = small_slime1.x - 37, small_slime1.y-39, small_slime1.x+37, small_slime1.y+30
        if int(small_slime1.frame_Idle) == 2:
            small_slime1.get_bb_x1, small_slime1.get_bb_y1, small_slime1.get_bb_x2, small_slime1.get_bb_y2 = small_slime1.x - 47, small_slime1.y - 50, small_slime1.x + 47, small_slime1.y + 8
        if int(small_slime1.frame_Idle) == 3:
            small_slime1.get_bb_x1, small_slime1.get_bb_y1, small_slime1.get_bb_x2, small_slime1.get_bb_y2 = small_slime1.x - 40, small_slime1.y - 35, small_slime1.x + 40, small_slime1.y + 32
        pass

    @staticmethod
    def draw(small_slime1):
        if small_slime1.face_dir == 1:
            small_slime1.image_Idle.clip_composite_draw(int(small_slime1.frame_Idle) * 94, 0, 94, 112, 0, 'h',small_slime1.x, small_slime1.y, 94,112)
        elif small_slime1.face_dir == -1:
            small_slime1.image_Idle.clip_draw(int(small_slime1.frame_Idle) * 94, 0, 94, 112, small_slime1.x,small_slime1.y)


        pass

    @staticmethod
    def get_bb(small_slime1):
        return small_slime1.x - 47, small_slime1.y-56, small_slime1.x+47, small_slime1.y+35

class Small_slime1:
    def __init__(self, x=700, y=187):
        self.x, self.y, self.world = x, y, x
        self.x_first, self.y_first = x, y     #초기 위치 (700, 167)
        self.get_bb_x1, self.get_bb_y1, self.get_bb_x2, self.get_bb_y2 = x - 47, y-56, x+47, y+35
        self.knight_x_location = 480
        self.face_dir , self.speed = random.choice([-1,1]), 1
        self.hp_max, self.hp_now, self.hp_decrease, self.power = 1000, 1000, 1000,200

        self.frame_Idle, self.frame_Idle_timer = random.randint(0, 3), 0
        self.timer = random.randint(0, 200)
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.image_Idle = load_image('./using_resource/'+'mon_swamp_dungeon17_01.png')
        self.image_hp_bar = load_image('./using_resource/'+'hp_bar.png')
        self.image_decrease_hp_bar = load_image('./using_resource/'+'decreasing_hp_bar.png')
        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태 -- Idle


    def update(self):
        self.state_machine.update()

        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.background.w) - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.background.w) - self.cw - 1:
            self.x -= int(server.knight.move * RUN_SPEED_PPS * game_framework.frame_time)  # 타일 이동에 맞춰 x 좌표 수정

        self.x +=  int(self.face_dir * RUN_SPEED_PPS * game_framework.frame_time)/4

        if self.hp_now <= 0:
            game_world.remove_object(self)
            print('slime is dead')

        if self.hp_decrease > self.hp_now:
            self.hp_decrease -= 5

        if self.hp_decrease < self.hp_now:
            self.hp_decrease += 5

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()


        self.image_decrease_hp_bar.clip_draw_to_origin(0, 0, 50, 50, self.x-50, self.y+50, self.hp_decrease // 10, 5)
        self.image_hp_bar.clip_draw_to_origin(0, 0, 50, 50, self.x-50, self.y+50, self.hp_now // 10 ,5)



    def draw_rectangle(self):
        draw_rectangle(self.x - 1, self.y - 1, self.x + 1, self.y + 1)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.get_bb_x1, self.get_bb_y1, self.get_bb_x2, self.get_bb_y2

    def get_power(self):
        return self.power


    def handle_collision(self, group, other, power):
        # fill here
        if group == 'sword:monster':
            self.hp_now -= power

        pass