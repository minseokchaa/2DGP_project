
from pico2d import *
import game_framework
import game_world_boss_room
from game_world_boss_room import add_collision_pair_boss_room
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from state_machine import *
import ending_mode
import server
import random
from boss_sword import Sword
from flame_strike import Flame_strike
from crater import Crater


PIXEL_PER_METER = (10.0 / 0.12)  # 10 pixel 30 cm
Walk_SPEED_KMPH = 12.0  # Km / Hour
Walk_SPEED_MPM = (Walk_SPEED_KMPH * 1000.0 / 60.0)
Walk_SPEED_MPS = (Walk_SPEED_MPM / 60.0)
Walk_SPEED_PPS = (Walk_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FRAMES_IDLE_ACTION = 6.0
FRAMES_WALK_ACTION = 12.0
FRAMES_ATTACK_ACTION = 16.0
FRAMES_FLAME_STRIKE_ACTION = 8.0
FRAMES_DEAD_ACTION = 48.0

class Idle:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(boss, e):

        boss.action_num = 4
        pass

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):

        boss.frame_Idle = (boss.frame_Idle + 0.5*FRAMES_IDLE_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_IDLE_ACTION

        if boss.face_dir == -1:
            if int(boss.frame_Idle) ==0:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 62, boss.y - 200, boss.x + 87, boss.y - 23
            elif int(boss.frame_Idle) ==1:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 200, boss.x + 87, boss.y - 20
            elif int(boss.frame_Idle) ==2:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 200, boss.x + 87, boss.y - 18
            elif int(boss.frame_Idle) ==3:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 200, boss.x + 87, boss.y - 11
            elif int(boss.frame_Idle) ==4:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 200, boss.x + 87, boss.y - 16
            elif int(boss.frame_Idle) ==5:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 200, boss.x + 87, boss.y - 20
        else:
            if int(boss.frame_Idle) == 0:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 200, boss.x + 62, boss.y - 23
            elif int(boss.frame_Idle) == 1:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 200, boss.x + 65, boss.y - 20
            elif int(boss.frame_Idle) == 2:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 200, boss.x + 65, boss.y - 18
            elif int(boss.frame_Idle) == 3:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 200, boss.x + 65, boss.y - 11
            elif int(boss.frame_Idle) == 4:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 200, boss.x + 65, boss.y - 16
            elif int(boss.frame_Idle) == 5:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 200, boss.x + 65, boss.y - 20

    @staticmethod
    def draw(boss):
        if boss.face_dir ==1:
            boss.image.clip_composite_draw(int(boss.frame_Idle) * 288, boss.action_num*160, 288, 160, 0, 'h', boss.x, boss.y, 720, 400)
        else:
            boss.image.clip_draw(int(boss.frame_Idle) * 288, boss.action_num * 160, 288, 160, boss.x, boss.y, 720, 400)

        pass

class Walk:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(boss, e):
        boss.action_num = 3
        pass

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):
        global Walk_SPEED_PPS

        boss.frame_Walk = (boss.frame_Walk + 0.5*FRAMES_WALK_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_WALK_ACTION
        if int(boss.frame_Walk) ==0:
            if boss.sound1 ==None:
                boss.sound_walk1.play()
                boss.sound1 = 1
                boss.sound2 = None
        elif int(boss.frame_Walk) ==1:
            Walk_SPEED_PPS  = 0
        elif int(boss.frame_Walk) ==2:
            Walk_SPEED_PPS = 0
        elif int(boss.frame_Walk) ==6:
            if boss.sound2 == None:
                boss.sound_walk2.play()
                boss.sound2 = 1
                boss.sound1 = None
        elif int(boss.frame_Walk) ==7:
            Walk_SPEED_PPS = 0
        elif int(boss.frame_Walk) ==8:
            Walk_SPEED_PPS = 0
        else:
            Walk_SPEED_PPS = (Walk_SPEED_MPS * PIXEL_PER_METER)

        if boss.face_dir == 1:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 62, boss.y - 200, boss.x + 87, boss.y - 23
        else:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 62, boss.y - 200, boss.x + 87, boss.y - 23

    @staticmethod
    def draw(boss):
        if boss.face_dir == 1:
            boss.image.clip_composite_draw(int(boss.frame_Walk) * 288, boss.action_num * 160, 288, 160, 0, 'h', boss.x,boss.y, 720, 400)
        else:
            boss.image.clip_draw(int(boss.frame_Walk) * 288, boss.action_num * 160, 288, 160, boss.x, boss.y, 720, 400)

        pass
    
class Attack:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(boss, e):
        boss.method = random.choice([1, 2])

        if boss.method == 1:
            boss.sound_attack1.play()
        if boss.method == 2:
            boss.sound_attack2.play()

        boss.action_num = 2
        pass

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):

        boss.frame_Attack = (boss.frame_Attack + 0.4*FRAMES_ATTACK_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_ATTACK_ACTION

        if boss.face_dir == 1:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 62, boss.y - 200, boss.x + 87, boss.y - 23
        else:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 62, boss.y - 200, boss.x + 87, boss.y - 23


        if int(boss.frame_Attack) == 9:
            if boss.sword == None:
                boss.sword = Sword(boss.x, boss.y, boss.power, boss.face_dir)  # Sword 객체 생성
                game_world_boss_room.add_object(boss.sword, 1)
                add_collision_pair_boss_room('knight:boss_sword', None, boss.sword)
                boss.sound_hit_ground.play()

        if int(boss.frame_Attack) == 11:
            if boss.sword:
                game_world_boss_room.remove_object(boss.sword)
                boss.sword = None




        if int(boss.frame_Attack) ==15:
            boss.state_machine.add_event(('Boss_attack_end', 0))
            boss.frame_Attack =0



    @staticmethod
    def draw(boss):
        if boss.face_dir == 1:
            boss.image.clip_composite_draw(int(boss.frame_Attack) * 288, boss.action_num * 160, 288, 160, 0, 'h', boss.x,boss.y, 720, 400)
        else:
            boss.image.clip_draw(int(boss.frame_Attack) * 288, boss.action_num * 160, 288, 160, boss.x, boss.y, 720, 400)

        pass

class Dead:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(boss, e):

        boss.action_num = 0
        boss.sound_dead.play()
        pass

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):

        boss.frame_Dead = (boss.frame_Dead + 0.07*FRAMES_DEAD_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_DEAD_ACTION

        if int(boss.frame_Dead) ==47:
            game_world_boss_room.remove_object(boss)
            game_framework.change_mode(ending_mode)


    @staticmethod
    def draw(boss):
        if boss.face_dir ==1:
            boss.image.clip_composite_draw(int(boss.frame_Dead) * 288, boss.action_num*160, 288, 160, 0, 'h', boss.x, boss.y, 720, 400)
        else:
            boss.image.clip_draw(int(boss.frame_Dead) * 288, boss.action_num * 160, 288, 160, boss.x, boss.y, 720, 400)

        pass

class flame_strike:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(boss, e):
        boss.method = random.choice([1, 2])

        if boss.method == 1:
            boss.sound_attack1.play()
        if boss.method == 2:
            boss.sound_attack2.play()

        boss.action_num = 0
        boss.frame_Attack = 0

        craters = [Crater(random.randint(100, 1500), 300) for _ in range(4)]
        for crater in craters:
            game_world_boss_room.add_object(crater, 1)
        pass

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):

        boss.frame_flame_strike = (boss.frame_flame_strike + 0.6*FRAMES_FLAME_STRIKE_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_FLAME_STRIKE_ACTION

        if boss.face_dir == 1:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 62, boss.y - 200, boss.x + 87, boss.y - 23
        else:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 62, boss.y - 200, boss.x + 87, boss.y - 23


        if int(boss.frame_flame_strike) ==7:
            boss.state_machine.add_event(('Boss_attack_end', 0))
            boss.frame_flame_strike =0
            boss.flame_strike_time=0



    @staticmethod
    def draw(boss):
        if boss.face_dir == 1:
            boss.image.clip_composite_draw(int(boss.frame_flame_strike) * 288, boss.action_num * 160, 288, 160, 0, 'h', boss.x,boss.y, 720, 400)
        else:
            boss.image.clip_draw(int(boss.frame_flame_strike) * 288, boss.action_num * 160, 288, 160, boss.x, boss.y, 720, 400)

        pass


class Boss:

    def __init__(self, x=1000, y=350):
        self.x ,self.y = x,y
        self.get_bb_x1, self.get_bb_y1, self.get_bb_x2, self.get_bb_y2 = self.x - 20, self.y - 53, self.x + 25, self.y + 43
        self.face_dir = 1       #1=오른쪽으로 이동 0=왼쪽으로 이동
        self.frame_Idle, self.frame_Walk, self.frame_Attack, self.frame_Dead, self.frame_flame_strike = 0, 0, 0, 0, 0
        self.sword, self.sound1, self.sound2 = None, None, None
        self.hp_max, self.hp_now,self.hp_decrease, self.power = 28000, 28000, 28000,500
        self.action_num = 4     #0=dead, 1 = hit, 2 = attack, 3 = walk, 4 = idle
        self.method = 0
        self.hit, self.hit_timer = False, 0
        self.flame_strike_time = 0

        self.image = load_image('./using_resource_image/' + 'demon_slime_FREE_v1.0_288x160_spritesheet.png')
        self.image_hp_bar, self.image_max_hp_bar= load_image('./using_resource_image/' + 'hp_bar.png'), load_image('./using_resource_image/' + 'max_hp_bar.png')
        self.image_decrease_hp_bar = load_image('./using_resource_image/' + 'decreasing_hp_bar.png')

        self.sound_attack1, self.sound_attack2 = load_wav('./using_resource_sound/' + 'boss_attack_sound1.wav'), load_wav('./using_resource_sound/' + 'boss_attack_sound2.wav')
        self.sound_walk1, self.sound_walk2 = load_wav('./using_resource_sound/' + 'small_explosion1.wav'), load_wav('./using_resource_sound/' + 'small_explosion2.wav')
        self.sound_hit_ground, self.sound_dead = load_wav('./using_resource_sound/' + 'boss_sword_hit_ground.wav'), load_wav('./using_resource_sound/' + 'boss_dead_sound.wav')
        self.sound_hit1, self.sound_hit2 = load_wav('./using_resource_sound/' + 'boss_hit_sound1.wav'), load_wav('./using_resource_sound/' + 'boss_hit_sound2.wav')

        self.sound_attack1.set_volume(55), self.sound_attack2.set_volume(55), self.sound_walk1.set_volume(20), self.sound_walk2.set_volume(20)
        self.sound_hit_ground.set_volume(90), self.sound_hit1.set_volume(40), self.sound_hit2.set_volume(40)

        self.build_behavior_tree()

        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태 -- Idle
        self.state_machine.set_transitions(
            {
                Idle: {boss_move: Walk, boss_attack: Attack, boss_is_dead: Dead, boss_flame_strike: flame_strike},
                Walk: {boss_stop: Idle, boss_attack: Attack, boss_is_dead: Dead, boss_flame_strike: flame_strike},
                Attack: {boss_attack_end: Idle, boss_is_dead: Dead},
                flame_strike: {boss_attack_end: Idle, boss_is_dead: Dead},
                Dead: {}
            }
        )


    def get_bb(self):
        return self.get_bb_x1, self.get_bb_y1,self.get_bb_x2,self.get_bb_y2


    def update(self):
        if self.hit:
            self.hit_timer += 1
            if 1 <= self.hit_timer < 6:
                self.x -= 2
            if 6 <= self.hit_timer <= 10:
                self.x += 2

        if self.hit_timer == 10:
            self.image.opacify(1)
            self.hit = False
            self.hit_timer = 0

        if self.hp_now <= 0:
            self.state_machine.add_event(('Boss_is_dead', 0))


        self.x = clamp(50, self.x, 1550)

        self.flame_strike_time +=1

        if self.hp_decrease > self.hp_now:
            self.hp_decrease -= 20

        self.state_machine.update()
        # fill here
        self.bt.run()

    def draw(self):
        self.state_machine.draw()

        self.image_max_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 850, self.hp_max//20, 20)             #(90,90)을 왼쪽 아래로 두고 그리기
        self.image_decrease_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 850, self.hp_decrease//20 , 20)
        self.image_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 850, self.hp_now//20, 20)


    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())
        draw_rectangle(self.x - 1, self.y - 1, self.x + 1, self.y + 1)


    def handle_event(self, event):
        pass

    def get_power(self):
        return self.power

    def take_damage(self, others_power):
        self.hp_now -= others_power
        pass

    def handle_collision(self, group, other,others_power):
        if group == 'sword:boss':
            self.hit = True
            self.image.opacify(0.5)

            self.method = random.choice([1, 2])
            if self.method == 1:
                self.sound_hit1.play()
            if self.method == 2:
                self.sound_hit2.play()

            self.take_damage(others_power)



    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx):
        distance = Walk_SPEED_PPS * game_framework.frame_time
        diff = tx - self.x
        if diff > 0:
            self.face_dir = 1
        else:
            self.face_dir = -1
        if abs(diff) <= distance:
            self.x = tx  # 정확히 목표 지점에 도달
            self.state_machine.add_event(('Boss_knight_same_x', 0))
        else:
            self.x += distance * (self.face_dir)
            self.state_machine.add_event(('Boss_knight_diff_x', 0))

    def find_direction(self, tx):
        diff = tx - self.x              #face_dir =1 => 오른쪽 공격, tx가 self.x보다 작으면 =>face_dir =-1 => 왼쪽 공격
        if diff > 0:
            self.face_dir = 1
        else:
            self.face_dir = -1

    def turn_to_knight(self):
        if self.frame_Attack <= 0:
            self.find_direction(server.knight.x)
        return BehaviorTree.SUCCESS

    def slash_the_sword(self):
        self.state_machine.add_event(('Boss_attack', 0))
        return BehaviorTree.SUCCESS


    def is_knight_nearby(self, r):
        if self.distance_less_than(server.knight.x, server.knight.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_attacking_now(self):
        if self.frame_Attack >0:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS


    def move_to_knight(self, r=0.5):
        self.move_slightly_to(server.knight.x)
        if self.distance_less_than(server.knight.x, server.knight.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_hp_under_half(self):
        if self.hp_now < self.hp_max/2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def check_flame_strike(self):
        if self.flame_strike_time > 500:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def make_flame_strike(self):
        self.state_machine.add_event(('Boss_flame_strike', 0))
        return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
         #--------------------------------------------------------------------
    #
        c1 = Condition('기사가 근처에 있는가?', self.is_knight_nearby, 3)
        a1 = Action('기사 방향으로 돌기', self.turn_to_knight)
        a3 = Action('검 내려찍기', self.slash_the_sword)

        # --------------------------------------------------------------------

        c2 = Condition('나의 체력이 절반 이하인가?', self.is_hp_under_half)
        c3 = Condition('마지막 불기둥을 사용한지 일정시간이 지났나?', self.check_flame_strike)
        a2 = Action('불기둥 생성', self.make_flame_strike)

        # --------------------------------------------------------------------
        c4 = Condition('공격 중이 아닌가?', self.is_attacking_now)
        a4 = Action('기사의 x위치 추적', self.move_to_knight)
        #----------------------------------------------------------------------
        sword_attack = Sequence('검 공격', c1, a1, a3)

        flame_strike = Sequence('불기둥 공격', c2, c3, a2)

        chase_knight = Sequence('이동', c4, a4)

    #   root = boss_behavior_tree = Selector('보스의 행동트리', chase_knight)
        root = boss_behavior_tree = Selector('보스의 행동트리', sword_attack, chase_knight)
        root = boss_behavior_tree = Selector('보스의 행동트리', flame_strike, sword_attack, chase_knight)

        self.bt = BehaviorTree(root)

    pass