from pico2d import *

WIDTH, HEIGHT = 960, 800
move_x = 0
direction = 1
is_running = False

# Game object class here

def handle_events():
    global alive, is_running, move_x, direction

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            alive = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                alive = False
            elif event.key == SDLK_RIGHT:
                is_running = True
                move_x = -1
                direction = 1
            elif event.key == SDLK_LEFT:
                is_running = True
                move_x = +1
                direction = 0

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                is_running = False
                move_x = 0
            elif event.key == SDLK_LEFT:
                is_running = False
                move_x = 0

class Back_ground_swamp:
    global move_x
    def __init__(self):

        self.x = WIDTH
        self.Back_ground_swamp = load_image('bg_tile_chapter_02_02x2.png')
        self.scroll_speed = 5
    def update(self):
        self.x += self.scroll_speed * move_x

    def handle_event(self):
        pass

    def draw(self):
        self.Back_ground_swamp.draw(self.x, HEIGHT // 2)


class Knight:
    global is_running
    global direction
    def __init__(self):
        self.x, self.y = 400, 200
        self.hp_max, self.stamina_max, self.power = 1000, 100, 100
        self.hp_now, self.stamina_now = 1000, 100
        self.frame_Idle = 0
        self.frame_Idle_timer = 0
        self.frame_Run = 0
        self.frame_Run_timer = 0
        self.image_Idle = load_image('Knight_Idle.png')
        self.image_Run = load_image('Knight_Run.png')


    def update(self):
        if is_running:
            if self.frame_Run_timer >= 10:  # run 애니메이션
                self.frame_Run = (self.frame_Run + 1) % 7
                self.frame_Run_timer = 0
            else:
                self.frame_Run_timer += 1
        else:
            if self.frame_Idle_timer >= 15:  # idle 애니메이션
                self.frame_Idle = (self.frame_Idle + 1) % 4
                self.frame_Idle_timer = 0
            else:
                self.frame_Idle_timer += 1

    def handle_event(self):
        pass

    def draw(self):
        if is_running:
            if direction:
                self.image_Run.clip_draw(self.frame_Run * 128, 0, 70, 70, self.x, self.y,105,105)
            else:
                self.image_Run.clip_composite_draw(self.frame_Run * 128, 0, 70, 70, 0, 'h', self.x, self.y, 105, 105)
        else:
            if direction:
              self.image_Idle.clip_draw(self.frame_Idle * 128, 0, 55, 70, self.x, self.y,83,105)
            else:
                self.image_Idle.clip_composite_draw(self.frame_Idle * 128, 0, 55, 70, 0, 'h', self.x, self.y,83,105)

def reset_world():
    global alive
    global grass
    global world
    global knight
    global bg_swamp

    alive = True
    world = []

    bg_swamp = Back_ground_swamp()
    world.append(bg_swamp)

    knight = Knight()
    world.append(knight)




def update_world():

    bg_swamp.update()  # 배경 업데이트
    knight.update()  # 기사 업데이트


def render_world():
    clear_canvas()
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