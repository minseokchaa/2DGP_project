from pico2d import load_image, get_time, draw_rectangle

from state_machine import StateMachine, space_down, right_down, left_down, left_up, right_up, start_event, landing, attack_end, a_down, no_stamina, d_down, d_up


WIDTH = 960

# 상태를 클래스를 통해서 정의함
class Idle:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(knight, e):
        knight.start_time = get_time()
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
        if knight.frame_Idle_timer >= 15:  # idle 애니메이션
            knight.frame_Idle = (knight.frame_Idle + 1) % 4
            knight.frame_Idle_timer = 0
        else:
            knight.frame_Idle_timer += 1

        if knight.y == 168:
            knight.gravity = 0
        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Idle.clip_draw(knight.frame_Idle * 128, 0, 55, 70, knight.x, knight.y, 83, 105)
        else:
            knight.image_Idle.clip_composite_draw(knight.frame_Idle * 128, 0, 55, 70, 0, 'h', knight.x, knight.y, 83, 105)

        pass

class Run:
    @staticmethod
    def enter(knight, e):
        knight.attack_count = 0
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.move = 1
        elif left_down(e) or right_up(e):
            knight.face_dir = 0
            knight.move = -1
        pass

    @staticmethod
    def exit(knight,e):
        pass

    @staticmethod
    def do(knight):
        if knight.frame_Run_timer >= 8:  # run 애니메이션
            knight.frame_Run = (knight.frame_Run + 1) % 7
            knight.frame_Run_timer = 0
        else:
            knight.frame_Run_timer += 1
        if knight.y == 168:
            knight.gravity = 0
        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Run.clip_draw(knight.frame_Run * 128, 0, 70, 70, knight.x, knight.y, 105, 105)
        else:
            knight.image_Run.clip_composite_draw(knight.frame_Run * 128, 0, 70, 70, 0, 'h', knight.x, knight.y, 105, 105)
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
            knight.gravity = 18
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        if knight.frame_Jump_timer >= 15:  # jump 애니메이션
            knight.frame_Jump = (knight.frame_Jump + 1) % 6
            knight.frame_Jump_timer = 0
        else:
            knight.frame_Jump_timer += 1

        knight.gravity -= 1
        if knight.y <= 168:
            knight.gravity = 0
            knight.y = 168
            knight.state_machine.add_event(('LAND', 0))
        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Jump.clip_draw(knight.frame_Jump * 128, 0, 70, 70, knight.x, knight.y, 105, 105)
        else:
            knight.image_Jump.clip_composite_draw(knight.frame_Jump * 128, 0, 70, 70, 0, 'h', knight.x, knight.y, 105, 105)
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
            knight.gravity = 18

        knight.move = 0
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        if knight.frame_Jump_timer >= 15:  # jump 애니메이션
            knight.frame_Jump = (knight.frame_Jump + 1) % 6
            knight.frame_Jump_timer = 0
        else:
            knight.frame_Jump_timer += 1

        knight.gravity -= 1
        if knight.y <= 168:
            knight.gravity = 0
            knight.y = 168
            knight.state_machine.add_event(('LAND', 0))
        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Jump.clip_draw(knight.frame_Jump * 128, 0, 70, 70, knight.x, knight.y, 105, 105)
        else:
            knight.image_Jump.clip_composite_draw(knight.frame_Jump * 128, 0, 70, 70, 0, 'h', knight.x, knight.y, 105, 105)
        pass

class Attack:
    @staticmethod
    def enter(knight, e):
        knight.move = 0
        if a_down(e) and knight.attack_count + 1 <= 3:
            knight.attack_count += 1
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        if knight.frame_Attack_timer >= 6:  # attack 애니메이션
            knight.frame_Attack = (knight.frame_Attack + 1) % 5  # 0.06초에 1프레임, 총 4프레임 있음
            knight.frame_Attack_timer = 0
        else:
            knight.frame_Attack_timer += 1

        if knight.attack_motion <= knight.attack_count and knight.frame_Attack == 4:  # 4프레임이 다 그려졌을 때 다음 모션, 프레임 초기화
            knight.attack_motion += 1
            knight.frame_Attack = 0
        elif knight.attack_motion > knight.attack_count:
            knight.attack_motion = 1
            knight.frame_Attack = 0
            knight.attack_count = 0
            knight.state_machine.add_event(('Attack_end', 0))

        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            if knight.attack_motion == 1:
                knight.image_Attack1.clip_draw(knight.frame_Attack * 128, 0, 100, 70, knight.x + 10, knight.y, 150, 105)
            if knight.attack_motion == 2:
                knight.image_Attack2.clip_draw(knight.frame_Attack * 128, 0, 120, 70, knight.x + 20, knight.y, 180, 105)
            if knight.attack_motion == 3:
                knight.image_Attack3.clip_draw(knight.frame_Attack * 128, 0, 100, 70, knight.x + 10, knight.y, 150, 105)
            pass
        else:
            if knight.attack_motion == 1:
                knight.image_Attack1.clip_composite_draw(knight.frame_Attack * 128, 0, 100, 70, 0, 'h', knight.x - 10,
                                                       knight.y, 150, 105)
            if knight.attack_motion == 2:
                knight.image_Attack2.clip_composite_draw(knight.frame_Attack * 128, 0, 120, 70, 0, 'h', knight.x - 20,
                                                       knight.y, 180, 105)
            if knight.attack_motion == 3:
                knight.image_Attack3.clip_composite_draw(knight.frame_Attack * 128, 0, 100, 70, 0, 'h', knight.x - 10,
                                                       knight.y, 150, 105)
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
        knight.stamina_now -= 0.5  # 방어중이면 스테미나 감소
        print(knight.stamina_now)

        if knight.stamina_now < 0:
            knight.state_machine.add_event(('No_stamina', 0))
        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            knight.image_Protect.clip_draw(0, 0, 70, 70, knight.x, knight.y, 105, 105)
        else:
            knight.image_Protect.clip_composite_draw(0, 0, 70, 70, 0, 'h', knight.x, knight.y, 105, 105)
        pass


