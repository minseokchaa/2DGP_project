from pico2d import load_image, get_time, draw_rectangle
from state_machine import StateMachine, too_far_to_first

def find_knight(monster): #knight를 찾았을 때  state machine에 이벤트 생성

    monster.state_machine.add_event(('Find_knight', 0))
    pass

class Idle:
    @staticmethod
    def enter(small_slime1, e):
        small_slime1.wait_time = get_time()
        pass

    @staticmethod
    def exit(small_slime1, e):
        pass

    @staticmethod
    def do(small_slime1):
        if small_slime1.frame_Idle_timer >= 10:  # idle 애니메이션
            small_slime1.frame_Idle = (small_slime1.frame_Idle + 1) % 4
            small_slime1.frame_Idle_timer = 0
        else:
            small_slime1.frame_Idle_timer += 1

        if small_slime1.timer > 200:     #3초마다 방향전환
            if small_slime1.face_dir == 1:
                small_slime1.face_dir = -1
                small_slime1.timer = 0
            else:
                small_slime1.face_dir = 1
                small_slime1.timer = 0
        small_slime1.timer +=1

        pass

    @staticmethod
    def draw(small_slime1):
        if small_slime1.face_dir == 1:
            small_slime1.image_Idle.clip_composite_draw(small_slime1.frame_Idle * 94, 0, 94, 112, 0, 'h',small_slime1.x, small_slime1.y, 94,112)
        elif small_slime1.face_dir == -1:
            small_slime1.image_Idle.clip_draw(small_slime1.frame_Idle * 94, 0, 94, 112, small_slime1.x,small_slime1.y)
        pass

class Attack:
    @staticmethod
    def enter(small_slime1, e):
        pass

    @staticmethod
    def exit(small_slime1, e):
        pass

    @staticmethod
    def do(small_slime1):

        if abs(small_slime1.x - small_slime1.x_first) > 400:    #처음 위치에서 400만큼 떨어지면 Idle 상태로 돌아가기
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

class Small_slime1:
    def __init__(self):
        self.x, self.y, self.world = 700, 167, 700
        self.x_first, self.y_first = 700, 167      #초기 위치 (700, 167)
        self.y_foot = self.y - 35
        self.gravity = 0
        self.face_dir, self.move, self.speed = 1, 0, 1
        self.hp_max, self.hp_now,  self.power = 1000, 1000, 100
        self.frame_Idle, self.frame_Idle_timer = 0, 0
        self.timer = 0

        self.image_Idle = load_image('mon_swamp_dungeon17_01.png')
        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태 -- Idle
        self.state_machine.set_transitions(
            {
                Idle: {}, #슬라임이 보는 시선의 방향에서 일정거리 안에 knight가 있으면 attack으로 전환
                Attack: {too_far_to_first: Idle} #초기 슬라임 위치에서 일정거리 이상 벗어나면 idle로 전환
            }
        )


    def update(self):
        self.state_machine.update()
        self.x += self.speed * self.face_dir
        self.world += self.speed * self.face_dir
        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        bb = self.get_bb()
        if bb:
            draw_rectangle(*bb)

    def get_bb(self):
        return self.x - 47, self.y-56, self.x+47, self.y+56
