from xml.sax.saxutils import escape
from pico2d import *
import server
from game_world_boss_room import add_collision_pair_boss_room
from state_machine import *
import game_world
import game_world_boss_room
import game_framework
from game_world import add_collision_pair
from sword import Sword
import random

sx, sy = 0 , 0
PIXEL_PER_METER = (10.0 / 0.12)                     # 10 pixel 12 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour                  #시속 km/h
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)    #분속 m/m
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)              #초속 m/s
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)   #초속 pixel/s


TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ATTACK_ACTION = 4
FRAMES_PER_IDLE_ACTION = 4
FRAMES_PER_RUN_ACTION = 7


# 상태를 클래스를 통해서 정의함
class Idle:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(knight, e):
        if right_up(e) or start_event(e):
            knight.face_dir = 1
            knight.move = 0
        elif left_up(e):
            knight.face_dir = 0
            knight.move = 0
        pass

    @staticmethod
    def exit(knight,e):
            pass

    @staticmethod
    def do(knight):

        knight.frame_Idle = (knight.frame_Idle + FRAMES_PER_IDLE_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if knight.face_dir == 1:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 20, sy - 53, sx + 25, sy + 43
        else: knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 25, sy - 53, sx + 20, sy + 43

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Idle.clip_draw(int(knight.frame_Idle) * 128, 0, 55, 70, sx, sy, 83, 105)
        else:
            knight.image_Idle.clip_composite_draw(int(knight.frame_Idle) * 128, 0, 55, 70, 0, 'h', sx, sy, 83, 105)

        pass

class Run:
    @staticmethod
    def enter(knight, e):
        knight.attack_count = 0
        knight.sound_running = load_wav('./using_resource_sound/' + 'running_sound.wav')
        # knight.sound_running.set_volume(60)
        # knight.sound_running.play()
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.move = 1
        elif left_down(e) or right_up(e):
            knight.face_dir = 0
            knight.move = -1
        pass

    @staticmethod
    def exit(knight,e):
        knight.sound_running = None
        pass

    @staticmethod
    def do(knight):
        knight.frame_Run = (knight.frame_Run + FRAMES_PER_RUN_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 7



        knight.x += knight.move * int(RUN_SPEED_PPS * game_framework.frame_time)

        if int(knight.frame_Run)  == 0:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 30, sy - 53, sx + 19, sy + 40
            else: knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 19, sy - 53, sx + 30, sy + 40
        if int(knight.frame_Run)  == 1:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 53, sy - 53, sx + 17, sy + 37
            else: knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 17, sy - 53, sx + 53, sy + 37
        if int(knight.frame_Run)  == 2:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 53, sy - 53, sx+2, sy + 40
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 2, sy - 53, sx + 53, sy + 40
        if int(knight.frame_Run)  == 3:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 37, sy - 53, sx + 17, sy + 42
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 17,sy - 53, sx + 37, sy + 42
        if int(knight.frame_Run)  == 4:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 =sx - 27, sy - 53, sx + 27, sy + 38
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 =sx - 27, sy - 53, sx + 27, sy + 38
        if int(knight.frame_Run)  == 5:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 53, sy - 53, sx + 15, sy + 36
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 15, sy - 53, sx + 53, sy + 36
        if int(knight.frame_Run)  == 6:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 48, sy - 53, sx + 5, sy + 41
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 5, sy - 53, sx + 48, sy + 41

        if knight.gravity <=-3:
            knight.state_machine.add_event(('Falling', 0))

        pass
    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Run.clip_draw(int(knight.frame_Run) * 128, 0, 70, 70, sx, sy, 105, 105)
        else:
            knight.image_Run.clip_composite_draw(int(knight.frame_Run) * 128, 0, 70, 70, 0, 'h', sx, sy, 105, 105)
        pass

class Jump_run:
    @staticmethod
    def enter(knight, e):
        if right_down(e):
            knight.face_dir = 1
            knight.move = 1
        elif left_down(e):
            knight.face_dir = 0
            knight.move = -1
        if space_down(e):
            knight.gravity = 28
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.frame_Jump = (knight.frame_Jump +FRAMES_PER_RUN_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        knight.x += knight.move * int(RUN_SPEED_PPS * game_framework.frame_time)

        if knight.face_dir:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 41, sy - 53, sx + 5, sy + 43
        else:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 5, sy - 53, sx + 41, sy + 43
        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Jump.clip_draw(int(knight.frame_Jump) * 128, 0, 70, 70, sx, sy, 105, 105)
        else:
            knight.image_Jump.clip_composite_draw(int(knight.frame_Jump) * 128, 0, 70, 70, 0, 'h', sx, sy, 105, 105)

        pass

class Jump:
    @staticmethod
    def enter(knight, e):
        knight.attack_count = 0
        if right_down(e):
            knight.face_dir = 1
        elif left_down(e):
            knight.face_dir = 0
        if space_down(e):
            knight.gravity = 28

        knight.move = 0
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.frame_Jump = (knight.frame_Jump + FRAMES_PER_ATTACK_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6



        if knight.face_dir:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 41, sy - 53, sx +5, sy + 43
        else:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 5, sy - 53, sx + 41, sy + 43

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Jump.clip_draw(int(knight.frame_Jump) * 128, 0, 70, 70, sx, sy, 105, 105)
        else:
            knight.image_Jump.clip_composite_draw(int(knight.frame_Jump) * 128, 0, 70, 70, 0, 'h', sx, sy, 105, 105)
        pass

class Attack:
    @staticmethod
    def enter(knight, e):
        knight.move = 0
        if a_down(e) and knight.attack_count + 1 <= 3:
            knight.attack_count += 1
    @staticmethod
    def exit(knight, e):
        if right_down(e) or left_down(e) or space_down(e) or d_down(e):
            knight.attack_motion = 1
            knight.frame_Attack = 0
            knight.attack_count = 0
            knight.power_combo = knight.power
            if knight.sword:
                game_world.remove_object(knight.sword)
                game_world_boss_room.remove_object(knight.sword)
                knight.sword = None

            pass
        pass

    @staticmethod
    def do(knight):
        knight.frame_Attack = (knight.frame_Attack +2*FRAMES_PER_ATTACK_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5  # 0.06초에 1프레임, 총 4프레임 있음

        if knight.attack_motion <= knight.attack_count and int(knight.frame_Attack) == 4:  # 4프레임이 다 그려졌을 때 다음 모션, 프레임 초기화
            knight.attack_motion += 1
            knight.power_combo +=50
            knight.frame_Attack = 0


        elif knight.attack_motion > knight.attack_count:
            knight.attack_motion = 1
            knight.frame_Attack = 0
            knight.attack_count = 0
            knight.state_machine.add_event(('Attack_end', 0))
            knight.power_combo = knight.power




        if int(knight.frame_Attack) == 2:

            if knight.sword == None:
                knight.sword = Sword(sx, sy, knight.power_combo, knight.face_dir)  # Sword 객체 생성
                game_world.add_object(knight.sword, 1)
                game_world_boss_room.add_object(knight.sword, 1)
                add_collision_pair('sword:monster', knight.sword, None)
                add_collision_pair('sword:tree', knight.sword, None)

                add_collision_pair_boss_room('sword:boss', knight.sword, None)

                if knight.attack_motion == 1:
                    knight.sound_attack1.play()
                if knight.attack_motion == 2:
                    knight.sound_attack2.play()
                if knight.attack_motion == 3:
                    knight.sound_attack3.play()

        if int(knight.frame_Attack) == 3:
            if knight.sword:
                game_world.remove_object(knight.sword)
                game_world_boss_room.remove_object(knight.sword)
                knight.sword = None

        if knight.attack_motion == 1:
            if knight.frame_Attack == 0:
                if knight.face_dir:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 43, sy - 53, sx + 35, sy + 43
                else: knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 35, sy - 53, sx + 43,sy + 43
            if int(knight.frame_Attack) == 1:
                if knight.face_dir:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 37, sy - 53, sx + 22,sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 22, sy - 53, sx + 37, sy + 43
            if int(knight.frame_Attack) == 2:
                if knight.face_dir:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 37, sy - 53, sx + 20, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 20, sy - 53, sx + 37, sy + 43
            if int(knight.frame_Attack) == 3:
                if knight.face_dir:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 36, sy - 53, sx + 25, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 25, sy - 53, sx + 36, sy + 43
        if knight.attack_motion == 2:
            if int(knight.frame_Attack) == 0:
                if knight.face_dir ==1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 40, sy - 53, sx + 22, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 22, sy - 53, sx + 40, sy + 43
            if int(knight.frame_Attack) == 1:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 34, sy - 53, sx + 22, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 22, sy - 53, sx + 34,sy + 43
            if int(knight.frame_Attack) == 2:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 39, sy - 53, sx + 32, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 =sx - 32, sy - 53,sx + 39, sy + 43
            if int(knight.frame_Attack) == 3:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 43, sy - 53, sx + 32, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 32, sy - 53, sx + 43,sy + 43
        if knight.attack_motion == 3:
            if int(knight.frame_Attack) == 0:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 43, sy - 53,sx + 24, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 24,sy - 53, sx + 43, sy + 43
            if int(knight.frame_Attack) == 1:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 48, sy - 53, sx + 19, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 19, sy - 53, sx + 48, sy + 43
            if int(knight.frame_Attack) == 2:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 43, sy - 53, sx + 40, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 40, sy - 53, sx + 43, sy + 43
            if int(knight.frame_Attack) == 3:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 43, sy - 53, sx + 32, sy + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 =sx - 32, sy - 53, sx + 43, sy + 43


        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            if knight.attack_motion == 1:
                knight.image_Attack1.clip_draw(int(knight.frame_Attack) * 128, 0, 100, 70, sx + 10, sy, 150, 105)
            if knight.attack_motion == 2:
                knight.image_Attack2.clip_draw(int(knight.frame_Attack) * 128, 0, 120, 70, sx + 20, sy, 180, 105)
            if knight.attack_motion == 3:
                knight.image_Attack3.clip_draw(int(knight.frame_Attack) * 128, 0, 110, 70, sx + 10, sy, 165, 105)
            pass
        else:
            if knight.attack_motion == 1:
                knight.image_Attack1.clip_composite_draw(int(knight.frame_Attack) * 128, 0, 100, 70, 0, 'h', sx - 10,sy, 150, 105)
            if knight.attack_motion == 2:
                knight.image_Attack2.clip_composite_draw(int(knight.frame_Attack) * 128, 0, 120, 70, 0, 'h', sx - 20,sy, 180, 105)
            if knight.attack_motion == 3:
                knight.image_Attack3.clip_composite_draw(int(knight.frame_Attack) * 128, 0, 100, 70, 0, 'h', sx - 10,sy, 150, 105)
        pass

class Protect:
    @staticmethod
    def enter(knight,e):
        knight.attack_count = 0
        knight.move = 0
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.stamina_now -= 50*game_framework.frame_time  # 방어중이면 스테미나 감소

        if knight.stamina_now < 0:
            knight.state_machine.add_event(('No_stamina', 0))
        knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 =sx - 27, sy - 53, sx + 25, sy + 37
        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Protect.clip_draw(0, 0, 70, 70, sx, sy, 105, 105)
        else:
            knight.image_Protect.clip_composite_draw(0, 0, 70, 70, 0, 'h', sx, sy, 105, 105)
        pass


class Defend:
    @staticmethod
    def enter(knight,e):
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.frame_Defend = (knight.frame_Defend + 2.5*FRAMES_PER_ATTACK_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if knight.face_dir:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 41, sy - 53, sx + 5, sy + 43
        else:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 5, sy - 53, sx + 41, sy + 43

        if int(knight.frame_Defend) ==5:
            knight.state_machine.add_event(('Defend_is_over', 0))
            knight.frame_Defend=0

        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Defend.clip_draw(int(knight.frame_Defend) * 128, 0, 70, 70, sx, sy, 105, 105)
        else:
            knight.image_Defend.clip_composite_draw(int(knight.frame_Defend) * 128, 0, 70, 70, 0, 'h', sx, sy, 105, 105)
        pass

class Dead:
    @staticmethod
    def enter(knight,e):
        knight.sound_dead.play()
        knight.move = 0
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.frame_Dead = (knight.frame_Dead + FRAMES_PER_ATTACK_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 19

        if knight.face_dir:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 41, sy - 53, sx + 5, sy + 43
        else:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = sx - 5, sy - 53, sx + 41, sy + 43

        if int(knight.frame_Dead) == 17:
            game_framework.quit()

        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Dead.clip_draw(int(knight.frame_Dead) * 128, 0, 100, 70, sx, sy, 150, 105)
        else:
            knight.image_Dead.clip_composite_draw(int(knight.frame_Dead) * 128, 0, 100, 70, 0, 'h', sx, sy, 150, 105)
        pass

class Knight:
    def __init__(self):
        self.x, self.y = 480, 188
        self.get_bb_x1, self.get_bb_y1,self.get_bb_x2,self.get_bb_y2 = self.x - 20, self.y-53, self.x+25, self.y+43
        self.gravity, self.sword = 0, None
        self.face_dir, self.move, self.speed = 1, 0, RUN_SPEED_PPS
        self.hp_max, self.stamina_max, self.power = 1000, 100, 200
        self.power_combo = self.power
        self.hp_now, self.stamina_now = 1000, 100
        self.hp_decrease = 1000
        self.frame_Idle= 0
        self.frame_Run=0
        self.frame_Jump= 0
        self.frame_Attack=0
        self.frame_Defend = 0
        self.frame_Dead = 0
        self.attack_motion, self.attack_count = 1, 0
        self.method = 0

        self.invincible, self.invincible_timer = False,  0

        self.image_Idle,self.image_Run,self.image_Jump = load_image('./using_resource_image/'+'Knight_Idle.png'), load_image('./using_resource_image/'+'Knight_Run.png'), load_image('./using_resource_image/'+'Knight_Jump.png')
        self.image_Attack1,self.image_Attack2,self.image_Attack3 = load_image('./using_resource_image/'+'Knight_Attack 1.png'), load_image('./using_resource_image/'+'Knight_Attack 2.png'),load_image('./using_resource_image/'+'Knight_Attack 3.png')
        self.image_Protect, self.image_Defend = load_image('./using_resource_image/'+'Knight_Protect.png'), load_image('./using_resource_image/'+'Knight_Defend.png')
        self.image_Dead = load_image('./using_resource_image/'+'Knight_Dead.png')
        self.image_hp_bar,self.image_stamina_bar = load_image('./using_resource_image/'+'hp_bar.png'),load_image('./using_resource_image/'+'stamina_bar.png')
        self.image_max_hp_bar, self.image_max_stamina_bar = load_image('./using_resource_image/'+'max_hp_bar.png'), load_image('./using_resource_image/'+'max_stamina_bar.png')
        self.image_decrease_hp_bar,self.image_ui = load_image('./using_resource_image/'+'decreasing_hp_bar.png'), load_image('./using_resource_image/'+'knight_ui.png')

        self.sound_attack1,  self.sound_attack2,  self.sound_attack3 = load_wav('./using_resource_sound/'+'attack1.wav'), load_wav('./using_resource_sound/'+'attack2.wav'),load_wav('./using_resource_sound/'+'attack3.wav')
        self.sound_get_red_elixir, self.sound_get_yellow_elixir = load_wav('./using_resource_sound/'+'get_red_elixir.wav'), load_wav('./using_resource_sound/'+'get_yellow_elixir.wav')
        self.sound_running, self.sound_hit = load_wav('./using_resource_sound/'+'running_sound.wav'), load_wav('./using_resource_sound/'+'knight_hit.wav')
        self.sound_block1, self.sound_block2, self.sound_block3 = load_wav('./using_resource_sound/'+'knight_block_sword1.wav'), load_wav('./using_resource_sound/'+'knight_block_sword2.wav'),load_wav('./using_resource_sound/'+'knight_block_sword3.wav')
        self.sound_dead = load_wav('./using_resource_sound/'+'knight_is_dead.wav')


        self.sound_get_red_elixir.set_volume(60), self.sound_running.set_volume(40)
        self.sound_attack1.set_volume(20),self.sound_attack2.set_volume(70),self.sound_attack3.set_volume(70),



        self.state_machine = StateMachine(self) #소년 객체의 state machine 생성
        self.state_machine.start(Idle)      #초기 상태 -- Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, space_down: Jump, a_down: Attack, d_down: Protect,knight_is_dead: Dead},
                Run: {right_up: Idle, left_up: Idle, space_down: Jump_run,a_down: Attack, d_down: Protect, falling: Jump_run, knight_is_dead: Dead},
                Attack : {a_down : Attack, attack_end: Idle, right_down: Run, left_down: Run, space_down: Jump, d_down: Protect, knight_is_dead: Dead},
                Jump : {right_down: Jump_run, left_down: Jump_run, landing: Idle, knight_is_dead: Dead},
                Jump_run: {right_up: Jump, left_up: Jump, landing: Run, knight_is_dead: Dead},
                Protect: {right_down: Run, left_down: Run, space_down: Jump, d_up: Idle, no_stamina: Idle, protect_success: Defend,knight_is_dead: Dead},
                Defend: {defend_is_over:Idle},
                Dead: {}
            }
        )

    def update(self):
        self.y += int(self.gravity*game_framework.frame_time*50)  # 기사는 중력(gravity)에 의해 항상 y값이 줄어든다.
        self.gravity -=1

        if self.stamina_now < self.stamina_max:
            self.stamina_now += 5*game_framework.frame_time
        if self.hp_now < self.hp_max:
            self.hp_now += 0.1
            self.hp_decrease += 0.1

        if self.hp_now < 0:
            self.state_machine.add_event(('Knight_is_dead', 0))

        if self.invincible:
            self.invincible_timer += 1

        if self.invincible_timer == 180:
            self.invincible = False
            self.invincible_timer = 0
            print('무적 해제')

        self.state_machine.update()
        self.x = clamp(10.0, self.x, server.background.w - 10.0)
        self.y = clamp(180.0, self.y, server.background.w - 10.0)

        if self.hp_decrease > self.hp_now:
            self.hp_decrease -= 2


    def handle_event(self, event):
        #event: 입력 이벤트 key mouse
        #우리가 state_machine에 전달해 줄건 ( , )
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        global sx
        global sy

        sx = int(self.x -server.background.window_left)
        sy = self.y

        if get_canvas_width()/2<=self.x<=server.background.w-get_canvas_width()/2:
            sx = get_canvas_width()/2

        if self.invincible_timer % 10 <= 5:
            self.state_machine.draw()

        self.image_max_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 90, self.hp_max//2, 20)             #(90,90)을 왼쪽 아래로 두고 그리기
        self.image_decrease_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 90, self.hp_decrease//2 , 20)
        self.image_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 90, self.hp_now//2, 20)


        self.image_max_stamina_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 50, self.stamina_max*3, 20)      #(90,50)을 왼쪽 아래로 두고 그리기
        self.image_stamina_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 50, self.stamina_now*3, 20)

        self.image_ui.clip_draw_to_origin(0, 0, 130, 80, 0, 40, 130, 80)



    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())
        draw_rectangle(sx-1,sy-1,sx+1,sy+1)



    def get_bb(self):
            return self.get_bb_x1, self.get_bb_y1,self.get_bb_x2,self.get_bb_y2

    def get_power(self):
        return self.power

    def take_damage(self, others_power):
        if not self.invincible and self.state_machine.current_state() != Protect:
            self.hp_now -= others_power
            self.invincible = True
            if self.hp_now > 0:
                self.sound_hit.play()
        pass


    def handle_collision(self, group, other, others_power):
        # fill here
        if group == 'knight:monster':
            self.take_damage(others_power)

        if group == 'knight:boss_sword':
            if self.state_machine.current_state() == Protect:
                self.method = random.choice([1, 2, 3])
                if self.method == 1:
                    self.sound_block1.play()
                if self.method == 2:
                    self.sound_block2.play()
                if self.method == 3:
                    self.sound_block3.play()
                self.state_machine.add_event(('Protect_success', 0))


            self.take_damage(others_power)


        if group == 'knight:elixir_hp':
            self.sound_get_red_elixir.play()
            self.hp_max += 150
            self.hp_decrease += 150
            self.hp_now += 150

        if group == 'knight:elixir_power':
            self.sound_get_yellow_elixir.play()
            self.power += 200
            self.power_combo = self.power
            self.stamina_now += 20
            self.stamina_max += 20

        if group == 'knight:tile_ground':
            if self.gravity <=-1.5:            #떨어지는 중에
                self.y = others_power + 53
                self.gravity = 0
                self.state_machine.add_event(('LAND', 0))

        if group == 'knight:tile_midair':
            if self.gravity <= -1.5:
                self.y = others_power + 53
                self.gravity = 0
                self.state_machine.add_event(('LAND', 0))


