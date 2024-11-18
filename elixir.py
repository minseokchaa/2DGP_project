from pico2d import *
import server
import game_world


class Elixir_hp:
    def __init__(self, x=500, y=135):
        self.x, self.y = x, y  # 나무의 기본 위치
        self.gravity = 15
        self.elixir_red = load_image('./using_resource/'+'elixir_red.png')

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.elixir_red.w
        self.h = self.elixir_red.h

    def draw(self):
        self.elixir_red.clip_draw_to_origin(0, 0, self.w, self.h, self.x, self.y)

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())

        #이미지 파일의 0,0부터 self.w, self.h 까지 이미지를 도려내서 화면의 self.x, self.y(맨 왼쪽 아래부터)의 위치에 그린다.

    def update(self):
        self.gravity -= 1
        self.y += self.gravity
        if self.y <= 135:
            self.gravity = 0
            self.y = 135

        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.tile_ground_swamp.w)  - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.tile_ground_swamp.w) - self.cw - 1:
            self.x -= int(server.knight.move * server.knight.speed)  # 타일 이동에 맞춰 x 좌표 수정


    def get_bb(self):
            return self.x, self.y,self.x+24,self.y+35


    def get_power(self):
        return 0


    def handle_collision(self, group, other, power):
        # fill here
        if group == 'knight:elixir_hp':
            game_world.remove_object(self)

        if group == 'knight:tile_ground':
            if self.gravity <=-0.7:            #떨어지는 중에
                if self.y <= power:
                    self.y = power
                    self.gravity = 0

        if group == 'knight:tile_midair':
            if self.gravity <= -0.7:
                if self.y < power:
                    self.y = power
                    self.gravity = 0
        pass

class Elixir_power:
    def __init__(self, x=500, y=135):
        self.x, self.y = x, y  # 나무의 기본 위치
        self.gravity = 15
        self.elixir_yellow = load_image('./using_resource/'+'elixir_yellow.png')

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.elixir_yellow.w
        self.h = self.elixir_yellow.h

    def draw(self):
        self.elixir_yellow.clip_draw_to_origin(0, 0, self.w, self.h, self.x, self.y)

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())

        #이미지 파일의 0,0부터 self.w, self.h 까지 이미지를 도려내서 화면의 self.x, self.y(맨 왼쪽 아래부터)의 위치에 그린다.

    def update(self):
        self.gravity -= 1
        self.y += self.gravity
        if self.y <= 135:
            self.gravity = 0
            self.y = 135

        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.tile_ground_swamp.w)  - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.tile_ground_swamp.w) - self.cw - 1:
            self.x -= int(server.knight.move * server.knight.speed)  # 타일 이동에 맞춰 x 좌표 수정


    def get_bb(self):
            return self.x, self.y,self.x+24,self.y+35


    def get_power(self):
        return 0

    def handle_collision(self, group, other, power):
        # fill here
        if group == 'knight:elixir_power':
            game_world.remove_object(self)

        if group == 'knight:tile_ground':
            if self.gravity <=-0.7:            #떨어지는 중에
                if self.y <= power:
                    self.y = power
                    self.gravity = 0

        if group == 'knight:tile_midair':
            if self.gravity <= -0.7:
                if self.y < power:
                    self.y = power
                    self.gravity = 0
        pass