class Knight:
    def __init__(self):
        self.x, self.y, self.world = 480, 170, 480
        self.y_foot = self.y - 35
        self.gravity = 0
        self.face_dir, self.move, self.speed = 1, 0, 5
        self.hp_max, self.stamina_max, self.power = 1000, 100, 100
        self.hp_now, self.stamina_now = 1000, 100
        self.hp_draw = 150 - (self.hp_max-self.hp_now)//2
        self.stamina_draw = 150 - (self.stamina_max - self.stamina_now) // 2
        self.frame_Idle, self.frame_Idle_timer = 0, 0
        self.frame_Run, self.frame_Run_timer = 0, 0
        self.frame_Jump, self.frame_Jump_timer = 0, 0
        self.frame_Attack, self.frame_Attack_timer = 0, 0
        self.attack_motion, self.attack_count = 1, 0

        self.image_Idle = load_image('Knight_Idle.png')
        self.image_Run = load_image('Knight_Run.png')
        self.image_Jump = load_image('Knight_Jump.png')
        self.image_Attack1 = load_image('Knight_Attack 1.png')
        self.image_Attack2 = load_image('Knight_Attack 2.png')
        self.image_Attack3 = load_image('Knight_Attack 3.png')
        self.image_Protect = load_image('Knight_Protect.png')
        self.image_hp_bar = load_image('hp_bar.png')
        self.image_stamina_bar = load_image('stamina_bar.png')
        self.image_max_hp_bar = load_image('max_hp_bar.png')
        self.image_max_stamina_bar = load_image('max_stamina_bar.png')
        self.start_time = get_time()
        self.state_machine = StateMachine(self) #소년 객체의 state machine 생성
        self.state_machine.start(Idle)      #초기 상태 -- Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, space_down: Jump, a_down: Attack, d_down: Protect},
                Run: {right_up: Idle, left_up: Idle, space_down: Jump_run,a_down: Attack, d_down: Protect},
                Attack : {a_down : Attack, attack_end: Idle, right_down: Run, left_down: Run, space_down: Jump, d_down: Protect},
                Jump : {right_down: Jump_run, left_down: Jump_run, landing: Idle},
                Jump_run: {right_up: Jump, left_up: Jump, landing: Run},
                Protect: {right_down: Run, left_down: Run, space_down: Jump, d_up: Idle, no_stamina: Idle}
            }
        )

    def update(self):
        self.y += self.gravity  # 기사는 중력(gravity)에 의해 항상 y값이 줄어든다.
        if self.stamina_now < self.stamina_max:
            self.stamina_now += 0.1  # 1초에 10씩 스테미나 회복

        if 0 <= self.world + 5*self.move <= 480:
            if self.x + 5 * self.move > 10:
                self.x += self.speed*self.move
                self.world += 5 * self.move

        elif 480 < self.world+ 5*self.move <= 1440:
            self.x = 480
            self.world += self.speed * self.move

        elif 1440 < self.world+ 5*self.move <= 1920:
            if self.x + 5 * self.move < 950:
                self.x += self.speed * self.move
                self.world += 5* self.move

        self.state_machine.update()
        #print('world:', self.world)

    def handle_event(self, event):
        #event: 입력 이벤트 key mouse
        #우리가 state_machine에 전달해 줄건 ( , )
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()

        self.image_max_hp_bar.clip_draw(0, 0, 50, 50, 0, 90, self.hp_max/2, 20)
        self.image_hp_bar.clip_draw(0, 0, 50, 50, 0, 90, self.hp_now/2, 20)

        self.image_max_stamina_bar.clip_draw(0, 0, 50, 50, 0, 50, self.stamina_max*3, 20)
        self.image_stamina_bar.clip_draw(0, 0, 50, 50, 0, 50, self.stamina_now*3, 20)

        bb = self.get_bb()
        if bb:
            draw_rectangle(*bb)


    def get_bb(self):
        if self.face_dir == 1:
            if self.state_machine.cur_state == Idle:
                return self.x - 20, self.y-53, self.x+25, self.y+43
        else:
            if self.state_machine.cur_state == Idle:
                return self.x - 25, self.y - 53, self.x + 20, self.y + 43

    def get_bottom(self):
        return self.x - 20, self.y-53, self.x+25, self.y-53,



