#world = []
#world [0] = 백그라운드 객체들
#world [1] = 포어그라운드 객체들 -위에 그려야 할 객체들
world = [[],[]]

def add_object(o, depth):
    world[depth].append(o)

def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return # 지우는 미션은 달성, 그 후 멈추기
print('에러! 존재하지 않은 객체를 지운거 같은데?')