from pico2d import load_image, get_time, draw_rectangle

from state_machine import StateMachine, space_down, right_down, left_down, left_up, right_up, start_event, landing, attack_end, a_down, no_stamina, d_down, d_up
import game_world
from game_world import add_collision_pair
from sword import Sword
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
        if knight.face_dir == 1:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 20, knight.y - 53, knight.x + 25, knight.y + 43
        else: knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 25, knight.y - 53, knight.x + 20, knight.y + 43


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
        if knight.frame_Run  == 0:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 30, knight.y - 53, knight.x + 19, knight.y + 40
            else: knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 19, knight.y - 53, knight.x + 30, knight.y + 40
        if knight.frame_Run  == 1:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 53, knight.y - 53, knight.x + 17, knight.y + 37
            else: knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 17, knight.y - 53, knight.x + 53, knight.y + 37
        if knight.frame_Run  == 2:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 53, knight.y - 53, knight.x+2, knight.y + 40
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 2, knight.y - 53, knight.x + 53, knight.y + 40
        if knight.frame_Run  == 3:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 37, knight.y - 53, knight.x + 17, knight.y + 42
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 17, knight.y - 53, knight.x + 37, knight.y + 42
        if knight.frame_Run  == 4:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 27, knight.y - 53, knight.x + 27, knight.y + 38
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 27, knight.y - 53, knight.x + 27, knight.y + 38
        if knight.frame_Run  == 5:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 53, knight.y - 53, knight.x + 15, knight.y + 36
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 15, knight.y - 53, knight.x + 53, knight.y + 36

        if knight.frame_Run  == 6:
            if knight.face_dir == 1:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 48, knight.y - 53, knight.x + 5, knight.y + 41
            else:
                knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 5, knight.y - 53, knight.x + 48, knight.y + 41
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

        if knight.face_dir:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 41, knight.y - 53, knight.x + 5, knight.y + 43
        else:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 5, knight.y - 53, knight.x + 41, knight.y + 43
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
        if knight.face_dir:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 41, knight.y - 53, knight.x +5, knight.y + 43
        else:
            knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 5, knight.y - 53, knight.x + 41, knight.y + 43

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
        global sword
        knight.move = 0
        if a_down(e) and knight.attack_count + 1 <= 3:
            knight.attack_count += 1
        sword = Sword(knight.x, knight.y, knight.power, knight.face_dir)
        game_world.add_object(sword, 1)
        add_collision_pair('sword:monster', sword, None)

    @staticmethod
    def exit(knight, e):
        game_world.remove_object(sword)
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


        if knight.attack_motion == 1:
            if knight.frame_Attack == 0:
                if knight.face_dir:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 43, knight.y - 53, knight.x + 35, knight.y + 43
                else: knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 35, knight.y - 53, knight.x + 43, knight.y + 43
            if knight.frame_Attack == 1:
                if knight.face_dir:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 37, knight.y - 53, knight.x + 22, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 22, knight.y - 53, knight.x + 37, knight.y + 43
            if knight.frame_Attack == 2:
                if knight.face_dir:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 37, knight.y - 53, knight.x + 20, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 20, knight.y - 53, knight.x + 37, knight.y + 43
            if knight.frame_Attack == 3:
                if knight.face_dir:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 36, knight.y - 53, knight.x + 25, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 25, knight.y - 53, knight.x + 36, knight.y + 43

        if knight.attack_motion == 2:
            if knight.frame_Attack == 0:
                if knight.face_dir ==1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 40, knight.y - 53, knight.x + 22, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 22, knight.y - 53, knight.x + 40, knight.y + 43
            if knight.frame_Attack == 1:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 34, knight.y - 53, knight.x + 22, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 22, knight.y - 53, knight.x + 34, knight.y + 43
            if knight.frame_Attack == 2:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 39, knight.y - 53, knight.x + 32, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 32, knight.y - 53, knight.x + 39, knight.y + 43
            if knight.frame_Attack == 3:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 43, knight.y - 53, knight.x + 32, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 32, knight.y - 53, knight.x + 43, knight.y + 43
        if knight.attack_motion == 3:
            if knight.frame_Attack == 0:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 43, knight.y - 53, knight.x + 24, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 24, knight.y - 53, knight.x + 43, knight.y + 43
            if knight.frame_Attack == 1:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 48, knight.y - 53, knight.x + 19, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 19, knight.y - 53, knight.x + 48, knight.y + 43
            if knight.frame_Attack == 2:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 43, knight.y - 53, knight.x + 40, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 40, knight.y - 53, knight.x + 43, knight.y + 43
            if knight.frame_Attack == 3:
                if knight.face_dir == 1:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 43, knight.y - 53, knight.x + 32, knight.y + 43
                else:
                    knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 32, knight.y - 53, knight.x + 43, knight.y + 43


        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir:
            if knight.attack_motion == 1:
                knight.image_Attack1.clip_draw(knight.frame_Attack * 128, 0, 100, 70, knight.x + 10, knight.y, 150, 105)
            if knight.attack_motion == 2:
                knight.image_Attack2.clip_draw(knight.frame_Attack * 128, 0, 120, 70, knight.x + 20, knight.y, 180, 105)
            if knight.attack_motion == 3:
                knight.image_Attack3.clip_draw(knight.frame_Attack * 128, 0, 110, 70, knight.x + 10, knight.y, 165, 105)
            pass
        else:
            if knight.attack_motion == 1:
                knight.image_Attack1.clip_composite_draw(knight.frame_Attack * 128, 0, 100, 70, 0, 'h', knight.x - 10,knight.y, 150, 105)
            if knight.attack_motion == 2:
                knight.image_Attack2.clip_composite_draw(knight.frame_Attack * 128, 0, 120, 70, 0, 'h', knight.x - 20,knight.y, 180, 105)
            if knight.attack_motion == 3:
                knight.image_Attack3.clip_composite_draw(knight.frame_Attack * 128, 0, 100, 70, 0, 'h', knight.x - 10,knight.y, 150, 105)
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

        if knight.stamina_now < 0:
            knight.state_machine.add_event(('No_stamina', 0))
        knight.get_bb_x1, knight.get_bb_y1, knight.get_bb_x2, knight.get_bb_y2 = knight.x - 27, knight.y - 53, knight.x + 25, knight.y + 37
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
        self.get_bb_x1, self.get_bb_y1,self.get_bb_x2,self.get_bb_y2 = self.x - 20, self.y-53, self.x+25, self.y+43
        self.gravity = 0
        self.face_dir, self.move, self.speed = 1, 0, 5
        self.hp_max, self.stamina_max, self.power = 1000, 100, 300
        self.hp_now, self.stamina_now = 1000, 100
        self.hp_decrease = 1000
        self.hp_draw = 150 - (self.hp_max-self.hp_now)//2
        self.stamina_draw = 150 - (self.stamina_max - self.stamina_now) // 2
        self.frame_Idle, self.frame_Idle_timer = 0, 0
        self.frame_Run, self.frame_Run_timer = 0, 0
        self.frame_Jump, self.frame_Jump_timer = 0, 0
        self.frame_Attack, self.frame_Attack_timer = 0, 0
        self.attack_motion, self.attack_count = 1, 0

        self.invincible, self.invincible_timer = False,  0

        self.image_Idle,self.image_Run,self.image_Jump = load_image('Knight_Idle.png'), load_image('Knight_Run.png'), load_image('Knight_Jump.png')
        self.image_Attack1,self.image_Attack2,self.image_Attack3 = load_image('Knight_Attack 1.png'), load_image('Knight_Attack 2.png'),load_image('Knight_Attack 3.png')

        self.image_Protect = load_image('Knight_Protect.png')
        self.image_hp_bar,self.image_stamina_bar = load_image('hp_bar.png'),load_image('stamina_bar.png')
        self.image_max_hp_bar, self.image_max_stamina_bar = load_image('max_hp_bar.png'), load_image('max_stamina_bar.png')
        self.image_decrease_hp_bar,self.image_ui = load_image('decreasing_hp_bar.png'), load_image('knight_ui.png')

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

        if 0 <= self.world + self.speed * self.move <= 1920:
            self.world += self.speed * self.move

        if 0 <= self.world + self.speed * self.move <= 480:
            if self.x + 5 * self.move > 10:
                self.x += self.speed*self.move

        elif 1440 < self.world+ self.speed * self.move <= 1920:
            if self.x + 5 * self.move < 950:
                self.x += self.speed * self.move
        if self.invincible:
            self.invincible_timer += 1

        # 1.5초 후 무적 상태를 해제하는 타이머 시작
        if self.invincible_timer == 150:
            self.invincible = False
            self.invincible_timer = 0
            print('무적 해제')

        self.state_machine.update()

        if self.hp_decrease > self.hp_now:
            self.hp_decrease -= 2

        if self.hp_decrease < self.hp_now:
            self.hp_decrease += 2


    def handle_event(self, event):
        #event: 입력 이벤트 key mouse
        #우리가 state_machine에 전달해 줄건 ( , )
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        if self.invincible_timer % 10 <= 5:
            self.state_machine.draw()

        self.image_max_hp_bar.clip_draw(0, 0, 50, 50, 90, 90, self.hp_max//4*3, 20)             #(90,90)을 중심으로 hp바 생성
        self.image_decrease_hp_bar.clip_draw(0, 0, 50, 50, 90, 90, self.hp_decrease//4*3 , 20)
        self.image_hp_bar.clip_draw(0, 0, 50, 50, 90, 90, self.hp_now//4*3, 20)

        self.image_max_stamina_bar.clip_draw(0, 0, 50, 50, 90, 50, self.stamina_max*3, 20)      #(90,50)을 중심으로 stamina바 생성
        self.image_stamina_bar.clip_draw(0, 0, 50, 50, 90, 50, self.stamina_now*3, 20)

        self.image_ui.clip_draw(0, 0, 130, 80, 65, 70, 130, 80)

        draw_rectangle(*self.get_bb())
        draw_rectangle(self.x-1,self.y-1,self.x+1,self.y+1)


    def get_bb(self):
            return self.get_bb_x1, self.get_bb_y1,self.get_bb_x2,self.get_bb_y2

    def get_bottom(self):
        return self.x - 20, self.y-53, self.x+25, self.y-53

    def power(self):
        return self.power

    def current_state(self):
        return str(self.state_machine.current_state)

    def take_damage(self, power):
        if not self.invincible and self.state_machine.current_state() != Protect:
            # if power !=0:
                    self.hp_now -= power
                    self.invincible = True
                    print('knight is invincible for 1.5 second')
        pass

    def handle_collision(self, group, other, power):
        # fill here
        if group == 'knight:small_slime1':
            if not self.state_machine.current_state == Protect:
                self.take_damage(power)
        pass



