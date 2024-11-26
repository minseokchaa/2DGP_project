from xml.sax.saxutils import escape
from pico2d import *
import random
import game_world_boss_room
import server
import game_framework
import play_mode

from game_world_boss_room import add_collision_pair_boss_room, add_collision_pair_for_tile
from knight import Knight
from boss_room import Bg_Boss_room, Tile_midair
from boss import Boss

# Game object class here
running = True
view_box = False

def handle_events():
    global running
    global view_box

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b:
            view_box = not view_box
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                server.knight.handle_event(event)  # input 이벤트를 boy에게 전달하고 있다.
                pass


def init():
    global running
    global knight

    running = True

    server.background = Bg_Boss_room()
    game_world_boss_room.add_object(server.background, 0)
    add_collision_pair_for_tile('knight:tile_ground', None, server.background)

    positions = [200, 350, 1050, 1200]
    for i in positions:
        server.tile_midair_boss = Tile_midair(i, 210)
        game_world_boss_room.add_object(server.tile_midair_boss, 0)
        add_collision_pair_for_tile('knight:tile_midair', None, server.tile_midair_boss)

        server.tile_midair_boss = Tile_midair(i, 420)
        game_world_boss_room.add_object(server.tile_midair_boss, 0)
        add_collision_pair_for_tile('knight:tile_midair', None, server.tile_midair_boss)

    boss = Boss()
    game_world_boss_room.add_object(boss, 1)
    add_collision_pair_boss_room('sword:boss', None, boss)

    server.knight = server.knight
    server.knight.x = 360
    game_world_boss_room.add_object(server.knight, 1)

    add_collision_pair_boss_room('knight:monster', server.knight, None)
    add_collision_pair_for_tile('knight:tile_ground', server.knight, None)
    add_collision_pair_for_tile('knight:tile_midair', server.knight, None)

def finish():
    game_world_boss_room.clear()
    pass

def update():
    game_world_boss_room.update()
    game_world_boss_room.handle_collisions()
    game_world_boss_room.tile_handle_collisions()

    pass

def draw():
    clear_canvas()
    game_world_boss_room.render()
    if view_box:
        game_world_boss_room.draw_rectangle_all()
    update_canvas()


def pause():
    pass
def resume():
    pass