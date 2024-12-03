from pico2d import *
import game_world
import game_world_boss_room


class Flame_strike:
    image = None

    def __init__(self, x ,power):
        global start_time

        self.x, self.Power = x, power
        self.y, self.disappear, self.i = 900, False, 1
        self.image = load_image('./using_resource_image/' + 'flame_strike.png')
        self.image1 = load_image('./using_resource_image/' + 'flame_strike.png')
        self.sound = load_wav('./using_resource_sound/' + 'flamestrike.wav')
        self.sound.set_volume(40)
        self.sound.play()
        self.image1.opacify(0.2)
        start_time = get_time()
        self.width = 100
        self.time = 0

        pass
    def draw(self):
        self.image1.draw(self.x, 525, self.width+10, 750)
        self.image.draw(self.x, 525,self.width,750)
        pass

    def draw_rectangle(self):
        draw_rectangle(*self.get_bb())  # *을 써줌으로서 패키지를 뜯는다.

    def update(self):
        global start_time
        self.time +=1

        if self.time %10 < 5:
            self.width+=2
        else:
            self.width -= 2

        if get_time() - start_time >= 2.0:
            self.disappear =True


        if self.disappear:
            self.i -= 0.02
            self.image.opacify(self.i)

        if self.i <0:
            game_world_boss_room.remove_object(self)

        pass

    def get_power(self):
        return self.Power

    def get_bb(self):
        # fill here
        return self.x-self.width/2, 150, self.x +self.width/2, 900
        pass

    def handle_collision(self, group, other, power):
        # fill here\

        pass