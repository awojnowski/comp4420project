import math
from searchtree import SearchTree
from xfasttrie import XFastTrie

class YFastTrie:
    # assumes that values is a sorted array
    def __init__(self, values, u):
        self.x_trie = None
        self.search_trees = {}

        def chunk_array(l):
            count = len(l)
            n = int(math.ceil(math.log(count, 2)))
            for i in range(0, count, n):
                yield l[i:i + n]

        chunks = list(chunk_array(values))
        reps = []
        for chunk in chunks:
            rep = chunk[0] + chunk[-1] - chunk[0]
            reps.append(rep)

            search_tree = SearchTree(chunk)
            self.search_trees[rep] = search_tree
        self.x_trie = XFastTrie(reps, u)


    def find(self, x):
        def find_tree(node, x):
            if node is None:
                return False
            if node.value == x:
                return True
            elif x > node.value:
                return find_tree(node.right_ptr, x)
            elif x < node.value:
                return find_tree(node.left_ptr, x)

        reps = self._find_reps(x)
        for rep in reps:
            if rep is None:
                continue
            tree = self.search_trees[rep]
            if find_tree(tree.root, x):
                return True
        return False


    def predecessor(self, x):
        def pred_tree(node, x):
            predecessor = None
            while True:
                if node is None:
                    break
                if node.value < x:
                    predecessor = node.value
                if x <= node.value:
                    node = node.left_ptr
                else:
                    node = node.right_ptr
            return predecessor

        reps = self._find_reps(x)
        best_result = None
        for rep in reps:
            if rep is None:
                continue
            tree = self.search_trees[rep]
            if tree.min > x:
                continue
            result = pred_tree(tree.root, x)
            if best_result is None or result > best_result:
                best_result = result
        return best_result


    def successor(self, x):
        def succ_tree(node, x):
            successor = None
            while True:
                if node is None:
                    break
                if node.value > x:
                    successor = node.value
                if x >= node.value:
                    node = node.right_ptr
                else:
                    node = node.left_ptr
            return successor

        reps = self._find_reps(x)
        best_result = None
        for rep in reps:
            if rep is None:
                continue
            tree = self.search_trees[rep]
            if tree.max < x:
                continue
            result = succ_tree(tree.root, x)
            if best_result is None or result < best_result:
                best_result = result
        return best_result


    def _find_reps(self, x):
        predecessor = None
        successor = self.x_trie.successor(x)
        if successor is None:
            if self.x_trie.find(x):
                successor = x
        if successor is not None:
            predecessor = self.x_trie.predecessor(successor)
        else:
            predecessor = self.x_trie.predecessor(x)
        return [predecessor, successor]
