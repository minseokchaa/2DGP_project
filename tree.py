from pico2d import *
import server
import game_world
import game_framework
from elixir import Elixir_hp, Elixir_power
from game_world import add_collision_pair, add_collision_pair_for_tile

PIXEL_PER_METER = (10.0 / 0.12)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)



class Dead_tree1:
    def __init__(self, x=500, y=135, type = 0):
        self.x, self.y, self.i = x, y, 1  # 나무의 기본 위치
        self.type = type        #1 = hp 엘릭서, 2 - 공격력 엘릭서, 3- 폭발
        self.db_dead_tree_1 = load_image('./using_resource_image/'+'ob_dead_tree_1.png')
        self.invincible, self.invincible_timer = False, 0
        self.life =5

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.db_dead_tree_1.w
        self.h = self.db_dead_tree_1.h

        self.tree_hit1, self.tree_hit2 = load_wav('./using_resource_sound/'+'tree_hit1.wav'), load_wav('./using_resource_sound/'+'tree_hit2.wav')
        self.tree_destroyed = load_wav('./using_resource_sound/'+'tree_destroyed.wav')

        self.tree_hit1.set_volume(48), self.tree_hit2.set_volume(48), self.tree_destroyed.set_volume(48)

    def draw(self):
        self.db_dead_tree_1.clip_draw_to_origin(0, 0, self.w, self.h, self.x, self.y,170,170)

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())

        #이미지 파일의 0,0부터 self.w, self.h 까지 이미지를 도려내서 화면의 self.x, self.y(맨 왼쪽 아래부터)의 위치에 그린다.

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.background.w) - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.background.w) - self.cw - 1:
            self.x -= int(server.knight.move * RUN_SPEED_PPS * game_framework.frame_time)  # 타일 이동에 맞춰 x 좌표 수정

        if self.life == 0:
            self.i -= 0.02
            self.db_dead_tree_1.opacify(self.i)
            self.invincible = True
            self.invincible_timer = 0

        if self.i <=0:
            game_world.remove_object(self)
            if self.type ==1:
                elixir_hp = Elixir_hp(self.x+80, self.y)
                game_world.add_object(elixir_hp, 1)
                add_collision_pair('knight:elixir_hp', None, elixir_hp)
                add_collision_pair_for_tile('knight:tile_ground', elixir_hp, None)
                add_collision_pair_for_tile('knight:tile_midair', elixir_hp, None)
            elif self.type ==2:
                elixir_power = Elixir_power(self.x+80, self.y)
                game_world.add_object(elixir_power, 1)
                add_collision_pair('knight:elixir_power', None, elixir_power)
                add_collision_pair_for_tile('knight:tile_ground', elixir_power, None)
                add_collision_pair_for_tile('knight:tile_midair', elixir_power, None)

        if self.invincible:
            self.invincible_timer += 1
            if 2 <= self.invincible_timer < 6:
                self.x -= 1
            if 6 <= self.invincible_timer < 10:
                self.x += 1

        if self.invincible_timer == 10:
            self.db_dead_tree_1 = load_image('./using_resource_image/'+'ob_dead_tree_1.png')

        if self.invincible_timer == 29:
            if self.life != 0:
                self.invincible = False
                self.invincible_timer = 0

    def get_bb(self):
            return self.x+60, self.y,self.x+110,self.y+150


    def get_power(self):
        return 0


    def handle_collision(self, group, other, power):
        # fill here
        if group == 'sword:tree':
            if not self.invincible:
                self.life -=1
                self.invincible = True
                self.db_dead_tree_1 = load_image('./using_resource_image/'+'ob_dead_tree_1_hit.png')

                if self.life > 0 and self.life % 2 == 0:
                    self.tree_hit1.play()
                elif self.life > 0 and self.life % 2 != 0:
                    self.tree_hit2.play()

                if self.life == 0:
                    self.tree_destroyed.play()
        pass

