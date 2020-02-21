from fractions import gcd

def calc_grav_coords(coord1, coord2):
    if coord1 == coord2:
        return (0, 0)
    elif coord1 > coord2:
        return (-1, 1)
    elif coord1 < coord2:
        return (1, -1)

class Moon:
    def __init__(self, position=None, velocity=(0, 0, 0)):
        "lists of x, y, z"
        self.position = position
        self.velocity = velocity
        self.gravities = []
        
    def add_gravity(self, gravity):
        self.gravities.append(gravity)
        
    def apply_gravities(self):
        # print(self.gravities)
        while len(self.gravities) > 0:
            grav = self.gravities.pop()
            self._update_velocity(grav)
        # print(self.gravities)
        self._update_position()
    
    def _update_velocity(self, grav):
        new_velocity = tuple(map(
            lambda v: v[0] + v[1],
            zip(self.velocity, grav)
        ))
        # print(new_velocity)
        self.velocity = new_velocity
        
    def _update_position(self):
        # print(self.velocity)
        new_position = tuple(map(
            lambda p: p[0] + p[1],
            zip(self.position, self.velocity)
        ))
        # print(new_position)
        self.position = new_position
   
    @property 
    def energy(self):
        potential = sum(map(
            lambda x: abs(x),
            self.position
        ))
        kinetic = sum(map(
            lambda x: abs(x),
            self.velocity
        ))
        return potential * kinetic
        
    def __repr__(self):
        return "Moon"

class GravPull:
    def __init__(self, moon1, moon2):
        self.moon1 = moon1
        self.moon2 = moon2

    def calculate_gravity(self):
        moon1_delta, moon2_delta = calc_grav_deltas(self.moon1, self.moon2)
        
        self.moon1.add_gravity(moon1_delta)
        self.moon2.add_gravity(moon2_delta)
        return moon1_delta, moon2_delta
        
    def __repr__(self):
        return f"GravPull {self.moon_1}, {self.moon_2}"
        

def calc_grav_deltas(moon1, moon2):
    x1, y1, z1 = moon1.position
    x2, y2, z2 = moon2.position

    x1_delta, x2_delta = calc_grav_coords(x1, x2)
    y1_delta, y2_delta = calc_grav_coords(y1, y2)
    z1_delta, z2_delta = calc_grav_coords(z1, z2)
    
    return (
        (x1_delta, y1_delta, z1_delta),
        (x2_delta, y2_delta, z2_delta)
    )
    
def update_moons(moons, steps):
    vertexes = []
    edges = []
    for moon in moons:
        for vertex in vertexes:
            grav_pull = GravPull(moon, vertex)
            edges.append(grav_pull)
        vertexes.append(moon)

    for _ in range(0, steps):
        for edge in edges:
            edge.calculate_gravity()
            
        for moon in moons:
            # print(moon.position, moon.gravities)
            moon.apply_gravities()

    return moons
    
def calculate_energy(moons):
    return sum(map(
        lambda moon: moon.energy,
        moons
    ))

def calculate_repeat(moons):
    def hash_moons(_moons):
        return list(map(
            lambda a: str(a),
            zip(*map(lambda m: m.position, _moons))
        ))
        
    # print(hash_moons(moons))
    ixs, iys, izs = hash_moons(moons)
    x_repeat_steps = None
    y_repeat_steps = None
    z_repeat_steps = None

    steps = 1
    # not sure why i have to initialise with 1
    while x_repeat_steps is None or y_repeat_steps is None or z_repeat_steps is None:
        steps += 1
        update_moons(moons, steps=1)
        xs, ys, zs = hash_moons(moons)
        
        if ixs == xs and x_repeat_steps is  None:
            x_repeat_steps = steps
            
        if iys == ys and y_repeat_steps is None:
            y_repeat_steps = steps
        
        if izs == zs and z_repeat_steps is None:
            z_repeat_steps = steps
        
    print(x_repeat_steps, y_repeat_steps, z_repeat_steps)
    
    lcm = x_repeat_steps
    for n in (y_repeat_steps, z_repeat_steps):
        lcm = lcm * n/gcd(int(lcm), n)

    return lcm


def execute_a():
    moons = (
        Moon(position=(-13, -13, -13)), Moon(position=(5, -8, 3)), Moon(position=(-6, -10, -3)), Moon(position=(0, 5, -5))
    )
    update_moons(moons, steps=1000)
    total = calculate_energy(moons)
    
    print(total)

def execute_b():
    moons = (
        Moon(position=(-13, -13, -13)), Moon(position=(5, -8, 3)), Moon(position=(-6, -10, -3)), Moon(position=(0, 5, -5))
    )
    steps = calculate_repeat(moons)
    print(steps)
    
    
execute_b()

