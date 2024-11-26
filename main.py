from pico2d import open_canvas, close_canvas

import game_framework
#로고 모드를 임포트 하되 start모드로 이름을 바꾼다.
import play_mode as start_mode
import title_mode
# import logo_mode
import play_boss_room



open_canvas(1600,900)
# game loop
game_framework.run(start_mode)
close_canvas()