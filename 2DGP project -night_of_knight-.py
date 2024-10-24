from pico2d import *

WIDTH, HEIGHT = 960, 800
move_x, move_y = 0, 0
direction = 1           # 1==오른쪽, 0 == 왼쪽
stage = 1               # 1== 늪지역, 2==용암지역
is_running = False
is_attacking = False
is_defending = False
is_protecting = False
is_jumping = False
background_move = True
attack_count = 0

# Game object class here

def handle_events():
    global alive, is_running, is_attacking, is_jumping, is_protecting, move_x, move_y, direction, attack_count, stage

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            alive = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                alive = False
            elif event.key == SDLK_RIGHT:
                is_running = True
                is_protecting = False
                is_attacking = False
                attack_count = 0        #공격 초기화
                move_x = -1
                direction = 1
                # 오른쪽 이동 방향키
            elif event.key == SDLK_LEFT:
                is_running = True
                is_protecting = False
                is_attacking = False
                attack_count = 0
                move_x = +1
                direction = 0
                # 왼쪽 이동 방향키
            elif event.key == SDLK_SPACE:
                if move_y == 0:
                    move_y = +18
                    is_jumping = True
            elif event.key == SDLK_a and attack_count + 1 <= 3:   #공격
                if not is_jumping:
                     is_attacking = True
                     is_running = False
                     move_x = 0         #움직임 초기화
                     attack_count += 1

            elif event.key == SDLK_d:   #방어
                is_protecting = True
                is_running = False
                is_attacking = False
                attack_count = 0  # 공격 초기화
                move_x = 0      #이동 초기화
            elif event.key == SDLK_2:   #스테이지 스킵
                stage =2
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                is_running = False
                move_x = 0
                # 오른쪽 이동 멈춤
            elif event.key == SDLK_LEFT:
                is_running = False
                move_x = 0
                # 왼쪽 이동 멈춤
            elif event.key == SDLK_d:  # 방어
                is_protecting = False

