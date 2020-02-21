from collections import deque


def sum_orbits(map):
    roots, _, _ = build_tree(map)
    # assumes single root
    checksums = roots[0].traverse()
    return sum(checksums)


class Node:
    def __init__(self, id):
        self.id = id
        self.children = []
        self.checksums = 0
        self.parent = None
    
    def add_parent(self, parent_node):
        self.parent = parent_node
        
    def add_child(self, child_node):
        # child = Node(child_id, self.checksums + 1)
        self.children.append(child_node)
        child_node.add_parent(self)
        
    def transfers_to(self, target_node):
        own_tree = set()
        current_node = self
        while current_node.parent:
            own_tree.add(current_node)
            current_node = current_node.parent

        current_node = target_node
        while current_node.parent:
            if current_node in own_tree:
                common_parent = current_node
                break
            current_node = current_node.parent
                
        common_parent.traverse()
        return self.checksums + target_node.checksums - 2


    def traverse(self):
        acc = []
        todo = deque(self.children)
        print(todo)
        while(len(todo) > 0):
            node = todo.popleft()
            if node.parent:
                node.checksums = node.parent.checksums + 1
            else:
                node.checksums = 0

            acc.append(node.checksums)

            for child in node.children:
                todo.append(child)

        return acc

    def rec_traverse(self, acc, curr):
        """
        acc is an Array that gets mutated
        curr is the checksum
        """
        acc.append(curr)
        # print(acc)
        if len(self.children) <= 0:
            return

        for child in self.children:
            child.traverse(acc, curr + 1)
            
        return acc
        
    def search(self, id):
        if self.id == id:
            return self
        if len(self.children) == 0:
            return None
            
        for child in self.children:
            result = child.search(id)
            if result:
                return result
        
        return None
    
    @property
    def is_root(self):
        return self.parent is None
        
    def __repr__(self):
        return f'<Node id={self.id} is_root={self.is_root}>'


def build_tree(init_map):
    nodes = {}
    map = deque(init_map)
    santa, you = None, None

    while len(map) > 0:
        rel = map.popleft()

        parent, child = rel.split(')')

        if parent in nodes:
            pnode = nodes[parent]
        else:
            pnode = Node(parent)
            nodes[parent] = pnode
            
        if child in nodes:
            cnode = nodes[child]
        else:
            cnode = Node(child)
            nodes[child] = cnode
            
            if child == "SAN":
                santa = cnode
            if child == "YOU":
                you = cnode
        
        pnode.add_child(cnode)
 
    roots = list(filter(
        lambda x: x.is_root,
        nodes.values()
    ))
    return roots, santa, you


map = [
    "COM)B",
    "B)C",
    "C)D",
    "D)E",
    "E)F",
    "B)G",
    "G)H",
    "D)I",
    "E)J",
    "J)K",
    "K)L"
]
# roots = _build_tree(map)
# print(roots)
# print(sum_orbits(map))

def part1():
    with open('./puzzle6_input.txt') as f:
        orbits = f.read().split('\n')[:-1]
    # print(orbits)
    # print(_build_tree(orbits))
    print(sum_orbits(orbits))

def execute():
    with open('./puzzle6_input.txt') as f:
        orbits = f.read().split('\n')[:-1]
    _, santa, you = build_tree(orbits)
    print(santa.transfers_to(you))

execute()
