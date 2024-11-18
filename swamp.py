from pico2d import *
from state_machine import StateMachine, right_down, left_down, left_up, right_up, d_down, a_down
import server

class Bg_swamp:

    def __init__(self):

        self.x = 0
        self.Back_ground_swamp = load_image('./using_resource/'+'bg_tile_chapter_02_02x2.png')

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.Back_ground_swamp.w
        self.h = self.Back_ground_swamp.h
        pass
    def update(self):
        self.window_left = clamp(0, (int(server.knight.x) - self.cw // 2)//4, 400)
        self.window_bottom = clamp(0, (int(server.knight.y) - self.ch // 2)//4, self.h - self.ch - 1)

        if self.window_left != 0 and self.window_left != int(server.tile_ground_swamp.w) - self.cw - 1:
            self.x -= int(server.knight.move * server.knight.speed)  # 타일 이동에 맞춰 x 좌표 수정


    def draw(self):
        self.Back_ground_swamp.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def draw_rectangle(self):
        pass

class Tile_ground_swamp:
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y
        self.tile_ground_swamp = load_image('./using_resource/'+'tile_chapter_0000_tile1_.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.tile_ground_swamp.w
        self.h = self.tile_ground_swamp.h


    def draw(self):
        self.tile_ground_swamp.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, self.x, self.y)

    def draw_rectangle(self):
        draw_rectangle(self.x - 1, self.y - 1, self.x + 1, self.y + 1)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.ch // 2, self.h - self.ch - 1)

    def get_bb(self):
        return 0, 0, 1920, self.y+150

class Tile_midair_swamp:
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y
        self.tile_midair_swamp = load_image('./using_resource/'+'tile_swamp.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.tile_midair_swamp.w
        self.h = self.tile_midair_swamp.h


    def draw(self):
        self.tile_midair_swamp.clip_draw_to_origin(0, 0, self.w, self.h, self.x, self.y)

    def draw_rectangle(self):
        draw_rectangle(self.x - 1, self.y - 1, self.x + 1, self.y + 1)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.tile_ground_swamp.w) - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.tile_ground_swamp.w) - self.cw - 1:
            self.x -= int(server.knight.move * server.knight.speed)  # 타일 이동에 맞춰 x 좌표 수정

    def get_bb(self):
        return self.x, self.y, self.x+200, self.y+131