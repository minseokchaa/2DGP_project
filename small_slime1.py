from pico2d import load_image, get_time, draw_rectangle
from state_machine import StateMachine, too_far_to_first, right_up, right_down, left_down, left_up, arrive_at_first
import game_world


def find_knight(monster): #knight를 찾았을 때  state machine에 이벤트 생성

    monster.state_machine.add_event(('Find_knight', 0))
    pass

class Idle:
    @staticmethod
    def enter(small_slime1, e):
        pass

    @staticmethod
    def exit(small_slime1, e):
        if right_up(e) or left_up(e):
            small_slime1.move = 0
        elif right_down(e):
            small_slime1.move = -5
        elif left_down(e):
            small_slime1.move = 5
        pass

    @staticmethod
    def do(small_slime1):
        if small_slime1.frame_Idle_timer >= 13:  # idle 애니메이션
            small_slime1.frame_Idle = (small_slime1.frame_Idle + 1) % 4
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
        if  small_slime1.frame_Idle == 0:
            small_slime1.get_bb_x1, small_slime1.get_bb_y1, small_slime1.get_bb_x2, small_slime1.get_bb_y2 = small_slime1.x - 42, small_slime1.y-27, small_slime1.x+40, small_slime1.y+40
        if  small_slime1.frame_Idle == 1:
            small_slime1.get_bb_x1, small_slime1.get_bb_y1, small_slime1.get_bb_x2, small_slime1.get_bb_y2 = small_slime1.x - 37, small_slime1.y-39, small_slime1.x+37, small_slime1.y+30
        if small_slime1.frame_Idle == 2:
            small_slime1.get_bb_x1, small_slime1.get_bb_y1, small_slime1.get_bb_x2, small_slime1.get_bb_y2 = small_slime1.x - 47, small_slime1.y - 50, small_slime1.x + 47, small_slime1.y + 8
        if small_slime1.frame_Idle == 3:
            small_slime1.get_bb_x1, small_slime1.get_bb_y1, small_slime1.get_bb_x2, small_slime1.get_bb_y2 = small_slime1.x - 40, small_slime1.y - 35, small_slime1.x + 40, small_slime1.y + 32
        pass

    @staticmethod
    def draw(small_slime1):
        if small_slime1.face_dir == 1:
            small_slime1.image_Idle.clip_composite_draw(small_slime1.frame_Idle * 94, 0, 94, 112, 0, 'h',small_slime1.x, small_slime1.y, 94,112)
        elif small_slime1.face_dir == -1:
            small_slime1.image_Idle.clip_draw(small_slime1.frame_Idle * 94, 0, 94, 112, small_slime1.x,small_slime1.y)

        draw_rectangle(small_slime1.x - 1, small_slime1.y - 1, small_slime1.x + 1, small_slime1.y + 1)
        draw_rectangle(*small_slime1.get_bb())
        pass

    @staticmethod
    def get_bb(small_slime1):
        return small_slime1.x - 47, small_slime1.y-56, small_slime1.x+47, small_slime1.y+35

class Attack:
    @staticmethod
    def enter(small_slime1, e):
        pass

    @staticmethod
    def exit(small_slime1, e):
        if right_up(e) or left_up(e):
            small_slime1.move = 0
        elif right_down(e):
            small_slime1.move =-5
        elif left_down(e):
            small_slime1.move = 5
        pass

    @staticmethod
    def do(small_slime1):
        if small_slime1.frame_Idle_timer >= 10:  # idle 애니메이션
            small_slime1.frame_Idle = (small_slime1.frame_Idle + 1) % 4
            small_slime1.frame_Idle_timer = 0
        else:
            small_slime1.frame_Idle_timer += 1

        if abs(small_slime1.x - small_slime1.x_first) > 400:    #처음 위치에서 400만큼 떨어지면 처음 위치로 돌아가기
            small_slime1.state_machine.add_event(('Too_far_to_first', 0))
        pass

    @staticmethod
    def draw(small_slime1):
        if small_slime1.face_dir == 1:
            small_slime1.image_Idle.clip_composite_draw(small_slime1.frame_Idle * 94, 0, 94, 112, 0, 'h',
                                                        small_slime1.x, small_slime1.y, 94, 112)
        elif small_slime1.face_dir == -1:
            small_slime1.image_Idle.clip_draw(small_slime1.frame_Idle * 94, 0, 94, 112, small_slime1.x, small_slime1.y)
        pass

