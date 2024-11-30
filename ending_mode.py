from pico2d import *
import game_framework
import title_mode


def init():
    global image
    global ending_start_time
    global bgm

    image = load_image('./using_resource_image/' + 'ending.png')

    bgm = load_music('./using_resource_sound/' + 'chiptune-ending-212716.mp3')
    bgm.play()



    ending_start_time = get_time()

def finish():
    global image
    del image

def update():
    global ending_start_time
    if get_time() - ending_start_time >= 19.5:
        ending_start_time = get_time()
        game_framework.quit()

def draw():
    clear_canvas()
    image.draw(get_canvas_width()/2,get_canvas_height()/2)
    update_canvas()

def handle_events():

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def pause():
    pass
def resume():
    pass