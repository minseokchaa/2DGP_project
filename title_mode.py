from pico2d import *
import game_framework
import play_mode
from server import knight

x=0
decreasing = False
inhalation = True

knight_y = 450

def init():
    global title_back_ground
    global Night_of_Knight_title
    global press_any_key_to_start
    global title_knight
    title_back_ground = load_image('./using_resource/'+'title_back_ground.png')
    Night_of_Knight_title = load_image('./using_resource/' + 'Night_of_Knight_title.png')
    press_any_key_to_start = load_image('./using_resource/' + 'press_any_key_to_start.png')
    title_knight = load_image('./using_resource/' + 'title_knight.png')

def finish():
    global title_back_ground
    global Night_of_Knight_title
    global press_any_key_to_start
    global title_knight

    del title_back_ground
    del Night_of_Knight_title
    del press_any_key_to_start
    del title_knight

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    title_back_ground.draw(800,450)
    Night_of_Knight_title.draw(500,600)
    press_any_key_to_start.draw(500,200)
    title_knight.draw(800,knight_y,1600,960)
    update_canvas()

def update():
    global x
    global decreasing
    global knight_y
    global inhalation
    press_any_key_to_start.opacify(255-x)
    if decreasing:  # 감소 상태라면
        x -= 3
        if x == 0:  # x가 0이 되면 증가로 전환
            decreasing = False
    else:  # 증가 상태라면
        x += 3
        if x == 255:  # x가 255가 되면 감소로 전환
            decreasing = True

    if inhalation:
        knight_y +=0.1
        if knight_y >= 460:
            inhalation = False
    else:
        knight_y -= 0.1
        if knight_y <= 440:
            inhalation = True


    pass

def pause():
    pass
def resume():
    pass