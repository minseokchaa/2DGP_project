from pico2d import *
import server
import game_framework

PIXEL_PER_METER = (10.0 / 0.12)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Bg_Boss_room:
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y
        self.bg_boss_room = load_image('./using_resource/'+'bg_boss_room.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.bg_boss_room.w
        self.h = self.bg_boss_room.h


    def draw(self):
        self.bg_boss_room.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, self.x, self.y)

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
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.background.w) - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.background.w) - self.cw - 1:
            self.x -= int(server.knight.move * RUN_SPEED_PPS * game_framework.frame_time)  # 타일 이동에 맞춰 x 좌표 수정

    def get_bb(self):
        return self.x, self.y, self.x+200, self.y+131