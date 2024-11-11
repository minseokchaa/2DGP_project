from pico2d import load_image, get_time, draw_rectangle
from state_machine import StateMachine, too_far_to_first, right_up, right_down, left_down, left_up, arrive_at_first


def find_knight(monster): #knight를 찾았을 때  state machine에 이벤트 생성

    monster.state_machine.add_event(('Find_knight', 0))
    pass

class Idle:
    @staticmethod
    def enter(big_slime1, e):
        pass

    @staticmethod
    def exit(big_slime1, e):
        if right_up(e) or left_up(e):
            big_slime1.move = 0
        elif right_down(e):
            big_slime1.move =-5
        elif left_down(e):
            big_slime1.move = 5
        pass

    @staticmethod
    def do(big_slime1):
        if big_slime1.frame_Idle_timer >= 17:  # idle 애니메이션
            big_slime1.frame_Idle = (big_slime1.frame_Idle + 1) % 4
            big_slime1.frame_Idle_timer = 0
        else:
            big_slime1.frame_Idle_timer += 1

        if big_slime1.timer > 250:     #2.5초마다 방향전환
            if big_slime1.face_dir == 1:
                big_slime1.face_dir = -1
                big_slime1.timer = 0
            else:
                big_slime1.face_dir = 1
                big_slime1.timer = 0
        big_slime1.timer +=1

        pass

    @staticmethod
    def draw(big_slime1):
        if big_slime1.face_dir == 1:
            big_slime1.image_Idle.clip_draw(big_slime1.frame_Idle * 141, 0, 141, 163, big_slime1.x,big_slime1.y)
        elif big_slime1.face_dir == -1:
            big_slime1.image_Idle.clip_composite_draw(big_slime1.frame_Idle * 141, 0, 141, 163, 0, 'h', big_slime1.x,big_slime1.y, 141, 163)
        pass

class Attack:
    @staticmethod
    def enter(big_slime1, e):
        pass

    @staticmethod
    def exit(big_slime1, e):
        if right_up(e) or left_up(e):
            big_slime1.move = 0
        elif right_down(e):
            big_slime1.move =-5
        elif left_down(e):
            big_slime1.move = 5
        pass

    @staticmethod
    def do(big_slime1):
        if big_slime1.frame_Idle_timer >= 10:  # idle 애니메이션
            big_slime1.frame_Idle = (big_slime1.frame_Idle + 1) % 4
            big_slime1.frame_Idle_timer = 0
        else:
            big_slime1.frame_Idle_timer += 1

        if abs(big_slime1.x - big_slime1.x_first) > 400:    #처음 위치에서 400만큼 떨어지면 처음 위치로 돌아가기
            big_slime1.state_machine.add_event(('Too_far_to_first', 0))
        pass

    @staticmethod
    def draw(big_slime1):
        if big_slime1.face_dir == 1:
            big_slime1.image_Idle.clip_draw(big_slime1.frame_Idle * 141, 0, 141, 163, big_slime1.x, big_slime1.y)
        elif big_slime1.face_dir == -1:
            big_slime1.image_Idle.clip_composite_draw(big_slime1.frame_Idle * 141, 0, 141, 163, 0, 'h', big_slime1.x,big_slime1.y, 141, 163)
        pass

class Return_to_Idle:
    @staticmethod
    def enter(big_slime1, e):
        pass

    @staticmethod
    def exit(big_slime1, e):
        if right_up(e) or left_up(e):
            big_slime1.move = 0
        elif right_down(e):
            big_slime1.move = -5
        elif left_down(e):
            big_slime1.move = 5
        pass

    @staticmethod
    def do(big_slime1):
        if big_slime1.frame_Idle_timer >= 10:  # idle 애니메이션
            big_slime1.frame_Idle = (big_slime1.frame_Idle + 1) % 4
            big_slime1.frame_Idle_timer = 0
        else:
            big_slime1.frame_Idle_timer += 1

        if big_slime1.world < big_slime1.x_first:
            big_slime1.face_dir = 1
            big_slime1.world += 1
            big_slime1.x += 1
        if big_slime1.world > big_slime1.x_first:
            big_slime1.face_dir = -1
            big_slime1.world -= 1
            big_slime1.x -= 1

        if big_slime1.world == big_slime1.x_first:
            big_slime1.state_machine.add_event(('Arrive_at_first', 0))
        pass

    @staticmethod
    def draw(big_slime1):
        def draw(big_slime1):
            if big_slime1.face_dir == 1:
                big_slime1.image_Idle.clip_draw(big_slime1.frame_Idle * 141, 0, 141, 163, big_slime1.x, big_slime1.y)
            elif big_slime1.face_dir == -1:
                big_slime1.image_Idle.clip_composite_draw(big_slime1.frame_Idle * 141, 0, 141, 163, 0, 'h',big_slime1.x, big_slime1.y, 141, 163)
        pass

class Big_slime1:
    def __init__(self):
        self.x, self.y, self.world = 1400, 190, 1400
        self.x_first, self.y_first = 1400, 167      #초기 위치 (1400, 180)
        self.knight_x_location = 480
        self.gravity = 0
        self.face_dir, self.move, self.speed = 1, 0, 1
        self.hp_max, self.hp_now,  self.power = 1000, 1000, 200
        self.frame_Idle, self.frame_Idle_timer = 0, 0
        self.timer = 0

        self.image_Idle = load_image('mon_swamp_Big_Undead3_2_01.png')
        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태 -- Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}, #슬라임이 보는 시선의 방향에서 일정거리 안에 knight가 있으면 attack으로 전환
                Attack: {right_down: Attack, left_down: Attack, right_up: Attack, left_up: Attack,too_far_to_first: Return_to_Idle}, #초기 슬라임 위치에서 일정거리 이상 벗어나면 idle로 전환
                Return_to_Idle: {right_down: Return_to_Idle, left_down: Return_to_Idle, right_up: Return_to_Idle, left_up: Return_to_Idle,arrive_at_first: Idle} #처음 위치로 도착하면 idle로 변환
            }
        )


    def update(self):
        self.state_machine.update()

        if 0 <= self.knight_x_location - self.speed*self.move <= 1920:
            self.knight_x_location -= self.speed * self.move

        if 480 < self.knight_x_location:
            self.x += self.move
        else:
            self.x = self.world

        self.world += self.speed * self.face_dir
        self.x += self.speed * self.face_dir

        print(self.world, self.x)
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
        return self.x - 70, self.y-81, self.x+70, self.y+81