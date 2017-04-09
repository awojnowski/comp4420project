import math

class Node:
    def __init__(self, value):
        self.child_ptr = None
        self.left_ptr = None
        self.right_ptr = None
        self.next_ptr = None
        self.prev_ptr = None

        self.value = value


class XFastTrie:
    # assumes that values is a sorted array
    def __init__(self, values, u):
        self.max = values[-1]
        self.min = values[0]

        bit_length = self._count_bit_length(u)
        self.bit_length = bit_length

        # build the level table and get the root node
        self.table = []
        for i in xrange(bit_length + 1):
            self.table.append({})

        root = Node(-1)
        self.root = root
        self.table[bit_length][root.value] = root

        # begin assembling the trie
        last_child = None
        for value in values:
            child = Node(value)
            if last_child is None:
                root.child_ptr = child
            else:
                last_child.next_ptr = child
            child.prev_ptr = last_child

            parent = root
            index = bit_length - 1
            while index >= 0:
                key = self._get_key(value, index)
                level = self.table[index]
                low_bit = key & 1

                leaf = parent.left_ptr if low_bit == 0 else parent.right_ptr
                if leaf is None:
                    if index == 0:
                        leaf = child
                    else:
                        leaf = Node(key)
                        leaf.child_ptr = child
                    level[key] = leaf
                    if low_bit == 0:
                        parent.left_ptr = leaf
                    else:
                        parent.right_ptr = leaf
                    if parent.left_ptr and parent.right_ptr:
                        parent.child_ptr = None
                else:
                    if parent.left_ptr is None:
                        if child.value < parent.child_ptr.value:
                            parent.child_ptr = child
                    elif parent.right_ptr is None:
                        if child.value > parent.child_ptr.value:
                            parent.child_ptr = child
                parent = leaf
                index -= 1

            last_child = child


    def find(self, x):
        return (self.table[0].get(x) is not None)


    def predecessor(self, x):
        if x <= self.min:
            return None
        if x > self.max:
            return self.max
        found = self.table[0].get(x)
        if found is not None:
            if found.prev_ptr is not None:
                return found.prev_ptr.value
            return None
        lowest_node = self._find_lowest_ancestor(x)
        child = lowest_node.child_ptr
        if child.value > x:
            if child.prev_ptr is not None:
                return child.prev_ptr.value
            return None
        return child.value


    def successor(self, x):
        if x >= self.max:
            return None
        if x < self.min:
            return self.min
        found = self.table[0].get(x)
        if found is not None:
            if found.next_ptr is not None:
                return found.next_ptr.value
            return None
        lowest_node = self._find_lowest_ancestor(x)
        child = lowest_node.child_ptr
        if child.value < x:
            if child.next_ptr is not None:
                return child.next_ptr.value
            return None
        return child.value


    def _count_bit_length(self, u):
        length = 0
        while u:
            length += 1
            u >>= 1
        return length


    def _get_key(self, value, index):
        return (value & ((2**(self.bit_length - index) - 1) << index)) >> index


    def _find_lowest_ancestor(self, x):
        l = 1
        r = self.bit_length - 1
        lowest_node = self.root
        while r > l:
            level_index = l + int(math.floor((r - l) / 2))
            level = self.table[level_index]
            key = self._get_key(x, level_index)
            node = level.get(key)
            if node is not None:
                lowest_node = node
                r = level_index
            else:
                l = level_index + 1
        return lowest_node
