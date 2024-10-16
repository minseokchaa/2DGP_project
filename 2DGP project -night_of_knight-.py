from pico2d import *

WIDTH, HEIGHT = 960, 800

# Game object class here

def handle_events():
    global alive
    global dir_x

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            alive = False

        elif event.type == SDL_KEYDOWN:

            if event.key == SDLK_ESCAPE:
              alive = False

            if event.key == SDLK_RIGHT:
                    dir_x += 1

            elif event.key == SDLK_LEFT:
                    dir_x -= 1


        elif event.type == SDL_KEYUP:

            if event.key == SDLK_RIGHT:
                dir_x -= 1

            elif event.key == SDLK_LEFT:
                dir_x += 1

class Back_ground_swamp:
    def __init__(self):

        self.x = WIDTH
        self.Back_ground_swamp = load_image('bg_tile_chapter_02_02x2.png')
        pass
    def update(self):

        self.x -= 1
        pass
    def handle_event(self):
        pass
    def draw(self):
        self.Back_ground_swamp.draw(self.x, HEIGHT // 2)


class Knight:
    def __init__(self):
        self.x, self.y = 400,200
        self.frame_Idle = 0
        self.frame_Idle_timer = 0
        self.frame_Run = 0
        self.frame_Run_timer = 0
        self.dir_x =0
        self.image_Idle = load_image('Knight_Idle.png')
        self.image_Run = load_image('Knight_Run.png')
        self.image_Dead = load_image('Knight_Dead.png')

    def update(self):
        if self.frame_Idle_timer == 15:
            self.frame_Idle = (self.frame_Idle + 1) % 4
            self.frame_Idle_timer = 0
        else:
            self.frame_Idle_timer += 1

        if self.frame_Run_timer == 10:
            self.frame_Run = (self.frame_Run + 1) % 7
            self.frame_Run_timer = 0
        else:
           self.frame_Run_timer += 1

    def handle_event(self, event):
        pass

    def draw(self):
        self.image_Idle.clip_draw(self.frame_Idle * 128, 0, 128, 128, 400, 200,170,170)
        self.image_Run.clip_draw(self.frame_Run * 128, 0, 128, 128, 400, 400,170,170)


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
    for o in world:
        o.update()
    pass


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