class Return_to_Idle:
    @staticmethod
    def enter(small_slime1, e):
        pass

    @staticmethod
    def exit(small_slime1, e):
        if right_up(e) or left_up(e):
            small_slime1.move = 0
        elif right_down(e):
            small_slime1.move = -5
        elif left_down(e):
            small_slime1.move = 5
        pass

    @staticmethod
    def do(small_slime1):
        if small_slime1.frame_Idle_timer >= 10:  # idle 애니메이션
            small_slime1.frame_Idle = (small_slime1.frame_Idle + 1) % 4
            small_slime1.frame_Idle_timer = 0
        else:
            small_slime1.frame_Idle_timer += 1

        if small_slime1.world < small_slime1.x_first:
            small_slime1.face_dir = 1
            small_slime1.world += 1
            small_slime1.x += 1
        if small_slime1.world > small_slime1.x_first:
            small_slime1.face_dir = -1
            small_slime1.world -= 1
            small_slime1.x -= 1

        if small_slime1.world == small_slime1.x_first:
            small_slime1.state_machine.add_event(('Arrive_at_first', 0))
        pass

    @staticmethod
    def draw(small_slime1):
        if small_slime1.face_dir == 1:
            small_slime1.image_Idle.clip_composite_draw(small_slime1.frame_Idle * 94, 0, 94, 112, 0, 'h',small_slime1.x, small_slime1.y, 94, 112)
        elif small_slime1.face_dir == -1:
            small_slime1.image_Idle.clip_draw(small_slime1.frame_Idle * 94, 0, 94, 112, small_slime1.x, small_slime1.y)
        pass

class Small_slime1:
    def __init__(self):
        self.x, self.y, self.world = 700, 167, 700
        self.x_first, self.y_first = 700, 167      #초기 위치 (700, 167)
        self.get_bb_x1, self.get_bb_y1, self.get_bb_x2, self.get_bb_y2 = self.x - 47, self.y-56, self.x+47, self.y+35
        self.knight_x_location = 480
        self.face_dir, self.move, self.speed = 1, 0, 1
        self.hp_max, self.hp_now,  self.power = 1000, 1000, 100

        self.frame_Idle, self.frame_Idle_timer = 0, 0
        self.timer = 0
        self.invincible, self.invincible_timer = False,  0

        self.image_Idle = load_image('mon_swamp_dungeon17_01.png')
        self.image_hp_bar = load_image('hp_bar.png')

        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태 -- Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle} #슬라임이 보는 시선의 방향에서 일정거리 안에 knight가 있으면 attack으로 전환
            }
        )


    def update(self):
        self.state_machine.update()

        if 0 <= self.knight_x_location - self.speed*self.move <= 1920:
            self.knight_x_location -= self.speed * self.move

        if 480 < self.knight_x_location<1440:
            self.x += self.move                 #그려지는 위치만 달라짐

        self.world += self.speed * self.face_dir
        self.x += self.speed * self.face_dir

        if self.hp_now <= 0:
            game_world.remove_object(self)
            print('slime is dead')

        if self.invincible:
            self.invincible_timer += 1

            # 24프레임 후 무적 초기화
        if self.invincible_timer == 29:
            self.invincible = False
            self.invincible_timer = 0

        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.image_hp_bar.clip_draw(0, 0, 50, 50, self.x, self.y+50, self.hp_now // 10 ,5)


    def get_bb(self):
        return self.get_bb_x1, self.get_bb_y1, self.get_bb_x2, self.get_bb_y2

    def power(self):
        return self.power


    def handle_collision(self, group, other, power):
        # fill here
        if group == 'sword:monster':
            if not self.invincible:
                self.hp_now -= power
                self.invincible = True
        pass