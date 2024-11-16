from pico2d import *
import random
from pygame.event import event_name
import game_world
import server
from game_world import add_collision_pair
from knight import Knight
from swamp import Bg_swamp
from swamp import Tile_ground_swamp
from small_slime1 import Small_slime1
from tree import Dead_tree
from big_slime1 import Big_slime1

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
                server.knight.handle_event(event)  # input 이벤트를 boy에게 전달하고 있다.
                background_swamp.handle_event(event)  # input 이벤트를 background에 전달하고 있다.
                #small_slime1.handle_event(event)
                # big_slime1.handle_event(event)

def reset_world():
    global running
    global knight
    global background_swamp
    global small_slime1
    # global big_slime1

    running = True

    background_swamp = Bg_swamp()
    #game_world.add_object(background_swamp, 0)

    server.tile_swamp = Tile_ground_swamp()
    game_world.add_object(server.tile_swamp, 0)


    small_slimes1 = [Small_slime1(random.randint(500, 1000), 187) for _ in range(5)]


    server.knight = Knight()
    game_world.add_object(server.knight, 1)
    add_collision_pair('knight:small_slime1', server.knight, None)

    # big_slime1 = Big_slime1()
    # game_world.add_object(big_slime1, 0)



    tree1 = Dead_tree(700, 135)
    game_world.add_object(tree1, 1)
    add_collision_pair('sword:tree', None, tree1)

    tree2 = Dead_tree(1400, 135)
    game_world.add_object(tree2, 1)
    add_collision_pair('sword:tree', None, tree2)



    # for small_slime1 in small_slimes1:
    #     game_world.add_object(small_slime1, 1)
    #     add_collision_pair('knight:small_slime1', None, small_slime1)
    #     add_collision_pair('sword:small_slime1', None, small_slime1)

def update_world():
    game_world.update()

    game_world.handle_collisions()

    # if game_world.collide(knight, small_slime1):
    #     knight.take_damage(small_slime1.power)
    #     if knight.current_state() == 'Attack':
    #         small_slime1.take_damage(knight.power)

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
