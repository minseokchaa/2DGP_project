from pico2d import *
import server
import game_world


class Dead_tree:
    def __init__(self, x=500, y=135):
        self.x, self.y = x, y  # 나무의 기본 위치
        self.dx, self.dy = 0 , 0
        self.db_dead_tree_1 = load_image('ob_dead_tree_1.png')

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.db_dead_tree_1.w
        self.h = self.db_dead_tree_1.h

    def draw(self):
        # 나무는 타일의 좌표에 맞춰서 그려져야 한다.
        # 타일의 이동에 맞춰 나무도 그려지도록 수정
        self.db_dead_tree_1.clip_draw_to_origin(0, 0, self.w, self.h, self.x, self.y)
        draw_rectangle(*self.get_bb())
        #이미지 파일의 0,0부터 self.w, self.h 까지 이미지를 도려내서 화면의 self.x, self.y(맨 왼쪽 아래)의 위치에 그린다.

    def update(self):
        # 타일의 이동을 기준으로 Dead_tree 위치 업데이트
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, 1920 - self.cw - 1)

        if self.window_left != 0 and self.window_left != 1920 - self.cw - 1:
            self.x -= int(server.knight.move * server.knight.speed)  # 타일 이동에 맞춰 x 좌표 수정

    def get_bb(self):
            return self.x, self.y,self.x+101,self.y+103

    def power(self):
        return 0
    def handle_collision(self, group, other, power):
        # fill here
        if group == 'sword:tree':
            game_world.remove_object(self)
        pass

