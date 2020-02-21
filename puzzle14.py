from collections import deque
from math import floor, ceil

class Chemical:
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.reactions_needed = []
        if "count_produced" in kwargs:
            self.count_produced = int(kwargs.pop('count_produced'))

    def add_needed_reaction(self, ingredient, count):
        reaction = Reaction(
            ingredient=ingredient,
            ingredient_count=count,
            product=self
        )
        self.reactions_needed.append(reaction)
        
    def update(self, count_produced=None):
        if count_produced:
            self.count_produced = int(count_produced)
            
    def __repr__(self):
        return f'<{self.name}>'
        
class Fuel(Chemical):
    NAME = 'FUEL'
    
    def __init__(self, **kwargs):
        kwargs['name'] = Fuel.NAME
        kwargs['count_produced'] = 1
        super().__init__(**kwargs)


class Ore(Chemical):
    NAME = 'ORE'
    
    def __init__(self, **kwargs):
        kwargs['name'] = Ore.NAME
        kwargs['count_produced'] = 1
        super().__init__(**kwargs)

class Reaction:
    def __init__(self, **kwargs):
        self.ingredient = kwargs.pop('ingredient')  # a chemical or ore
        self.ingredient_count = int(kwargs.pop('ingredient_count'))
        self.product = kwargs.pop('product')

class ChemicalDirectory:
    def __init__(self):
        self._chemicals = {
            'FUEL': Fuel(),
            'ORE': Ore()
        }
    
    @property
    def root(self):
        return self.add_or_update(name=Fuel.NAME)

    # key assumption: there is only one way to produce a chemical
    def add_or_update(self, **chemical_kwargs):
        name = chemical_kwargs.pop('name')
        if name in self._chemicals:
            chemical = self._chemicals[name]
            chemical.update(**chemical_kwargs)
        else:
            chemical = Chemical(name=name, **chemical_kwargs)
            self._chemicals[name] = chemical
            
        return chemical

def xtraverse_reactions(root, inventory=None):
    queue = deque([root])
    ore_count = 0
    
    while len(queue) > 0:
        # print(inventory)
        # print(list(map(lambda c: c.name, queue)))
        # print(ore_count)
        
        chem = queue.pop()
        
        # record if its ore
        if type(chem) == Ore:
            ore_count += 1
        
        # check if there are leftovers
        if chem.name in inventory and inventory[chem.name] > 0:
            inventory[chem.name] -= 1
            continue
        
        # otherwise synthesise and record extra products to inventory
        inventory[chem.name] = chem.count_produced - 1

        for reaction in chem.reactions_needed:
            count_needed = reaction.ingredient_count

            # add ingredients to the queue
            queue += count_needed * [reaction.ingredient]
        
    return inventory, ore_count

def traverse_reactions(root, fuel_needed=1, inventory=None):
    "try to pass through each node in the tree once instead of spawning a traverse for each quantity"
    queue = [(root, fuel_needed)]
    ore_count = 0
    if inventory is None:
        inventory = {}

    while len(queue) > 0:
        chem, count_needed = queue.pop()
        
        if type(chem) == Ore:
            ore_count += count_needed

        # deduct existing stock
        if chem.name in inventory and inventory[chem.name] > 0:
            stock = inventory[chem.name]

            inventory[chem.name] = max(0, stock - count_needed)
            
            count_needed = max(0, count_needed - stock)

        
        # synthesise
        reaction_counts = ceil(count_needed / chem.count_produced)
        leftover = reaction_counts * chem.count_produced - count_needed
        if chem.name in inventory:
            inventory[chem.name] += leftover
        else:
            inventory[chem.name] = leftover

        # add ingredients to the queue
        for reaction in chem.reactions_needed:
            ingredient_count = reaction_counts * reaction.ingredient_count
            queue += [(
                reaction.ingredient,
                ingredient_count
            )]
        # print(queue, inventory)
        
    return ore_count
    

def build_reactions_tree(reactions_list):
    chemicals = ChemicalDirectory()
    for reaction_str in reactions_list:
        ings_str, pdt_str = reaction_str.split(' => ')
        
        pdt_count, pdt_name = pdt_str.strip().split(' ')
        product = chemicals.add_or_update(name=pdt_name, count_produced=pdt_count)

        for ing_str in ings_str.split(', '):
            ing_count, ing_name = ing_str.strip().split(' ')
    
            ingredient = chemicals.add_or_update(name=ing_name)
            product.add_needed_reaction(
                ingredient,
                ing_count,
            )
            # print(product.name, product.reactions_needed)

    return chemicals.root

def xcalculate_ore(reactions_list, inventory=None):
    if inventory is None:
        inventory = {}

    fuel = build_reactions_tree(reactions_list)

    inventory, ore_count = xtraverse_reactions(fuel, inventory=inventory)
        
    print(inventory)

    return ore_count
    
def calculate_ore(reactions, inventory=None):
    if inventory is None:
        inventory = {}
    
    root = build_reactions_tree(reactions)

    ore_count = traverse_reactions(root, fuel_needed=1, inventory=inventory)

    return ore_count

def do():
    with open('./puzzle14_input.txt') as f:
        reactions = f.read().split('\n')[:-1]

    ore_count = calculate_ore(reactions)
    
    print(ore_count)

def do_b():
    with open('./puzzle14_input.txt') as f:
        reactions = f.read().split('\n')[:-1]

    root = build_reactions_tree(reactions)
    inventory = {}
    fuel_count = 0
    initial_ore = 1000000000000

    milestone = 100000
    while initial_ore > 0:
        if initial_ore / 10000000 < milestone:
            print("Left:", initial_ore)
            milestone -= 1

        inventory, ore_count = traverse_reactions(root, inventory=inventory)
        # print(ore_count)
        
        initial_ore -= ore_count
        if initial_ore <= 0:
            break
        
        fuel_count += 1
        
    print(fuel_count)

def do_c():
    with open('./puzzle14_input.txt') as f:
        reactions = f.read().split('\n')[:-1]

    root = build_reactions_tree(reactions)
    ore_count = traverse_reactions(root, fuel_needed=1)
    
    initial_ore = 1000000000000
    approx_fuel = floor(initial_ore / ore_count)

    while True:
        ore_count = traverse_reactions(root, fuel_needed=approx_fuel)
        if initial_ore <= ore_count:
            upper_bound = approx_fuel
            break

        lower_bound = approx_fuel
        approx_fuel *= 2
        
        
    print(lower_bound, upper_bound)
    # binary search
    while True:
        approx_fuel = floor((upper_bound - lower_bound)/2) + lower_bound
        ore_count = traverse_reactions(root, fuel_needed=approx_fuel)
        
        print(upper_bound, lower_bound, approx_fuel, ore_count)
        if traverse_reactions(root, fuel_needed=approx_fuel+1) >= initial_ore and ore_count <= initial_ore:
            break
        elif ore_count >= initial_ore:
            upper_bound = approx_fuel
        elif ore_count <= initial_ore:
            lower_bound = approx_fuel

    print(approx_fuel)

    
def do_d():
    "Try multiplying the root"
    with open('./puzzle14_input.txt') as f:
        reactions = f.read().split('\n')[:-1]

    fuel_count = 1
    initial_ore = 1000000000000
    
    ore_required = 0
    fuel = build_reactions_tree(reactions)
    
    ore_count = traverse_reactions(fuel, inventory={})
        
    print(initial_ore/ore_count * initial_ore/traverse_reactions(fuel, fuel_needed=initial_ore/ore_count))
    
# do()
do_d()

