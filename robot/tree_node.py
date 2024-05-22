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

    def clean_heuristic(self):
        self.heuristic = None
        for child in self.children:
            child.clean_heuristic()

    def visualize_tree(self, level=0):
        # Print the current node's value and heuristic
        print(" " * (level * 4) + f"LVL:{level},Value: {self.heuristic}")

        # Recursively print all children
        for child in self.children:
            child.visualize_tree(level + 1)
