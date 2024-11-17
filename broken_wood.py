from pico2d import *
import server
import game_world
from elixir import Elixir_hp, Elixir_power
from game_world import add_collision_pair, add_collision_pair_for_tile


class Broken_wood1:
    def __init__(self, x=500, y=135, type = 0):
        self.x, self.y = x, y  # 나무의 기본 위치
        self.type = type        #1 = hp 엘릭서, 2 - 공격력 엘릭서, 3- 폭발

        self.ob_Ridges_6 = load_image('ob_Ridges_6.png')
        self.invincible, self.invincible_timer = False, 0
        self.life =4

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.ob_Ridges_6.w
        self.h = self.ob_Ridges_6.h

    def draw(self):
        self.ob_Ridges_6.clip_draw_to_origin(0, 0, self.w, self.h, self.x, self.y,70,82)

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())

        #이미지 파일의 0,0부터 self.w, self.h 까지 이미지를 도려내서 화면의 self.x, self.y(맨 왼쪽 아래부터)의 위치에 그린다.

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, 1920 - self.cw - 1)

        if self.window_left != 0 and self.window_left != 1920 - self.cw - 1:
            self.x -= int(server.knight.move * server.knight.speed)  # 타일 이동에 맞춰 x 좌표 수정

        if self.life ==0:
            game_world.remove_object(self)
            if self.type == 1:
                elixir_hp = Elixir_hp(self.x, self.y)
                game_world.add_object(elixir_hp, 1)
                add_collision_pair('knight:elixir_hp', None, elixir_hp)
                add_collision_pair_for_tile('knight:tile_ground', elixir_hp, None)
                add_collision_pair_for_tile('knight:tile_midair', elixir_hp, None)
            elif self.type == 2:
                elixir_power = Elixir_power(self.x, self.y)
                game_world.add_object(elixir_power, 1)
                add_collision_pair('knight:elixir_power', None, elixir_power)
                add_collision_pair_for_tile('knight:tile_ground', elixir_power, None)
                add_collision_pair_for_tile('knight:tile_midair', elixir_power, None)

        if self.invincible:
            self.invincible_timer += 1

        if self.invincible_timer == 10:
            self.ob_Ridges_6 = load_image('ob_Ridges_6.png')

        if self.invincible_timer == 29:
            self.invincible = False
            self.invincible_timer = 0

    def get_bb(self):
            return self.x+10, self.y,self.x+60,self.y+75

    def power(self):
        return 0


    def handle_collision(self, group, other, power):
        # fill here
        if group == 'sword:tree':
            if not self.invincible:
                self.life -=1
                self.invincible = True
                self.ob_Ridges_6 = load_image('ob_Ridges_6_hit.png')
        pass