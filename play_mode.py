from pico2d import *
import random
import game_world
import server
from game_world import add_collision_pair, add_collision_pair_for_tile
from knight import Knight
from swamp import Bg_swamp, Tile_midair_swamp,Tile_ground_swamp
from small_slime1 import Small_slime1
from tree import Dead_tree1, Dead_tree2, Alive_tree1
from broken_wood import Broken_wood1, Broken_wood2
from big_slime1 import Big_slime1

# Game object class here
running = True
view_box = False

def handle_events():
    global running
    global view_box

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b:
            view_box = not view_box
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                server.knight.handle_event(event)  # input 이벤트를 boy에게 전달하고 있다.


def reset_world():
    global running
    global knight

    running = True

    server.background_swamp = Bg_swamp()
    game_world.add_object(server.background_swamp, 0)
    server.tile_ground_swamp = Tile_ground_swamp()
    game_world.add_object(server.tile_ground_swamp, 0)
    add_collision_pair_for_tile('knight:tile_ground', None, server.tile_ground_swamp)
    positions = [500, 700, 1300,1400]
    for i in positions:
        server.tile_midair_swamp = Tile_midair_swamp(i, 220)
        game_world.add_object(server.tile_midair_swamp, 0)
        add_collision_pair_for_tile('knight:tile_midair', None, server.tile_midair_swamp)
    positions = [300, 350, 550]
    for i in positions:
        server.tile_midair_swamp = Tile_midair_swamp(i, 680)
        game_world.add_object(server.tile_midair_swamp, 0)
        add_collision_pair_for_tile('knight:tile_midair', None, server.tile_midair_swamp)
    server.tile_midair_swamp = Tile_midair_swamp(300, 400)
    game_world.add_object(server.tile_midair_swamp, 0)
    add_collision_pair_for_tile('knight:tile_midair', None, server.tile_midair_swamp)
    server.tile_midair_swamp = Tile_midair_swamp(-120, 600)
    game_world.add_object(server.tile_midair_swamp, 0)
    add_collision_pair_for_tile('knight:tile_midair', None, server.tile_midair_swamp)




    small_slimes1 = [Small_slime1(random.randint(600, 2500), 200) for _ in range(4)]
    for small_slime1 in small_slimes1:
        game_world.add_object(small_slime1, 1)
        add_collision_pair('knight:monster', None, small_slime1)
        add_collision_pair('sword:monster', None, small_slime1)
    big_slime1 = Big_slime1(1400, 220)
    game_world.add_object(big_slime1, 1)
    add_collision_pair('knight:monster', None, big_slime1)
    add_collision_pair('sword:monster', None, big_slime1)

    tree1 = Dead_tree1(700, 150,1)
    game_world.add_object(tree1, 0)
    add_collision_pair('sword:tree', None, tree1)
    tree1 = Dead_tree1(300, 530, 0)
    game_world.add_object(tree1, 0)
    add_collision_pair('sword:tree', None, tree1)
    tree1 = Alive_tree1(2400, 151)
    game_world.add_object(tree1, 0)
    add_collision_pair('sword:tree', None, tree1)
    tree2 = Dead_tree2(1400, 351,2)
    game_world.add_object(tree2, 0)
    add_collision_pair('sword:tree', None, tree2)
    positions = [200, 2000]
    for i in positions:
        if i == 200: j = 1
        else: j= 2

        ridges2 = Broken_wood1(i, 151, j)
        game_world.add_object(ridges2, 0)
        add_collision_pair('sword:tree', None, ridges2)



    broken_wood1 = Broken_wood1(700, 351,1)
    game_world.add_object(broken_wood1, 0)
    add_collision_pair('sword:tree', None, broken_wood1)
    broken_wood1 = Broken_wood2(550, 811, 2)
    game_world.add_object(broken_wood1, 0)
    add_collision_pair('sword:tree', None, broken_wood1)


    server.knight = Knight()
    game_world.add_object(server.knight, 1)
    add_collision_pair('knight:monster', server.knight, None)
    add_collision_pair('knight:elixir_hp', server.knight, None)
    add_collision_pair('knight:elixir_power', server.knight, None)
    add_collision_pair_for_tile('knight:tile_ground', server.knight, None)
    add_collision_pair_for_tile('knight:tile_midair', server.knight, None)





def update_world():
    game_world.update()
    game_world.handle_collisions()
    game_world.tile_handle_collisions()

    pass


def render_world():
    clear_canvas()
    game_world.render()
    if view_box:
        game_world.draw_rectangle_all()
    update_canvas()


open_canvas(1600,900)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
