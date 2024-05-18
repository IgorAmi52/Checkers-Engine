from robot.heuristic import get_heuristic


class TreeNode:
    def __init__(self, value=None):
        self.value = value
        self.heuristic = None
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_tree_depth(self):
        depth = 0
        node = self

        while node is not None:
            try:
                node = node.children[0]
                depth += 1
            except Exception:
                break
        return depth

    def set_heuristic(self, value):
        self.heuristic = value