class Dead_tree2:
    def __init__(self, x=500, y=135, type = 0):
        self.x, self.y, self.i = x, y, 1  # 나무의 기본 위치
        self.x, self.y = x, y  # 나무의 기본 위치
        self.type = type  # 1 = hp 엘릭서, 2 - 공격력 엘릭서, 3- 폭발
        self.ob_dead_tree_2 = load_image('./using_resource_image/'+'ob_dead_tree_2.png')
        self.invincible, self.invincible_timer = False, 0
        self.life =5

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.ob_dead_tree_2.w
        self.h = self.ob_dead_tree_2.h

        self.tree_hit1, self.tree_hit2 = load_wav('./using_resource_sound/'+'tree_hit1.wav'), load_wav('./using_resource_sound/'+'tree_hit2.wav')
        self.tree_destroyed = load_wav('./using_resource_sound/'+'tree_destroyed.wav')
        self.tree_hit1.set_volume(48), self.tree_hit2.set_volume(48), self.tree_destroyed.set_volume(48)

    def draw(self):
        self.ob_dead_tree_2.clip_draw_to_origin(0, 0, self.w, self.h, self.x, self.y,150,150)

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())

        #이미지 파일의 0,0부터 self.w, self.h 까지 이미지를 도려내서 화면의 self.x, self.y(맨 왼쪽 아래부터)의 위치에 그린다.

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.background.w) - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.background.w) - self.cw - 1:
            self.x -= int(server.knight.move * RUN_SPEED_PPS * game_framework.frame_time)  # 타일 이동에 맞춰 x 좌표 수정

        if self.life == 0:
            self.i -= 0.02
            self.ob_dead_tree_2.opacify(self.i)
            self.invincible = True
            self.invincible_timer = 0

        if self.i <=0:
            game_world.remove_object(self)
            if self.type == 1:
                elixir_hp = Elixir_hp(self.x+75, self.y)
                game_world.add_object(elixir_hp, 1)
                add_collision_pair('knight:elixir_hp', None, elixir_hp)
                add_collision_pair_for_tile('knight:tile_ground', elixir_hp, None)
                add_collision_pair_for_tile('knight:tile_midair', elixir_hp, None)
            elif self.type == 2:
                elixir_power = Elixir_power(self.x+75, self.y)
                game_world.add_object(elixir_power, 1)
                add_collision_pair('knight:elixir_power', None, elixir_power)
                add_collision_pair_for_tile('knight:tile_ground', elixir_power, None)
                add_collision_pair_for_tile('knight:tile_midair', elixir_power, None)

        if self.invincible:
            self.invincible_timer += 1
            if 2 <= self.invincible_timer < 6:
                self.x -= 1
            if 6 <= self.invincible_timer < 10:
                self.x += 1

        if self.invincible_timer == 10:
            self.ob_dead_tree_2 = load_image('./using_resource_image/'+'ob_dead_tree_2.png')

        if self.invincible_timer == 29:
            if self.life !=0:
                self.invincible = False
                self.invincible_timer = 0

    def get_bb(self):
            return self.x+50, self.y,self.x+100,self.y+150


    def get_power(self):
        return 0


    def handle_collision(self, group, other, power):
        # fill here
        if group == 'sword:tree':
            if not self.invincible:
                self.life -=1
                self.invincible = True
                self.ob_dead_tree_2 = load_image('./using_resource_image/'+'ob_dead_tree_2_hit.png')

                if self.life > 0 and self.life % 2 == 0:
                    self.tree_hit1.play()
                elif self.life > 0 and self.life % 2 != 0:
                    self.tree_hit2.play()

                if self.life == 0:
                    self.tree_destroyed.play()
        pass

class Alive_tree1:
    def __init__(self, x=500, y=135, type = 0):
        self.x, self.y, self.i = x, y, 1  # 나무의 기본 위치
        self.type = type        #1 = hp 엘릭서, 2 - 공격력 엘릭서, 3- 폭발
        self.ob_tree_3 = load_image('./using_resource_image/'+'ob_tree_3.png')
        self.invincible, self.invincible_timer = False, 0
        self.life =13

        self.tree_hit1, self.tree_hit2 = load_wav('./using_resource_sound/'+'tree_hit1.wav'), load_wav('./using_resource_sound/'+'tree_hit2.wav')
        self.tree_destroyed = load_wav('./using_resource_sound/'+'tree_destroyed.wav')
        self.tree_hit1.set_volume(48), self.tree_hit2.set_volume(48), self.tree_destroyed.set_volume(48)


        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.ob_tree_3.w
        self.h = self.ob_tree_3.h

    def draw(self):
        self.ob_tree_3.clip_draw_to_origin(0, 0, self.w, self.h, self.x, self.y,398,366)

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())

        #이미지 파일의 0,0부터 self.w, self.h 까지 이미지를 도려내서 화면의 self.x, self.y(맨 왼쪽 아래부터)의 위치에 그린다.

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, int(server.background.w) - self.cw - 1)

        if self.window_left != 0 and self.window_left != int(server.background.w) - self.cw - 1:
            self.x -= server.knight.move * int(RUN_SPEED_PPS * game_framework.frame_time)  # 타일 이동에 맞춰 x 좌표 수정



        if self.life ==0:
            self.i -= 0.007
            self.ob_tree_3.opacify(self.i)
            self.invincible = True
            self.invincible_timer = 0

        if self.i <= 0:
            game_world.remove_object(self)
            # forest_guardian = Forest_guardian(self.x+80, self.y)      #forest_guardian 생성
            # game_world.add_object(forest_guardian, 1)
            # add_collision_pair('knight:monster', None, forest_guardian)

        if self.invincible:
            self.invincible_timer += 1
            if 2 <= self.invincible_timer < 6:
                self.x -=0.5
            if 6 <= self.invincible_timer < 10:
                self.x +=0.5

        if self.invincible_timer == 29:
            self.invincible = False
            self.invincible_timer = 0

    def get_bb(self):
            return self.x+230, self.y,self.x+330,self.y+150


    def get_power(self):
        return 0


    def handle_collision(self, group, other, power):
        # fill here
        if group == 'sword:tree':
            if not self.invincible:
                self.life -=1
                self.invincible = True

                if self.life > 0 and self.life % 2 == 0:
                    self.tree_hit1.play()
                elif self.life > 0 and self.life % 2 != 0:
                    self.tree_hit2.play()

                if self.life == 0:
                    self.tree_destroyed.play()