class Back_ground_swamp:
    global move_x
    def __init__(self):

        self.x = WIDTH
        self.Back_ground_swamp = load_image('bg_tile_chapter_02_02x2.png')
        self.scroll_speed = 2
    def update(self):
        global background_move
        if self.x + self.scroll_speed * move_x < WIDTH and self.x + self.scroll_speed * move_x > -1920 + WIDTH*2 and background_move:
            self.x += self.scroll_speed * move_x
        elif self.x + self.scroll_speed * move_x >= WIDTH or self.x + self.scroll_speed * move_x <= -1920 + WIDTH*2:
            background_move = False

    def handle_event(self):
        pass

    def draw(self):
        self.Back_ground_swamp.draw(self.x, HEIGHT // 2)

class Tile_swamp:
    global move_x
    i =0

    def __init__(self):
        self.x = 0
        self.tile_swamp = load_image('tile_chapter_0000_tile1_.png')
        self.scroll_speed = 5

    def update(self):
        global background_move
        if background_move:
            self.x += self.scroll_speed * move_x

    def handle_event(self):
        pass

    def draw(self):
        for i in range(37):
            self.tile_swamp.draw(self.x + 128 * i, 50,192,136)

class Back_ground_lava:
    global move_x
    def __init__(self):

        self.x = WIDTH
        self.Back_ground_lava = load_image('bg_tile_chapter_02_03x2.png')
        self.scroll_speed = 2
    def update(self):
        global background_move
        if self.x + self.scroll_speed * move_x < WIDTH and self.x + self.scroll_speed * move_x > -1920 + WIDTH*2 and background_move:
            self.x += self.scroll_speed * move_x
        elif self.x + self.scroll_speed * move_x >= WIDTH or self.x + self.scroll_speed * move_x <= -1920 + WIDTH*2:
            background_move = False

    def handle_event(self):
        pass

    def draw(self):
        self.Back_ground_lava.draw(self.x, HEIGHT // 2)

class Tile_lava:
    global move_x
    i =0

    def __init__(self):
        self.x = 0
        self.tile_lava = load_image('tile_chapter_0004_tile2.png')
        self.scroll_speed = 5

    def update(self):
        global background_move
        if background_move:
            self.x += self.scroll_speed * move_x

    def handle_event(self):
        pass

    def draw(self):
        for i in range(37):
            self.tile_lava.draw(self.x + 128 * i, 50,192,136)


class Knight:
    global is_running
    global direction
    def __init__(self):
        self.x, self.y = WIDTH//2, 168
        self.hp_max, self.stamina_max, self.power = 1000, 100, 100
        self.hp_now, self.stamina_now = 1000, 100
        self.frame_Idle, self.frame_Idle_timer = 0, 0
        self.frame_Run, self.frame_Run_timer = 0, 0
        self.frame_Jump, self.frame_Jump_timer = 0, 0
        self.frame_Attack, self.frame_Attack_timer = 0, 0
        self.attack_motion = 1

        self.image_Idle = load_image('Knight_Idle.png')
        self.image_Run = load_image('Knight_Run.png')
        self.image_Jump = load_image('Knight_Jump.png')
        self.image_Attack1 = load_image('Knight_Attack 1.png')
        self.image_Attack2 = load_image('Knight_Attack 2.png')
        self.image_Attack3 = load_image('Knight_Attack 3.png')
        self.image_Protect = load_image('Knight_Protect.png')


    def update(self):
        global background_move
        global stage
        global move_y, is_jumping, is_attacking, is_protecting, attack_count

        self.y += move_y
        move_y -=1

        if self.y == 168:
            move_y = 0
            is_jumping = False

        if self.stamina_now < self.stamina_max:
            self.stamina_now += 0.1         #1초에 10씩 스테미나 회복


        if not background_move:
            if stage == 1:
                if self.x - 5 * move_x > 10:
                    self.x -= 5 * move_x
            elif stage == 2:
                if  10 < self.x - 5 * move_x < 950:
                    self.x -= 5 * move_x

        if self.x == WIDTH//2:
            background_move = True
        if self.x > WIDTH:
            stage = 2
            self.x = WIDTH // 2
            background_move = True



        if is_running:
            if self.frame_Run_timer >= 8:  # run 애니메이션
                self.frame_Run = (self.frame_Run + 1) % 7
                self.frame_Run_timer = 0
            else:
                self.frame_Run_timer += 1
        elif is_jumping:
            if self.frame_Jump_timer >= 15:  # jump 애니메이션
                self.frame_Jump = (self.frame_Jump + 1) % 6
                self.frame_Jump_timer = 0
            else:
                self.frame_Jump_timer += 1
        elif is_attacking:
            if self.frame_Attack_timer >= 6:  # attack 애니메이션
                self.frame_Attack = (self.frame_Attack + 1) % 5     #0.06초에 1프레임, 총 4프레임 있음
                self.frame_Attack_timer = 0
            else:
                self.frame_Attack_timer += 1

            if self.attack_motion <= attack_count and self.frame_Attack == 4:   #4프레임이 다 그려졌을 때 다음 모션, 프레임 초기화
                self.attack_motion +=1
                self.frame_Attack = 0
            elif self.attack_motion > attack_count:
                is_attacking = False
                self.attack_motion = 1
                self.frame_Attack = 0
                attack_count = 0

        elif is_protecting:
            self.stamina_now -= 0.5     #방어중이면 스테미나 감소
            print(self.stamina_now)

            if self.stamina_now <0:
                is_protecting = False


        else:
            if self.frame_Idle_timer >= 15:  # idle 애니메이션
                self.frame_Idle = (self.frame_Idle + 1) % 4
                self.frame_Idle_timer = 0
            else:
                self.frame_Idle_timer += 1

    def handle_event(self):
        pass

    def draw(self):
        if is_running and self.y == 168 :
            if direction:
                self.image_Run.clip_draw(self.frame_Run * 128, 0, 70, 70, self.x, self.y,105,105)
            else:
                self.image_Run.clip_composite_draw(self.frame_Run * 128, 0, 70, 70, 0, 'h', self.x, self.y, 105, 105)

        elif is_attacking and self.y == 168:
            if direction:
                if self.attack_motion == 1:
                    self.image_Attack1.clip_draw(self.frame_Attack * 128, 0, 100, 70, self.x + 10, self.y, 150, 105)
                if self.attack_motion == 2:
                    self.image_Attack2.clip_draw(self.frame_Attack * 128, 0, 120, 70, self.x + 20, self.y, 180, 105)
                if self.attack_motion == 3:
                    self.image_Attack3.clip_draw(self.frame_Attack * 128, 0, 100, 70, self.x + 10, self.y, 150, 105)
                pass
            else:
                if self.attack_motion == 1:
                    self.image_Attack1.clip_composite_draw(self.frame_Attack * 128, 0, 100, 70, 0, 'h', self.x - 10, self.y, 150, 105)
                if self.attack_motion == 2:
                    self.image_Attack2.clip_composite_draw(self.frame_Attack * 128, 0, 120, 70, 0, 'h', self.x - 20,self.y, 180, 105)
                if self.attack_motion == 3:
                    self.image_Attack3.clip_composite_draw(self.frame_Attack * 128, 0, 100, 70, 0, 'h', self.x - 10,self.y, 150, 105)

        elif is_jumping:
            if direction:
                self.image_Jump.clip_draw(self.frame_Jump * 128, 0, 70, 70, self.x, self.y,105,105)
            else:
                self.image_Jump.clip_composite_draw(self.frame_Jump * 128, 0, 70, 70, 0, 'h', self.x, self.y, 105, 105)

        elif is_protecting:
            if direction:
                self.image_Protect.clip_draw(0, 0, 70, 70, self.x, self.y,105,105)
            else:
                self.image_Protect.clip_composite_draw(0, 0, 70, 70, 0, 'h', self.x, self.y, 105, 105)

        else: #idle
            if direction:
              self.image_Idle.clip_draw(self.frame_Idle * 128, 0, 55, 70, self.x, self.y,83,105)
            else:
                self.image_Idle.clip_composite_draw(self.frame_Idle * 128, 0, 55, 70, 0, 'h', self.x, self.y,83,105)

def reset_world():
    global alive
    global world
    global knight
    global bg_swamp, tile_swamp
    global bg_lava, tile_lava
    global stage

    alive = True
    world = []

    bg_swamp = Back_ground_swamp()
    tile_swamp = Tile_swamp()

    bg_lava = Back_ground_lava()
    tile_lava = Tile_lava()

    knight = Knight()

    world.append(knight)    #기사를 월드에 추가


def update_world():
    global stage
    if stage ==1:
        bg_swamp.update()   # 늪배경 업데이트
        tile_swamp.update() # 늪타일 업데이트
    if stage == 2:
        bg_lava.update()    # 용암배경 업데이트
        tile_lava.update()  # 용암타일 업데이트

    knight.update()  # 기사 업데이트

def render_world():
    global stage
    clear_canvas()
    if stage == 1:
        bg_swamp.draw()
        tile_swamp.draw()
    elif stage == 2:
        bg_lava.draw()
        tile_lava.draw()

    for o in world:
        o.draw()

    update_canvas()


open_canvas(WIDTH,HEIGHT)
reset_world()
# game loop

while alive:

    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()