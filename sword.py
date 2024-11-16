from pico2d import *
import game_world


class Sword:
    image = None

    def __init__(self, x , y, power, face_dir):
        self.x, self.y, self.power, self.face_dir = x, y, power, face_dir

        pass
    def draw(self):
        draw_rectangle(*self.get_bb())  # *을 써줌으로서 패키지를 뜯는다.

    def update(self):
        pass

    def power(self):
        return self.power

    def get_bb(self):
        # fill here
        if self.face_dir:
            return self.x -10, self.y-53, self.x +100, self.y+60
        else:
            return self.x - 100, self.y - 53, self.x + 10, self.y + 60
        pass

    def handle_collision(self, group, other, power):
        # fill here
        if group == 'sword:tree':
            pass
        pass