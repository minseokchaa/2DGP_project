from pico2d import *
import game_world
import game_world_boss_room


class Sword:
    image = None

    def __init__(self, x , y, power, face_dir):
        self.x, self.y, self.Power, self.face_dir = x, y, power, face_dir

        pass
    def draw(self):
        pass

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())  # *을 써줌으로서 패키지를 뜯는다.

    def update(self):

        pass

    def get_power(self):
        return self.Power

    def get_bb(self):
        # fill here
        if self.face_dir==1:      #1일 때 오른쪽
            print('aa')
            return self.x +20, self.y - 200, self.x + 300, self.y
        else:
            print('bb')
            return self.x - 300, self.y - 200, self.x -20, self.y
        pass

    def handle_collision(self, group, other, power):
        # fill here
        if group == 'knight:boss_sword':
            game_world_boss_room.remove_object(self)
            pass
        pass