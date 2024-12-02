from pico2d import *
import game_world
import game_world_boss_room
from game_world_boss_room import add_collision_pair_boss_room
from flame_strike import Flame_strike


class Crater:
    image = None

    def __init__(self, x ,power):
        global start_time

        self.x, self.Power = x, power
        self.y, self.disappear, self.i = 900, False, 0
        self.image = load_image('./using_resource_image/' + 'crater.png')
        self.image.opacify(self.i)
        start_time = get_time()
        self.width = 140
        self.time = 0

        pass
    def draw(self):
        self.image.draw(self.x, 200,self.width,100)
        pass

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())  # *을 써줌으로서 패키지를 뜯는다.

    def update(self):
        global start_time

        if self.i < 1:
            if self.disappear == False:
                self.i += 0.005
                self.image.opacify(self.i)



        if self.i >=1 :
            flame_strike = Flame_strike(self.x, self.Power)
            game_world_boss_room.add_object(flame_strike, 0)
            add_collision_pair_boss_room('knight:monster', None, flame_strike)
            self.disappear = True

        if self.disappear:
            self.i -= 0.005
            self.image.opacify(self.i)

        if self.i <0:
            game_world_boss_room.remove_object(self)

        pass

    def get_power(self):
        return self.Power

    def get_bb(self):
        # fill here
        return self.x-self.width/2, 200, self.x +self.width/2, 100
        pass

    def handle_collision(self, group, other, power):
        # fill here\

        pass