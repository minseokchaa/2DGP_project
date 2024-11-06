from pico2d import *
from pygame.event import event_name
import game_world
from knight import Knight
from backgorund_swamp import Bg_swamp
from backgorund_swamp import Tile_ground_swamp


# Game object class here
running = True

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                knight.handle_event(event)  # input 이벤트를 boy에게 전달하고 있다.
                background_swamp.handle_event(event)  # input 이벤트를 background에 전달하고 있다.
                tile_ground_swamp.handle_event(event)  # input 이벤트를 tile_ground_swamp에 전달하고 있다.

def reset_world():
    global running
    global knight
    global background_swamp
    global tile_ground_swamp

    running = True

    background_swamp = Bg_swamp()
    #game_world.add_object(background_swamp, 0)

    tile_ground_swamp = Tile_ground_swamp()
    game_world.add_object(tile_ground_swamp, 0)

    knight = Knight()
    game_world.add_object(knight, 1)



def update_world():
    game_world.update()
    pass


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas(960,800)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
