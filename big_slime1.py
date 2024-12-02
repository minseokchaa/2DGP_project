from pico2d import *
from state_machine import StateMachine
import game_world
import server
import game_framework
import random

PIXEL_PER_METER = (10.0 / 0.12)                     # 10 pixel 12 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour                  #시속 km/h
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)    #분속 m/m
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)              #초속 m/s
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)   #초속 pixel/s

TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Idle:
    @staticmethod
    def enter(big_slime1, e):
        pass

    @staticmethod
    def exit(big_slime1, e):
        pass

    @staticmethod
    def do(big_slime1):
        big_slime1.frame_Idle = (big_slime1.frame_Idle + big_slime1.bounce_speed *FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4


        if big_slime1.timer > 200:  # 2초마다 방향전환
            if big_slime1.face_dir == 1:
                big_slime1.face_dir = -1
                big_slime1.timer = 0
            else:
                big_slime1.face_dir = 1
                big_slime1.timer = 0
        big_slime1.timer += 1

        if  int(big_slime1.frame_Idle) == 0:
            big_slime1.get_bb_x1, big_slime1.get_bb_y1, big_slime1.get_bb_x2, big_slime1.get_bb_y2 = big_slime1.x - 67, big_slime1.y - 65, big_slime1.x + 70, big_slime1.y + 80
        if  int(big_slime1.frame_Idle) == 1:
            big_slime1.get_bb_x1, big_slime1.get_bb_y1, big_slime1.get_bb_x2, big_slime1.get_bb_y2 = big_slime1.x - 67, big_slime1.y - 70, big_slime1.x + 67, big_slime1.y + 45
        if int(big_slime1.frame_Idle) == 2:
            big_slime1.get_bb_x1, big_slime1.get_bb_y1, big_slime1.get_bb_x2, big_slime1.get_bb_y2 = big_slime1.x - 67, big_slime1.y - 70, big_slime1.x + 67, big_slime1.y + 45
        if  int(big_slime1.frame_Idle) == 3:
            big_slime1.get_bb_x1, big_slime1.get_bb_y1, big_slime1.get_bb_x2, big_slime1.get_bb_y2 = big_slime1.x - 67, big_slime1.y - 65, big_slime1.x + 67, big_slime1.y + 80

        pass

    @staticmethod
    def draw(big_slime1):
        if big_slime1.face_dir == 1:
            big_slime1.image_Idle.clip_draw(int(big_slime1.frame_Idle) * 141, 0, 141, 163, big_slime1.x,big_slime1.y)
        elif big_slime1.face_dir == -1:
            big_slime1.image_Idle.clip_composite_draw(int(big_slime1.frame_Idle) * 141, 0, 141, 163, 0, 'h', big_slime1.x,big_slime1.y, 141, 163)
        pass


class Big_slime1:
    def __init__(self, x = 1400, y = 190):
        self.x, self.y = x, y
        self.get_bb_x1, self.get_bb_y1, self.get_bb_x2, self.get_bb_y2 = x - 47, y - 56, x + 47, y + 35
        self.i = 1
        self.face_dir , self.bounce_speed, self.running_speed = random.choice([-1,1]), 1.3, 5
        self.hp_max, self.hp_now, self.hp_decrease,self.power = 1500, 1500, 1500, 300
        self.frame_Idle, self.frame_Idle_timer = 0, 0
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.timer = 0
        self.hit = False
        self.hit_timer = 0
        self.image_Idle = load_image('./using_resource_image/'+'mon_swamp_Big_Undead3_2_01.png')
        self.image_hp_bar = load_image('./using_resource_image/'+'hp_bar.png')
        self.image_decrease_hp_bar = load_image('./using_resource_image/'+'decreasing_hp_bar.png')
        self.slime_hit = load_wav('./using_resource_sound/' + 'slime_hit.wav')
        self.slime_hit.set_volume(60)

        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태 -- Idle



    def update(self):
        self.state_machine.update()

        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.background.w) - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.background.w) - self.cw - 1:
            self.x -= int(server.knight.move * RUN_SPEED_PPS * game_framework.frame_time)  # 타일 이동에 맞춰 x 좌표 수정

        self.x +=  int(self.face_dir * RUN_SPEED_PPS * game_framework.frame_time)/self.running_speed

        if self.hp_now <= 0:
            self.bounce_speed = 2
            self.running_speed = 2
            game_world.remove_collision_object(self)
            self.i -= 0.01
            self.image_Idle.opacify(self.i)
            if get_canvas_width() / 2 <= server.knight.x <= server.background.w - get_canvas_width() / 2:
                if self.x > get_canvas_width()/2:
                    self.face_dir = 1
                elif self.x < get_canvas_width()/2:
                    self.face_dir = -1
            elif get_canvas_width() / 2 > server.knight.x:
                if self.x > server.knight.x:
                    self.face_dir = 1
                elif self.x < server.knight.x:
                    self.face_dir = -1


        if self.i < 0:
            game_world.remove_object(self)

        if self.hp_decrease > self.hp_now:
            self.hp_decrease -= 5

        if self.hp_decrease < self.hp_now:
            self.hp_decrease += 5

        if self.hit:
            self.hit_timer += 1
            if 1 <= self.hit_timer < 6:
                self.x -= 2
            if 6 <= self.hit_timer <= 10:
                self.x += 2

        if self.hit_timer == 10:
            self.image_Idle.opacify(1)
            self.hit = False
            self.hit_timer = 0

    pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()

        self.image_decrease_hp_bar.clip_draw_to_origin(0, 0, 50, 50, self.x-67, self.y+100, self.hp_decrease // 10, 5)
        self.image_hp_bar.clip_draw_to_origin(0, 0, 50, 50, self.x-67, self.y+100, self.hp_now // 10 ,5)



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
            if self.hp_now > 0:
                self.hp_now -= power
                self.slime_hit.play()

                self.hit = True
                self.image_Idle.opacify(0.5)


        pass