import math

class Node:
    def __init__(self, value):
        self.left_ptr = None
        self.right_ptr = None
        self.value = value


class SearchTree:
    # assumes that values is a sorted array
    def __init__(self, values):
        self.max = values[-1]
        self.min = values[0]
        self.root = None

        def build_tree(values):
            if len(values) == 0:
                return None
            mid = int(math.floor(len(values) / 2.0))
            root = Node(values[mid])
            root.left_ptr = build_tree(values[0:mid])
            root.right_ptr = build_tree(values[mid + 1:])
            return root
        self.root = build_tree(values)
