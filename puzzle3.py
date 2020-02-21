def is_between(point, start, end):
    checks = ((min(start, end, point) != point), (max(start, end, point) != point), (point == start or point == end))
    passes = 0
    for i in checks:
        if i:
            passes += 1
    if passes >= 2:
        return True
    return False

class Line:
    def __init__(self, start, end, direction, distance, total_distance):
        self.start = start
        self.end = end
        self.direction = direction
        self.distance = distance
        self.total_distance = total_distance

    @property
    def start_x(self):
        return self.start[0]
    
    @property
    def end_x(self):
        return self.end[0]
    
    @property
    def start_y(self):
        return self.start[1]
    
    @property
    def end_y(self):
        return self.end[1]
    
    @property
    def distance_to_point(self):
        return self.total_distance
    
    def is_horizontal(self):
        return self.direction in ['L', 'R']

    def is_vertical(self):
        return self.direction in ['U', 'D']
        
    def intersects_with(self, line2):
        # print(self.start, self.end)
        # print(line2.start, line2.end)
        total_distance = self.distance_to_point + line2.distance_to_point
        
        # does not handle same orientation
    
        # line1 horizontaly, line2 vertical
        if is_between(line2.start_x, self.start_x, self.end_x) and is_between(self.start_y, line2.start_y, line2.end_y):
            # line1 R: 2.startx - 1.startx
            if self.direction == "R":
                total_distance += abs(line2.start_x - self.start_x)
            # line1 L: 1.startx - 2.startx
            elif self.direction == "L":
                total_distance += abs(self.start_x - line2.start_x)

            # line2 U: 1.starty - 2.starty
            if line2.direction == "U":
                total_distance += abs(self.start_y - line2.start_y)
            # line2 D: 2.starty - 1.starty
            elif line2.direction == "D":
                total_distance += abs(line2.start_y - self.start_y)


            return [(line2.start_x, self.start_y, total_distance)]

        # line2 horizontal, line1 vertical
        elif line2.is_horizontal() and self.is_vertical() and is_between(self.start_x, line2.start_x, line2.end_x) and is_between(line2.start_y, self.start_y, self.end_y):
            if line2.direction == "R":
                total_distance += abs(self.start_x - line2.start_x)
            elif line2.direction == "L":
                total_distance += abs(line2.start_x - self.start_x)

            if self.direction == "U":
                total_distance += abs(line2.start_y - self.start_y)
            elif self.direction == "D":
                total_distance += abs(self.start_y - line2.start_y)

            return [(self.start_x, line2.start_y, total_distance)]

                
        return []

    
def calc_path(dirs):
    paths = []
    start = (0, 0)
    total_distance = 0
    for dir in dirs:
        direction = dir[0]
        distance = int(dir[1:])

        end = None
        x, y = start
        if direction == 'U':
            end = (x, y + distance) 
        elif direction == 'D':
            end = (x, y - distance) 
        elif direction == 'L':
            end = (x - distance, y)
        elif direction == 'R':
            end = (x + distance, y)

        paths.append(Line(
            start,
            end,
            direction,
            distance,
            total_distance
        ))

        start = end
        total_distance += distance

    return paths 
    

def execute_1(wire1, wire2):
    intersects = []
    wire1_path = calc_path_1(wire1)
    # print(wire1_path)
    wire2_path = calc_path_1(wire2)
    for point in wire1_path:
        if point in wire2_path:
            intersects.append(point)
    # print(intersects)
    return min(
        [
            abs(x) + abs(y) for x, y in intersects
        ]
    )

def execute(wire1, wire2):
    intersects = []
    wire1_path = calc_path(wire1)
    # print(wire1_path)
    wire2_path = calc_path(wire2)
    for line1 in wire1_path:
        for line2 in wire2_path:
            _intersects = line1.intersects_with(line2)
            # print(_intersects)
            intersects += _intersects
    
    print(intersects)
    distances = [
        abs(x) + abs(y) for x, y, _ in intersects
    ]
    if 0 in distances:
        distances.remove(0)
    print(distances)
    
    return min(distances)


def execute_shortest(wire1, wire2):
    intersects = []
    wire1_path = calc_path(wire1)
    # print(wire1_path)
    wire2_path = calc_path(wire2)
    for line1 in wire1_path:
        for line2 in wire2_path:
            _intersects = line1.intersects_with(line2)
            # print(_intersects)
            intersects += _intersects
    
    print(intersects)
    distances = [
        z for x, y, z in intersects
    ]
    if 0 in distances:
        distances.remove(0)
    # print(distances)
    
    return min(distances)


def do():
    withs open('./puzzle3_input.txt') as f:
        wire1, wire2, _ = f.read().split('\n')
        print(
            execute_shortest(wire1.split(','), wire2.split(','))
        )

do()

