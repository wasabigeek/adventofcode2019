from fractions import Fraction
from copy import deepcopy
from math import pi, atan2


def in_los(_asteroids, start, target):
    # print(f'{start} to {target}')
    x1, y1 = start
    x2, y2 = target

    # actually the equation is incorrect since the y axis increases downwards, but works
    dx, dy = x2 - x1, y2 - y1
    if dy == 0:
        is_blocker = lambda pos: pos[1] == y1
    elif dx == 0:
        is_blocker = lambda pos: pos[0] == x1
    else:
        gradient = Fraction(dy, dx)
        constant = y2 - gradient * x2
        is_blocker = lambda pos: pos[1] == gradient * pos[0] + constant
    
    def between_points(pos):
        return \
            (pos[0] >= min(x1, x2) and pos[0] <= max(x1, x2)) and \
            (pos[1] >= min(y1, y2) and pos[1] <= max(y1, y2))

    # make sure start and end are not included
    asteroids = list(filter(
        lambda a: a != start and a != target,
        _asteroids
    ))
    asteroids = list(filter(
        between_points,
        asteroids
    ))
    # print(asteroids)
    blockers = list(filter(
        is_blocker,
        asteroids
    ))


    if len(blockers) > 0:
        return False

    return True

def get_asteroids(chart):
    positions = []
    for y in range(0, len(chart)):
        for x in range(0, len(chart[0])):
            if chart[y][x] != ".":
                positions.append((x, y))
                
    return positions
    
def count_visibles(asteroids, start):
    # print(sorted(visible, key=lambda x: x[1]))
    return len(_find_visibles(asteroids, start))

def get_best_pos(chart):
    asteroids = get_asteroids(chart)
    # print(asteroids)
    highest = 0
    highest_pos = None

    for a in asteroids:
        visible_count = count_visibles(asteroids, a)
        # print(a, visible_count)
        if visible_count > highest:
            highest = visible_count
            highest_pos = a
            
    # print(counts)
    return highest_pos
    
def _find_visibles(asteroids, start):
    other_asteroids = list(filter(
        lambda a: a != start,
        asteroids
    ))
    # print(other_asteroids)

    return list(filter(
        lambda _a: in_los(asteroids, start, _a),
        other_asteroids
    ))
    
def print_visibles(chart, pos):
    asteroids = get_asteroids(chart)
    visibles = _find_visibles(asteroids, pos)
    
    _chart = []
    for row in chart:
        _chart.append(list(row))

    _chart[pos[1]][pos[0]] = "X"

    for v in visibles:
        _chart[v[1]][v[0]] = "v"
        
    for row in _chart:
        print(''.join(row))

def execute():
    with open("./puzzle10_input.txt") as f:
        chart = f.read().split('\n')[:-1]
    # print(chart)
    pos = get_best_pos(chart)
    print(pos)
    asteroids = get_asteroids(chart)
    count = count_visibles(asteroids, pos)
    return count

def vaporisation_order(chart):
    start = get_best_pos(chart)
    other_asteroids = set(get_asteroids(chart))
    # filter out start
    other_asteroids.remove(start)
    
    order = []
    
    # normalise so that 0,0 is the start
    def normalise(pos):
        return (pos[0] - start[0], start[1] - pos[1])
        
    def y_angle(original_pos):
        normalised = normalise(original_pos)
        # angle = 270 + (180/pi * atan2(normalised[1], normalised[0]))
        # return (angle if angle != 360 else 0)
        
        x_angle = 180/pi * atan2(normalised[1], normalised[0])
        if x_angle <= 90:
            y_angle = 90 - x_angle
        elif x_angle > 90 and x_angle < 360:
            y_angle = 450 - x_angle
            
        return y_angle
    
    while len(other_asteroids) > 0:
        # print(len(asteroids))
        visibles = _find_visibles(other_asteroids, start)

        sorted_visibles = sorted(
            visibles,
            key=lambda p: y_angle(p)
        )

        other_asteroids = other_asteroids - set(visibles)
        order += sorted_visibles
        
    [print(y_angle(p), p, normalise(p)) for p in order]
    
    return order

def execute_b():
    with open("./puzzle10_input.txt") as f:
        chart = f.read().split('\n')[:-1]
    # print(chart)
    order = vaporisation_order(chart)
    
    print(order[199][0] * 100 + order[199][1])

execute_b()

