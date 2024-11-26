from xml.sax.saxutils import escape

from pico2d import *
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from state_machine import StateMachine, boss_attack, boss_move, boss_stop
import play_boss_room
import server


PIXEL_PER_METER = (10.0 / 0.12)  # 10 pixel 30 cm
Walk_SPEED_KMPH = 12.0  # Km / Hour
Walk_SPEED_MPM = (Walk_SPEED_KMPH * 1000.0 / 60.0)
Walk_SPEED_MPS = (Walk_SPEED_MPM / 60.0)
Walk_SPEED_PPS = (Walk_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FRAMES_IDLE_ACTION = 6.0
FRAMES_WALK_ACTION = 12.0
FRAMES_ATTACK_ACTION = 15.0
FRAMES_DEAD_ACTION = 22.0

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
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 62, boss.y - 198, boss.x + 87, boss.y - 23
            elif int(boss.frame_Idle) ==1:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 198, boss.x + 87, boss.y - 20
            elif int(boss.frame_Idle) ==2:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 198, boss.x + 87, boss.y - 18
            elif int(boss.frame_Idle) ==3:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 198, boss.x + 87, boss.y - 11
            elif int(boss.frame_Idle) ==4:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 198, boss.x + 87, boss.y - 16
            elif int(boss.frame_Idle) ==5:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 65, boss.y - 198, boss.x + 87, boss.y - 20
        else:
            if int(boss.frame_Idle) == 0:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 198, boss.x + 62, boss.y - 23
            elif int(boss.frame_Idle) == 1:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 198, boss.x + 65, boss.y - 20
            elif int(boss.frame_Idle) == 2:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 198, boss.x + 65, boss.y - 18
            elif int(boss.frame_Idle) == 3:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 198, boss.x + 65, boss.y - 11
            elif int(boss.frame_Idle) == 4:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 198, boss.x + 65, boss.y - 16
            elif int(boss.frame_Idle) == 5:
                boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 87, boss.y - 198, boss.x + 65, boss.y - 20

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
            Walk_SPEED_PPS  = 0
        elif int(boss.frame_Walk) ==1:
            Walk_SPEED_PPS = 0
        elif int(boss.frame_Walk) ==7:
            Walk_SPEED_PPS = 0
        elif int(boss.frame_Walk) ==8:
            Walk_SPEED_PPS = 0
        else:
            Walk_SPEED_PPS = (Walk_SPEED_MPS * PIXEL_PER_METER)

        if boss.face_dir == 1:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 20, boss.y - 53, boss.x + 25, boss.y + 43
        else:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 25, boss.y - 53, boss.x + 20, boss.y + 43

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

        boss.action_num = 2
        pass

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):

        boss.frame_Attack = (boss.frame_Attack + FRAMES_ATTACK_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 15

        if boss.face_dir == 1:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 20, boss.y - 53, boss.x + 25, boss.y + 43
        else:
            boss.get_bb_x1, boss.get_bb_y1, boss.get_bb_x2, boss.get_bb_y2 = boss.x - 25, boss.y - 53, boss.x + 20, boss.y + 43

    @staticmethod
    def draw(boss):
        if boss.face_dir:
            boss.image.clip_draw(int(boss.frame_Attack) * 228, boss.action_num*160, 228, 160, boss.x, boss.y, 342, 240)
        else:
            boss.image.clip_composite_draw(int(boss.frame_Attack) * 128, boss.action_num*160, 228, 160, 0, 'h', boss.x, boss.y, 342, 240)

        pass


class Boss:

    def __init__(self, x=500, y=350):
        self.x ,self.y = x,y
        self.get_bb_x1, self.get_bb_y1, self.get_bb_x2, self.get_bb_y2 = self.x - 20, self.y - 53, self.x + 25, self.y + 43
        self.image = load_image('./using_resource/' + 'demon_slime_FREE_v1.0_288x160_spritesheet.png')
        self.face_dir = 1       #1=오른쪽으로 이동 0=왼쪽으로 이동
        self.frame_Idle, self.frame_Walk, self.frame_Attack = 0, 0, 0
        self.state = 'Idle'
        self.hp_max, self.hp_now,self.hp_decrease, self.power = 15000, 15000, 15000,300
        self.action_num = 4     #0=dead, 1 = hit, 2 = attack, 3 = walk, 4 = idle

        self.image_hp_bar= load_image('./using_resource/' + 'hp_bar.png')
        self.image_max_hp_bar= load_image('./using_resource/' + 'max_hp_bar.png')
        self.image_decrease_hp_bar = load_image('./using_resource/' + 'decreasing_hp_bar.png')

        self.build_behavior_tree()

        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태 -- Idle
        self.state_machine.set_transitions(
            {
                Idle: {boss_move: Walk},
                Walk: {boss_stop: Idle},
                # Attack: {a_down: Attack, attack_end: Idle, right_down: Walk, left_down: Walk, space_down: Jump,d_down: Protect}
            }
        )


    def get_bb(self):
        return self.get_bb_x1, self.get_bb_y1,self.get_bb_x2,self.get_bb_y2


    def update(self):


        self.x = clamp(50, self.x, 1550)

        if self.hp_decrease > self.hp_now:
            self.hp_decrease -= 20


        self.state_machine.update()


        # fill here
        self.bt.run()

    def draw(self):
        self.state_machine.draw()

        self.image_max_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 850, self.hp_max//10, 20)             #(90,90)을 왼쪽 아래로 두고 그리기
        self.image_decrease_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 850, self.hp_decrease//10 , 20)
        self.image_hp_bar.clip_draw_to_origin(0, 0, 50, 50, 90, 850, self.hp_now//10, 20)


    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())
        draw_rectangle(self.x - 1, self.y - 1, self.x + 1, self.y + 1)

        # Zombie.marker_image.draw(self.tx, self.ty)


    def handle_event(self, event):
        pass

    def get_power(self):
        return self.power

    def take_damage(self, others_power):
        self.hp_now -= others_power
        pass

    def handle_collision(self, group, other,others_power):
        if group == 'sword:boss':
            self.take_damage(others_power)





    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self. tx, self.ty = x, y
        return BehaviorTree.SUCCESS
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

        pass

    def distance_more_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 > (PIXEL_PER_METER * r) ** 2

        pass

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

    def slash_the_sword(self, tx, ty):
        self.state_machine.add_event(('Boss_attack', 0))
        pass


    def is_knight_nearby(self, r):
        if self.distance_less_than(server.knight.x, server.knight.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_knight(self, r=0.5):
        self.move_slightly_to(server.knight.x)
        if self.distance_less_than(server.knight.x, server.knight.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
    #     #--------------------------------------------------------------------
    #
    #     c1 = Condition('기사가 근처에 있는가?', self.is_knight_nearby, 7)
    #
    #     a3 = Action('검 내려찍기', self.slash_the_sword)
    #
    #     # --------------------------------------------------------------------
    #
    #     c2 = Condition('나의 체력이 절반 이하인가?', self.is_mine_more_then_knight, lambda:self.hp_now)
    #
    #     c3 = Condition('마지막 불기둥을 사용한지 일정시간이 지났나?', self.is_mine_less_then_knight, lambda:self.ball_count, lambda:play_boss_room.knight.ball_count)
    #
    #     a2 = Action('불기둥 생성', self.move_to)
    #
    #     # --------------------------------------------------------------------
    #
        a4 = Action('기사의 x위치 추적', self.move_to_knight)
    #
    #
    #     #----------------------------------------------------------------------
    #     sword_attack = Sequence('검 공격', c1, a3)
    #
    #     flame_strike = Sequence('불기둥 공격', c2, c3, a2)

        chase_knight = Sequence('이동', a4)
    #
    #
    #
    #
        root = boss_behavior_tree = Selector('보스의 행동트리', chase_knight)

        #root = boss_behavior_tree = Selector('보스의 행동트리', sword_attack, flame_strike, chase_knight)

        self.bt = BehaviorTree(root)

    pass