#world = []
#world [0] = 백그라운드 객체들
#world [1] = 포어그라운드 객체들 -위에 그려야 할 객체들
world = [[],[]]

collision_pairs = {}
collision_pairs_for_tile = {}

def add_collision_pair_boss_room(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]        #초기화
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_collision_pair_for_tile(group, a, b):
    if group not in collision_pairs_for_tile:
        collision_pairs_for_tile[group] = [[],[]]        #초기화
    if a:
        collision_pairs_for_tile[group][0].append(a)
    if b:
        collision_pairs_for_tile[group][1].append(b)


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


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

def clear():
    for layer in world:
        layer.clear()
    return None

def draw_rectangle_all():
    for layer in world:
        for o in layer:
            o.draw_rectangle()


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return # 지우는 미션은 달성, 그 후 멈추기
    print('에러! 존재하지 않은 객체를 지운거 같은데?')

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b, b.get_power())
                    b.handle_collision(group, a, a.get_power())

def tile_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if top_b >= bottom_a >= top_b-30:
        if left_a < right_b and right_a > left_b:

            return True
        else: return False

def tile_handle_collisions():
    for group, pairs in collision_pairs_for_tile.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if tile_collide(a, b):
                    left_b, bottom_b, right_b, top_b = b.get_bb()
                    a.handle_collision(group, b, top_b)